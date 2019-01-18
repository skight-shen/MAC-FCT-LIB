//
//  DLClient.m
//  TCPManager
//
//  Created by Liang on 15-4-27.
//  Copyright (c) 2015年 Liu Liang. All rights reserved.
//

#import "DLClient.h"
//#import "RegexKitLite.h"

#define kHost_IP     @"host ip"
#define kHost_Port   @"host port"

#include <string>
@implementation DLClient
@synthesize logOn;
@synthesize m_ClientSock;
@synthesize dataLast;


- (id)initWithIPPort:(NSString*)hwName :(NSString*)ip :(short)port
{
    self = [super init];
    if (self)
    {
        dp = [[DataParse alloc]init];
        
        for (int i=0; i<DATALOGGER_CHANNEL_NUM; i++) {
            dp->getAllFlag[i] = FALSE;
            dp->_resdiv[i] = 1.0;
            dp->_gain[i] = 3.91176;
            dp->_refVolt[i] = 2.5;
            dp->_res[i] = 0.5;
            //NSLog(@"Init Gain:%.4f,ref:%.4f,res:%.4f,res div:%.4f",dp->_gain[i],dp->_refVolt[i],dp->_res[i],dp->_resdiv[i]);
        }
        bParseFinished = YES;
        
        m_strServerIp = [[NSMutableString alloc ]initWithString:ip];
        m_port = port;
        
        m_ClientSock = [[GCDAsyncSocket alloc]initWithDelegate:self delegateQueue:dispatch_queue_create([[NSString stringWithFormat:@"%@-%d",hwName,m_port] UTF8String], DISPATCH_QUEUE_CONCURRENT)];
        
        m_ClientSock.delegate = self;
        
        m_dataRecvBuffer = [[NSMutableData alloc] init];
        m_strReadBuffer = [[NSMutableString alloc] init];
        m_lockBuffer = [[NSLock alloc] init];
        m_strOutput  = [[NSMutableString alloc] init];
        m_strStringToDetect  = [[NSMutableString alloc] initWithString:@"\r\n"];
        m_strConfigPath  = [[NSMutableString alloc] init];
        
        dataLast = [[NSMutableData alloc]init];
        
        logOn = NO;
        if(![self connect])
        {
            [NSThread sleepForTimeInterval:0.5];
//            [self getLinearIndex];
        }
//        [NSThread detachNewThreadSelector:@selector(threadParseData) toTarget:self withObject:nil];
    }
    [dp SetDelegate:self];
    return self;
}

- (int)initZmqPub:(const char*)address
{
    int ret = -1;
    zmqPub0 = new CPubliser();
    ret = zmqPub0->bind(address);
    return ret;
}

#pragma mark Update config
-(void)updateConfig:(int)channel :(float)resdiv :(float)gain :(float)refVolt :(float)res :(int)flag :(int)unitConvert
{
    dp->getAllFlag[channel] = (flag>0);
    dp->_resdiv[channel] = resdiv;
    dp->_gain[channel] = gain;
    dp->_refVolt[channel] = refVolt;
    dp->_res[channel] = res;
    dp->iUnitConvert[channel] = unitConvert;
    if (dp.myChannel < channel) dp.myChannel = channel;
    
    NSLog(@"update mychannel:%d",dp.myChannel);
    
    //NSLog(@"Update Gain:%.4f,ref:%.4f,res:%.4f,res div:%.4f,unit:%d",dp->_gain[channel],dp->_refVolt[channel],dp->_res[channel],dp->_resdiv[channel],dp->iUnitConvert[channel]);
}

-(void)updateCalFactor:(int)channel :(float)gain :(float)offset
{
    dp->k[channel] = gain;
    dp->b[channel] = offset;
    if (dp.myChannel < channel) dp.myChannel = channel;
    
    NSLog(@"update mychannel:%d",dp.myChannel);
}

