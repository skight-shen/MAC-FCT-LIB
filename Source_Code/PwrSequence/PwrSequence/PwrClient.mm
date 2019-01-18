//
//  PwrClient.m
//  PwrSequence
//
//  Created by AustinShih on 23/11/16.
//  Copyright © 2016年 AustinShih. All rights reserved.
//
#import <Foundation/NSFileHandle.h>
#import "PwrClient.h"

#define kHost_IP     @"host ip"
#define kHost_Port   @"host port"
bool dataReady = false;


@implementation PwrClient


@synthesize dataFilePath;
@synthesize byteFilePath;
@synthesize logOn;
@synthesize m_ClientSock;
@synthesize dataLast;
@synthesize m_channels;
@synthesize channelID;



- (id)initWithIPPort:(NSString*)hwName :(NSString*)ip :(short)port
{
    self = [super init];
    if (self) {
        dp = [[PwrDataParse alloc]init];
        dp.getAllFlag = false;
        
        bParseFinished = YES;
        m_strServerIp = [[NSMutableString alloc]initWithString:ip];
        m_port = port;
        
        m_ClientSock = [[GCDAsyncSocket_PS alloc]initWithDelegate:self delegateQueue:dispatch_queue_create([[NSString stringWithFormat:@"%@-%d",hwName,m_port]UTF8String],DISPATCH_QUEUE_CONCURRENT)];
        m_ClientSock.delegate = self;
        m_channels = 0;
        
        m_dataRecvBuffer = [[NSMutableData alloc]init];
        m_lockBuffer = [[NSLock alloc]init];
        dataLast = [[NSMutableData alloc]init];
        
        logOn = NO;
        ps_flag = 1;
        parseBuffLoc = 0;
        
        if (![self connect]) {
            [NSThread sleepForTimeInterval:0.5];
        }
    }
    return self;
}

- (void)dealloc
{
    [dp release];
    if (dataFilePath) {
        [dataFilePath release];
    }
    if (byteFilePath) {
        [byteFilePath release];
    }
    if (m_strServerIp) {
        [m_strServerIp release];
    }
    if (m_dataRecvBuffer) {
        [m_dataRecvBuffer release];
    }
    if (m_lockBuffer) {
        [m_lockBuffer release];
    }
    if (m_ClientSock) {
        [m_ClientSock release];
    }
    if (dataLast) {
        [dataLast release];
    }
    if (zmqPub) {
        zmqPub->close();
        delete zmqPub;
    }
    if (zmqPub_BKLT) {
        zmqPub_BKLT->close();
        delete zmqPub_BKLT;
    }

    [super dealloc];
}

- (int)connect
{
    NSError *err = nil;
    m_ConnState=[m_ClientSock connectToHost:m_strServerIp onPort:m_port error:&err];
    [dp SetDelegate:self];
    if(m_ConnState == NO)//fail
    {
        NSLog(@"failed to connect server：%@",m_strServerIp);
        return -1;
        
    }else
    {
        NSLog(@"<* Power sequencer * Connect To Server> %@:%d",m_strServerIp,m_port);
    }
    return 0;
}

- (int)initZmqPub:(const char*)address :(int)writeLog
{
    if (address) {
        zmqPub = new CPubliser();
        zmqPub->bind(address);
    }else{
        zmqPub = nil;
    }
    return 0;
}

- (int)initZmqPub_BKLT:(const char*)address :(int)writeLog
{
    if (address) {
        zmqPub_BKLT = new CPubliser();
        zmqPub_BKLT->bind(address);
    }else{
        zmqPub_BKLT = nil;
    }
    return 0;
}


- (BOOL)getConnectState
{
    return m_ConnState;
}

- (void)clearStubData
{
    [m_lockBuffer lock];
    [m_dataRecvBuffer resetBytesInRange:NSMakeRange(0, m_dataRecvBuffer.length)];
    [m_dataRecvBuffer setLength:0];
    [m_lockBuffer unlock];
}

- (void)clearDataLast
{
    [dataLast setLength:0];
    [self clearStubData];
}

- (int)disconnect
{
    [m_ClientSock disconnect];
    return 0;
}