-(void)setLogPath:(const char *)header :(const char*) filename
{
    NSLog(@"update LogName:%s %s",header,filename);
    std::string strFileName = std::string(filename);
    NSString * filePath = [NSString stringWithFormat:@"%s",strFileName.c_str()];
    NSString * str = [filePath stringByDeletingPathExtension];
    
    filePath = [NSString stringWithFormat:@"%@_Data.csv",str];
    NSLog(@"update LogPath:%s %s",header,filename);
    if (![[NSFileManager defaultManager]fileExistsAtPath:filePath]) {
        NSLog(@"update LogPath: Check Exits");
        [[NSFileManager defaultManager]createFileAtPath:filePath contents:nil attributes:nil];
        NSLog(@"update LogPath: Check After Create");
        dp->dataFilePath[0] = filePath;
        NSLog(@"update LogPath: Check After Set");
    }
    NSLog(@"Start To Save Log");
    [self SaveLog:[NSString stringWithUTF8String:header]];
    NSLog(@"End To Save Log");
}

-(void)getLinearIndex
{
    getGainFlag = YES;
    [self setDetectString:@"\n"];
    NSString * str = [self sendRecv:@"[12345678]eeprom read string(datalogger,cat08,0x80,9)\r\n" :2];
    if(str)//[2132]ACK(“length:44”;330,488,330,494)
    {
        NSString * len = [str stringByMatching:@"length:(%d*)" capture:1];//
        if(len)
        {
            str = [self sendRecv:[NSString stringWithFormat:@"[23456789]eeprom read string(datalogger,cat08,0x89,%@)\r\n",len] :2];
            if(str)//[2132]ACK(“offset:245.09340986054kgain:523.9112156854”;369,296,369,314)
            {
                NSString * kStr = [str stringByMatching:@"offset:(.-)k" capture:1];
                NSString * bStr = [str stringByMatching:@"gain:(.-)\"" capture:1];
                //NSLog(@"< Datalogger Linear Factor > k: %@, b: %@", kStr, bStr);
                if(kStr) dp->k[0] = [kStr floatValue];
                if(bStr) dp->b[0] = [bStr floatValue];
            }
            else
                NSLog(@"< Error: Fail to get Linear Factor, Set to default > k:1, b:0");
        }
        else
            NSLog(@"< Error: Fail to get Length of Linear Factor, Set to default > k:1, b:0");
    }
    else
        NSLog(@"< Error: No response when to get length, Set to default > k:1, b:0");
    
    getGainFlag = NO;
}

- (void)dealloc
{
    [dp release];
    if(m_strServerIp)
        [m_strServerIp release];
    if(m_dataRecvBuffer)
        [m_dataRecvBuffer release];
    if(m_strReadBuffer)
        [m_strReadBuffer release];
    if(m_lockBuffer)
        [m_lockBuffer release];
    if(m_lockBuffer)
        [m_strOutput release];
    if(m_strStringToDetect)
        [m_strStringToDetect release];
    if(m_strConfigPath)
        [m_strConfigPath release];
    if(m_ClientSock)
        [m_ClientSock release];
    if(dataLast){
        [dataLast release];
    }
    zmqPub0->close();
    delete zmqPub0;
    
    [super dealloc];
}
#pragma mark client operation
- (int)connect
{
    NSError *err = nil;
    m_ConnState=[m_ClientSock connectToHost:m_strServerIp onPort:m_port error:&err];
    if(m_ConnState == NO)//fail
    {
        NSLog(@"failed to connect server：%@",m_strServerIp);
        return -1;
        
    }else
    {
        NSLog(@"<* ArmDL * Connect To Server> %@:%d",m_strServerIp,m_port);
    }
    return 0;
}

- (int)disconnect
{
    [m_ClientSock disconnect];
    //not implemented
    return 0;
}

-(void)socket:(GCDAsyncSocket *)sock didConnectToHost:(NSString *)host port:(uint16_t)port

{
    //NSLog(@"%@", [NSString stringWithFormat:@"socket delegate connected server:%@ . Success.",host]);
    
    [m_ClientSock readDataWithTimeout:-1 tag:0];
}

- (void)socketDidDisconnect:(GCDAsyncSocket *)sock withError:(NSError *)err

{
    m_ConnState = NO;
    NSLog(@"socket disconnected:%@",err);
}