- (void)updateConfig:(const char *)config :(int)flag :(int)configID
{
    dp.getAllFlag = (flag>0);
    channelID = configID;
    NSString *strConfig = [NSString stringWithUTF8String:config];
    NSArray * contentArray = [strConfig componentsSeparatedByString:@";"];
    int cfg_num = (int)[contentArray count];
    
    if ([contentArray count]>80) {
        cfg_num = 80;
    }
    m_channels = cfg_num;
    dp.myChannel = m_channels;
    for (int i=0; i<cfg_num; i++) {
        NSString *strLine = [contentArray objectAtIndex:i];
        NSArray * arConfig = [strLine componentsSeparatedByString:@","];//{"PP0V82_SLPDDR",1,0,1}
        if ([arConfig count] >=4){
            [dp._chName replaceObjectAtIndex:i withObject:[arConfig objectAtIndex:0]];
            [dp._gain replaceObjectAtIndex:i withObject:[arConfig objectAtIndex:1]];
            [dp._offset replaceObjectAtIndex:i withObject:[arConfig objectAtIndex:2]];
            [dp._onoff replaceObjectAtIndex:i withObject:[arConfig objectAtIndex:3]];
            
        }
    }
}

- (void)StartDL:(int)flag
{
    if (logOn) [self StopDL:flag];
    [self openLogFile:dataFilePath];
    receiveCount = 0;
    logOn = YES;
    bParseFinished = YES;
    dp.bBreakParse = false;
    dp.Time_s = 0;
    dp.Time_ms = 0;
    dp.framenum = 0;
    dp._1to40_FrameId = -1;
    dp._41to80_FrameId = -1;
    ps_flag = flag;
    dataLenth = 0;
    [dp InitParser];
    [self clearDataLast];
    
    std::unique_lock<std::mutex> ul(m_data);
    [dataLast setLength:0];

    [dp.strBL_B setString:@""];
    [dp.strBL_D setString:@""];

    
//    [self SaveFrameLog:@"PS start"];
    if (ps_flag == 1) {  //Power sequence
        NSMutableString *header = [[NSMutableString alloc]initWithString:@"Time,"];
        
        for (int i=0; i<m_channels; i++)
        {
            [header appendString:[NSString stringWithFormat:@"%@,",[dp._chName objectAtIndex:i]]];
        }
        if (m_channels >= 80) {
            [header appendString:@"Frame_ID_0-40,Frame_ID_40-80"];
        }
        
        NSMutableString *pubHeadStr = [[NSMutableString alloc]init];
        
        if (dp.getAllFlag) {
            //[self writetoFileEnd:header :dataFilePath];
            [self writeLogFile:header];
            [pubHeadStr appendString:header];
        }
        

        [pubHeadStr release];
        [header release];

    }else{
        NSMutableString * strFileHeader = [[NSMutableString alloc]initWithString:@"Time,BL"];
        if (dp.getAllFlag) {
            //[self writetoFileEnd:strFileHeader :dataFilePath];
            [self writeLogFile:strFileHeader];
        }
//        if (zmqPub_BKLT) {
//            zmqPub_BKLT->PulishString([strFileHeader UTF8String]);
//        }
        [strFileHeader release];
    }
    
    [NSThread sleepForTimeInterval:0.1];
  
    threadParseManage = [[NSThread alloc]initWithTarget:self selector:@selector(threadParseData) object:nil];
    [threadParseManage start];
}

- (void)StopDL:(int)flag
{
    logOn = NO;
    dp.bBreakParse = true;
    {
        std::unique_lock<std::mutex> ul(m_data);
        dataReady = true;
        cv_data.notify_all();
    }
    NSLog(@"wait dataparse thread finished...");
    while (!bParseFinished) {
        [[NSRunLoop currentRunLoop]runMode:NSDefaultRunLoopMode beforeDate:[NSDate date]];
        [NSThread sleepForTimeInterval:0.1];
    }

    NSLog(@"dataparse thread done...");
    NSLog(@"Data Receive: %ld",dataLenth);
//    [self SaveFrameLog:[NSString stringWithFormat:@"receive frame count: %ld",receiveCount]];
//    [self SaveFrameLog:[NSString stringWithFormat:@"receive frame count from byte: %ld",dataLenth/2020]];
//    [self SaveFrameLog:[NSString stringWithFormat:@"parse frame count: %d",dp.framenum]];
//    [self SaveFrameLog:@"PS stop"];



    if (threadParseManage) {
        [threadParseManage cancel];
        [NSThread sleepForTimeInterval:0.1];
        [threadParseManage release];
        threadParseManage = nil;
        bParseFinished = YES;
        
    }
    [dp.strBL_B setString:@""];
    [dp.strBL_D setString:@""];
    [dp InitParser];
    
    std::unique_lock<std::mutex> ul(m_data);
    [dataLast setLength:0];
    
    [self clearDataLast];
    [self closeLogFile];
}