-(void)writetoFileEnd:(NSString*)str :(NSString*)fPath
{
    @try {
        NSFileHandle * fh = [NSFileHandle fileHandleForWritingAtPath:fPath];
        if(!fh) return;
        [fh seekToEndOfFile];
        [fh writeData:[str dataUsingEncoding:NSASCIIStringEncoding]];
        [fh closeFile];
    } @catch (NSException *exception) {
        NSLog(@"write fileexception error");
    } @finally {
        
    }

}

-(void)SaveLog:(NSString *)str
{
    [self writetoFileEnd:str :dp->dataFilePath[0]];
    zmqPub0->PulishString([str UTF8String]);
}

-(void)socket:(GCDAsyncSocket *)sock didReadData:(NSData *)data withTag:(long)tag
{
    
    if(!logOn)
    {
    [m_ClientSock readDataWithTimeout:-1 tag:0];
    return;
    }
    
    [m_lockBuffer lock];

    [m_dataRecvBuffer appendData:data];
    
    [m_lockBuffer unlock];
    
    [m_ClientSock readDataWithTimeout:-1 tag:0];
    //[m_ClientSock readDataToLength:FRAME_LENGTH withTimeout:-1 tag:0];
    
}
#pragma mark thread parse data
-(void)threadParseData
{
    while (1)
    {
        if(logOn)//start Logger
        {
            bParseFinished  = NO;
            [m_lockBuffer lock];
            [dataLast appendData:m_dataRecvBuffer];
            [m_dataRecvBuffer setLength:0];
            [m_lockBuffer unlock];
            
            //NSLog(@"WSA data last Length:%ld",[dataLast length]);
            if ([dataLast length]>=FRAME_LENGTH) {
                NSRange rct;
                rct.location = 0;
                rct.length = FRAME_LENGTH;
                NSData * data = [dataLast subdataWithRange:rct];
                //NSLog(@"Start parse dl data:");
                [dp parseData:data];
                
            
                
                rct.location = FRAME_LENGTH;
                rct.length = [dataLast length]-FRAME_LENGTH;
                NSData * dataTmp = [dataLast subdataWithRange:rct];
                [dataLast setLength:0];
                [dataLast appendData:dataTmp];
                //[dataLast appendBytes:[dataTmp bytes] length:rct.length];
            }else{
                [[NSRunLoop currentRunLoop]runMode:NSDefaultRunLoopMode beforeDate:[NSDate date]];
                [NSThread sleepForTimeInterval:0.05];
            }
        }
        else//Disable logger
        {
            [[NSRunLoop currentRunLoop]runMode:NSDefaultRunLoopMode beforeDate:[NSDate date]];
            [NSThread sleepForTimeInterval:0.1];
            break;
        }
    }
    [dp clearData];
    bParseFinished = YES;
}

-(void)clearDataLast
{
    [self clearStubData];
    [self clearBuffer];
    [dp clearData];
    [dataLast setLength:0];
}

#pragma mark RMS testing
- (NSString *)startRMS:(int)channel
{
    dp->count[channel] = 0;
    dp->powSum[channel] = 0.0;
    dp->maxValue[channel] = 0.0;
    dp->minValue[channel] = 0.0;
    dp->sum[channel] = 0.0;
    
    dp->bFirstValue[channel] = true;
    dp->bRMS[channel] = true;

    return dp->trigerTime[channel];
}

- (NSString *)endRMS:(int)channel
{
    dp->bRMS[channel] = false;
    dp->bFirstValue[channel] = false;
    return dp->trigerTime[channel];
}

- (double)getRMS:(int)channel
{
    unsigned long count = dp->count[channel];
    long double powSum = dp->powSum[channel];
    //NSLog(@" RMS count: %ld, powSum: %Lf",count, powSum);
    if (count == 0) {
        return 0.0;
    }
    return (double)sqrtl(powSum/count);
}

- (double)getAverage:(int)channel
{
    unsigned long count = dp->count[channel];
    long double sum = dp->sum[channel];
    if(count==0)
        return 0.0;
    return (double)(sum/count);
}

- (float)getMax:(int)channel
{
    return dp->maxValue[channel];
}

- (float)getMin:(int)channel
{
    return dp->minValue[channel];
}