-(void)socket:(GCDAsyncSocket_PS *)sock didConnectToHost:(NSString *)host port:(uint16_t)port

{
    NSLog(@"%@", [NSString stringWithFormat:@"socket delegate connected server:%@ . Success.",host]);
    
    [m_ClientSock readDataWithTimeout:-1 tag:0];
}

- (void)socketDidDisconnect:(GCDAsyncSocket_PS *)sock withError:(NSError *)err
{
    m_ConnState = NO;
    NSLog(@"socket disconnected:%@",err);
}

- (void)SaveLog:(NSString *)data logIndex:(int)index
{
    if (index == 1)
    {
        //[self writetoFileEnd:data :dataFilePath];
        [self writeLogFile:data];
        if (zmqPub) {
            zmqPub->PulishString([data UTF8String]);
        }
        
    }
}




-(void)writetoFileEnd:(NSString*)str :(NSString*)fPath
{
    if (![[NSFileManager defaultManager]fileExistsAtPath:fPath]) {
        [[NSFileManager defaultManager]createFileAtPath:fPath contents:nil attributes:nil];
        
    }
    NSFileHandle * fh = [NSFileHandle fileHandleForWritingAtPath:fPath];
    if(!fh) return;
    @try {
        [fh seekToEndOfFile];
        [fh writeData:[str dataUsingEncoding:NSASCIIStringEncoding]];
        [fh closeFile];
    }
    @catch (NSString *exception) {
        NSLog(@"catch file OperationException,excrption name:%@",exception);
    }
    @finally {
        
    }
    
}


-(BOOL)openLogFile:(NSString*)logPath
{
    [self closeLogFile];
    
    LogManager = fopen([logPath UTF8String], "a+");
    if (LogManager)
    {
        return YES;
    }
    
    return NO;
}

-(void)writeLogFile:(NSString*)logStr
{
    if (LogManager)
    {
        fwrite([logStr UTF8String], sizeof(char), [logStr length], LogManager);
        fflush(LogManager);
    }
}

-(void)closeLogFile
{
    if (LogManager)
    {
        fflush(LogManager);
        fclose(LogManager);
        LogManager = nil;
    }
}

-(void)socket:(GCDAsyncSocket_PS *)sock didReadData:(NSData *)data withTag:(long)tag
{
    if(!logOn)
    {
        [m_ClientSock readDataWithTimeout:-1 tag:0];
    
//        NSLog(@"Clear Buffer");
        return;
    }
    
    std::unique_lock<std::mutex> ul(m_data);
    [dataLast appendData:data];
    dataLenth += [data length];
    
    if ([data length] > 0)
    {
        if ([dataLast length] >= FRAME_LENGTH)
        {
            receiveCount++;
            dataReady = true;
            ul.unlock();
            cv_data.notify_one();  //notify threadParseData
        }
        else
        {
            dataReady = false;
            ul.unlock();
        }
    }
    [m_ClientSock readDataWithTimeout:-1 tag:0];
}

-(void)threadParseData
{
    while (1)
    {
        if(logOn)//start Logger
        {
            @autoreleasepool {
                bParseFinished  = NO;

                std::unique_lock<std::mutex> ul(m_data);
                if ([dataLast length] < FRAME_LENGTH) {
                    cv_data.wait(ul, []{return dataReady;});  //thread sleep,wait for dataReay
                    dataReady = false;
                }
                
                if ([dataLast length] < FRAME_LENGTH)
                    continue;
                
                NSRange rct;
                rct.location = 0;
                rct.length = FRAME_LENGTH;
                NSData * data = [NSData dataWithData:[dataLast subdataWithRange:rct]];
                if ([dataLast length]>=FRAME_LENGTH)
                {
                    rct.location = FRAME_LENGTH;
                    rct.length = [dataLast length]-FRAME_LENGTH;
                    NSData * dataTmp = [NSData dataWithData:[dataLast subdataWithRange:rct]];
                    [dataLast resetBytesInRange:NSMakeRange(0, dataLast.length)];
                    [dataLast setLength:0];
                    [dataLast appendData:dataTmp];
                }
                ul.unlock();

                [dp parseData:data];
 
                if (ps_flag != 1)
                {    //Backlight
                    NSArray * artd = [dp.strBL_D componentsSeparatedByString:@","];
                    NSArray * artb = [dp.strBL_B componentsSeparatedByString:@","];
                    for (long i=0; i<([artd count]-1); i++) {
                        //Time stamp
                        dp.Time_ms += 1;
                        int stp = (dp.Time_ms/1000);
                        dp.Time_s += stp;
                        dp.Time_ms -= (stp*1000);
                        
                        time_t t = (time_t)dp.Time_s;
                        tm * local = localtime(&t);
                        char buf[64];
                        memset(buf, 0, sizeof(buf));
                        strftime(buf, 64, "%Y-%m-%d %H:%M:%S", local);
                        NSString *strD = [NSString stringWithFormat:@"\r\n%s:%03d,%@",buf,dp.Time_ms,[[artd objectAtIndex:i]stringValue]];
                        NSString *strB = [NSString stringWithFormat:@"\r\n%s:%03d,%@",buf,dp.Time_ms,[[artb objectAtIndex:i]stringValue]];
                        if (dp.getAllFlag) {
                            [self writetoFileEnd:strD :dataFilePath];
                            [self writetoFileEnd:strB :byteFilePath];
                        }
    //                    if (zmqPub_BKLT) {
    //                        zmqPub_BKLT->PulishString([strD UTF8String]);
    //                    }
                    }
                }
                //[NSThread sleepForTimeInterval:0.01];
            }
            //[pool release];
        }
        else//Disable logger
        {
            std::unique_lock<std::mutex> ul(m_data);
            [dataLast resetBytesInRange:NSMakeRange(0, dataLast.length)];
            [dataLast setLength:0];
            NSLog(@"Clear DataBuffer");
            break;
        }
    }
    bParseFinished = YES;
    NSLog(@"Thread exit.");
}

-(void)SaveByteData:(NSData *)byteData
{
    NSMutableData* dataTmp = [NSMutableData data];
    [dataTmp appendData:byteData];
    Byte* dByte = (Byte*)[dataTmp bytes];
    
    NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
    [dateFormatter setDateFormat:@"yyyy-MM-dd-HH-mm-ss"];
    NSString * timePrix=[dateFormatter stringFromDate:[NSDate date]];
    [dateFormatter release];
    
    NSMutableString *stringData = [NSMutableString string];
    [stringData appendString:[NSString stringWithFormat:@"%@ Frame start\r\n",timePrix]];
    for (int i=0; i<[byteData length]; i++) {
        [stringData appendFormat:@"%02X ",dByte[i]];
    }
    [stringData appendString:[NSString stringWithFormat:@"\r\n%@ Frame stop\r\n",timePrix]];

    NSFileManager *fm = [NSFileManager defaultManager];
    if (![fm fileExistsAtPath:byteFilePath]) {
        [fm createFileAtPath:byteFilePath contents:nil attributes:nil];
    }
    NSFileHandle * fh = [NSFileHandle fileHandleForWritingAtPath:byteFilePath];
    if(!fh) return;
    [fh seekToEndOfFile];
    [fh writeData:[stringData dataUsingEncoding:NSASCIIStringEncoding]];
    [fh closeFile];
}

-(void)SaveFrameLog:(NSString *)data
{
    NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
//    [dateFormatter setDateFormat:@"yyyy-MM-dd"];
//    NSDate* logTime = [NSDate date];
//    NSString * strLogTime=[dateFormatter stringFromDate:logTime];
//    [dateFormatter release];
    
    NSString *fileName = [NSString stringWithFormat:@"/vault/Intelli_log/IA_log/UUT%d_PwrFrameLog.txt",channelID];
    NSFileManager *fm = [NSFileManager defaultManager];
    if (![fm fileExistsAtPath:fileName]) {
        [fm createFileAtPath:fileName contents:nil attributes:nil];
    }
    
    [dateFormatter setDateFormat:@"yyyy-MM-dd-HH-mm-ss"];
    NSString * timePrix=[dateFormatter stringFromDate:[NSDate date]];
    [dateFormatter release];
    
    NSMutableString *logData = [NSMutableString stringWithFormat:@"%@\t%@\r\n",timePrix,data];
    
    NSFileHandle * fh = [NSFileHandle fileHandleForWritingAtPath:fileName];
    if(!fh) return;
    [fh seekToEndOfFile];
    [fh writeData:[logData dataUsingEncoding:NSASCIIStringEncoding]];
    [fh closeFile];
}

-(void)setPwrSeqChannel:(int)ch
{
    return [dp setPwrSeqChannel:ch];
}

-(int)getPwrSeqChannel
{
    return [dp getPwrSeqChannel];
}

-(void)resetTimeStamp
{
    dp.Time_s = 0;
    dp.Time_ms = 0;
}

@end