- (unsigned long)getCount:(int)channel
{
    return dp->count[channel];
}
#pragma mark End RMS testing

- (BOOL)getConnectState;
{
    return m_ConnState;
}

- (NSData*)getStubData;
{
    return m_dataRecvBuffer;
}

- (void)clearStubData
{
    [m_dataRecvBuffer setLength:0];
}

- (void)clearBuffer
{
    [m_lockBuffer lock];
    [m_strReadBuffer setString:@""];
    [m_lockBuffer unlock];
}

- (void)setDetectString:(NSString*)strDetectString
{
    [m_strStringToDetect setString:strDetectString];
}

-(int)send:(NSString*)str
{
    if ((m_ConnState && str) == false) return -1;
    
    
    [m_lockBuffer lock];
    [m_strReadBuffer setString:@""];
    [m_lockBuffer unlock];
    
    
    //NSLog(@"about to send: %@  to server", str);
    
    const char* szData = [str UTF8String];
    NSData* dataToSend = [NSData dataWithBytes:szData length:[str length]];
    
    [m_ClientSock writeData:dataToSend withTimeout:-1 tag:0];
    
    [m_ClientSock readDataWithTimeout:-1 tag:0];
    
    return 0;
    
}

-(int)waitString:(int)timeout
{
    if (m_ConnState == NO) {
        return -1;
    }
    int r = 0;
    NSTimeInterval starttime = [[NSDate date]timeIntervalSince1970];
    double tm = (double)timeout/1000.0;
    while (1)
    {
        NSTimeInterval now = [[NSDate date]timeIntervalSince1970];
        if ((now-starttime)>=tm)
        {
            r = -2;
            break;
        }
        
        if ([[NSThread currentThread] isCancelled])
        {
            r = 1;
            break;
        }
        
        NSString* strTmp = nil;
        [m_lockBuffer lock];
        if (m_strReadBuffer) {
            strTmp = [NSString stringWithString:m_strReadBuffer];
        }
        [m_lockBuffer unlock];
        
        if (strTmp && [strTmp length]>0) {
            NSRange range = [strTmp rangeOfString:m_strStringToDetect];
            if (range.location!=NSNotFound)
            {
//                 NSLog(@"decteted string successfully");
                r = 0;
                break;
            }
        }
        [[NSRunLoop currentRunLoop] runMode:NSDefaultRunLoopMode beforeDate:[NSDate date]];
        [NSThread sleepForTimeInterval:0.01];
    }
//    NSLog(@"dectetString returned");
    return r;
}

- (NSString*)readString
{
    [m_lockBuffer lock];
    [m_strOutput setString:@""];
    if (m_strReadBuffer) {
        [m_strOutput setString:m_strReadBuffer];
        [m_strReadBuffer setString:@""];
    }
    [m_lockBuffer unlock];
    return m_strOutput;
}

- (NSString*)sendRecv:(NSString*)str :(int)timeout
{
    if (m_ConnState == NO) {
        return nil;
    }
    if (str) {
        [self send:str];
    }
    int r = [self waitString:timeout];
    if (r >= 0) {
        return [self readString];
    }
    return nil;
}
#pragma mark start/end datalogger
-(void)StartDL
{
    logOn = YES;
    if (!bParseFinished) {
        [self StopDL];
    }
   
    dp.bBreakParse = false;
    threadParseManage = [[NSThread alloc]initWithTarget:self selector:@selector(threadParseData) object:nil];
    [threadParseManage start];
}

-(void)StopDL
{
    logOn = NO;
    dp.bBreakParse = true;

    while (!bParseFinished) {
        [[NSRunLoop currentRunLoop] runMode:NSDefaultRunLoopMode beforeDate:[NSDate date]];
        [NSThread sleepForTimeInterval:0.1];
    }

    if(threadParseManage)
    {
        [threadParseManage cancel];
        [NSThread sleepForTimeInterval:0.1];
        [threadParseManage release];
        threadParseManage = nil;
        bParseFinished = YES;
    }

    [self clearDataLast];
}

-(void)setArmChannel:(int)ch
{
    [dp setArmChannel:ch];
}

-(int)getArmChannel
{
    return [dp getArmChannel];
}

@end
