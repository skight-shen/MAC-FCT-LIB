//
//  NanoHippoDev.m
//  socket_udp
//
//  Created by AustinShih on 1/12/16.
//  Copyright ¬© 2016Âπ¥ AustinShih. All rights reserved.
//

#include "NanoHippoDev.h"
#if NANO
#include "zmq.h"

#endif
#include <iostream>
#include <sstream>
#include <unistd.h>
#include <unistd.h>
#include <vector>

#include "lib/get_hash.h"

#import <ATDeviceElements/ATDeviceNanoHippo.h>

#define SMC_PORT 31339
#define DEBUG_PORT 4445

NSLock * g_LockCB = [[NSLock alloc]init];
ATDeviceNanoHippo *phippo = [[ATDeviceNanoHippo alloc] init];




NanoHippoDev::NanoHippoDev()
{
    pthread_mutex_init(&m_mutex, nil);

    m_returnData = [[NSData alloc]init];
    m_serialDataBuf = [[NSMutableData alloc]init];
    m_hippoDataBuf = [[NSMutableData alloc]init];
    m_defaultLogFile = [[NSMutableString alloc]init];
    
    m_hippoDataArrayByPort = [[NSMutableDictionary alloc]init];
    m_channel = [[NSMutableArray alloc]init];

    m_MutableDetect = [[NSMutableString alloc]init];
    [m_defaultLogFile setString:@"/vault/PRM_log/iefi_file.txt"];

    bNeedPub = false;
    bFilterUnreadable = false;
    bFilterColorCode = false;
    isOpen = false;
    bAppendBufTimeStamp = false;
    isThreadExit = false;
    m_writeInterval = 0;
    m_bPotassiumFlag= false;
}

NanoHippoDev::~NanoHippoDev()
{
    pthread_mutex_destroy(&m_mutex);
    if (isOpen) Close();

    CloseZMQ();
    [m_serialDataBuf release];
    
    [m_hippoDataArrayByPort removeAllObjects];
    [m_hippoDataArrayByPort release];
    if (m_returnData) {
        [m_returnData release];
    }
    [m_channel removeAllObjects];
    [m_channel release];

    [m_defaultLogFile release];
}


int NanoHippoDev::CreatePub(const char *publish,int port)
{
#if NANO
    std::map<int,CPubliser *>::iterator iter = m_Pub.find(port);
    if(iter!=m_Pub.end())
    {
        CPubliser *tmp = iter->second;
        tmp->close();
        delete tmp;
    }
    
    CPubliser * pub = new CPubliser();
    m_Pub[port] = pub;
    bNeedPub = true;
    return pub->bind(publish);
#else
    return 0 ;
#endif
}


int NanoHippoDev::CreateRep(const char *reply)
{
#if NANO
    CReplier::close();
    CReplier::bind(reply);
#endif
    return 0;
}


NSString * NanoHippoDev::LocalTimeStampStr()
{
    NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
    [dateFormatter setDateFormat:@"yyyy/MM/dd HH:mm:ss.SSS"];
    NSString *str =  [dateFormatter stringFromDate:[NSDate date]];
    [dateFormatter release];
    return str;
}

int NanoHippoDev::Open(const char * serialdev)
{
    NSLog(@"Init!!!!!!!!");
    if (isOpen) Close();
    strcpy(m_serialdev,serialdev);
    isOpen = false;
    pthread_create(&m_thread, nullptr,NanoHippoDev::Init,this);
    [NSThread sleepForTimeInterval:3];
    if (!isOpen) return -1;
    return 0;
}

void * NanoHippoDev::Init(void * arg)
{
    NSError * myError = nil;
    
    NanoHippoDev * pThis = (NanoHippoDev *)arg;

    @try {
        BOOL success = [phippo openWithSerialPath:[NSString stringWithUTF8String:pThis->m_serialdev]
                            andSerialDataCallBack:^(NSData *data){
                            }
                                 andHippoCallBack:^( NSNumber * srcPort,NSData *data){
                                     if (!pThis->isOpen) return;
                                     
                                     if ([srcPort intValue] ==  SMC_PORT) {
                                         pThis->_log_smc_file(SMC_PORT, pThis->ConvertDataToStr(data));
                                         return;
                                     }
                                     
                                     if ([srcPort intValue] ==  DEBUG_PORT) {
                                         pThis->_log_smc_file(DEBUG_PORT, pThis->ConvertDataToStr(data));
                                         return;
                                     }

                                     if (!pThis->m_Pub[[srcPort intValue]])
                                     {
                                         return;
                                     }
                                     
                                     @autoreleasepool
                                     {
                                         
                                         if(data && [data length] > 0)
                                         {
                                             @synchronized (pThis->m_hippoDataBuf)
                                             {
                                                 pThis->_log_file_timestamp([srcPort intValue],pThis->ConvertDataToStr(data));
                                                 
                                                 if (pThis->bAppendBufTimeStamp)
                                                     [pThis->m_hippoDataBuf appendData:[pThis->LocalTimeStampStr() dataUsingEncoding:NSUTF8StringEncoding]];
                                                 [pThis->m_hippoDataBuf appendData:data];
                                                 
                                               }
                                           }
                                      }
                                 }
                  andNewHippoChannelAddedCallBack:^( NSNumber * srcPort)
                        {
                            NSLog(@"New Channel added %@ %s",srcPort,pThis->m_serialdev);
                            @synchronized (pThis->m_channel)
                            {
                                [pThis->m_channel addObject:srcPort];
                            }
                        }
                                         andError:&myError];
        
        if(!success){
            NSLog(@"Failed to open serial dev: %s\n",pThis->m_serialdev);
            pThis->isOpen = false;
        }else{
            pThis->isOpen = true;
            pThis->isThreadExit = false;
            while (pThis->isOpen)
            {
                @autoreleasepool {
                    [[NSRunLoop currentRunLoop]runMode:NSDefaultRunLoopMode beforeDate:[NSDate date]];
                    [NSThread sleepForTimeInterval:0.03];
                }
            }
        }
    }
    @catch (NSException *exception) {
        NSLog(@"Open exception Reson:%@",exception);
        pThis->_log_file_timestamp(31337,[NSString stringWithFormat:@"Open exception Reson:%@",exception]);

    }
    @finally {
        
    }
    
    NSLog(@"running phippo close");
    pThis->isOpen = false;
    [NSThread sleepForTimeInterval:0.5];
    
    NSLog(@"Init Done");
    pThis->isThreadExit = true;
   
    return nullptr;
}

int NanoHippoDev::CloseZMQ()
{
#if NANO
    for (std::map<int,CPubliser *>::iterator i=m_Pub.begin(); i!=m_Pub.end();)
    {
        CPubliser *tmp = i->second;
        tmp->close();
        delete i->second;
        i->second = NULL;
        m_Pub.erase(i++);
    }
    
    CReplier::close();
#endif
    return 0;
}

int NanoHippoDev::Close()
{
    isOpen = false;
    while (!isThreadExit)
    {
        [[NSRunLoop currentRunLoop]runMode:NSDefaultRunLoopMode beforeDate:[NSDate date]];
        NSLog(@"Waiting thread close!!!! done");
        [NSThread sleepForTimeInterval:0.3];
    }
    NSLog(@"ThreadExit complete!!!");
    @try {
        [phippo close];
    }
    @catch (NSException *exception) {
        NSLog(@"Close Exception Reson:%@",exception);
    }
    @finally {
        
    }
    
    @synchronized (m_hippoDataArrayByPort) {
        [m_hippoDataArrayByPort removeAllObjects];
    }
    
    @synchronized (m_channel) {
        [m_channel removeAllObjects];
    }
    
    @synchronized (m_hippoDataBuf) {
        [m_hippoDataBuf replaceBytesInRange:NSMakeRange(0, [m_hippoDataBuf length]) withBytes:NULL length:0];
    }
    
    @synchronized (m_serialDataBuf) {
        [m_serialDataBuf resetBytesInRange:NSMakeRange(0, [m_serialDataBuf length])];
        [m_serialDataBuf setLength:0];
    }
    return 0;
}


int NanoHippoDev::SetPubOpt(int needPub)
{
    bNeedPub = (needPub>0)? YES:NO;
    return 0;
}

void NanoHippoDev::_log_smc_file(int port, NSString *string)
{
    
    
    NSString * strTime = LocalTimeStampStr();
    NSString *file;
    
    if ([string length] == 0) return;
    NSString *str = [string stringByReplacingOccurrencesOfString:@"\r" withString:@"\n"];
    
    NSString *strCont = [NSString stringWithFormat:@"\r\n%@ : \t %@",strTime,str];
    
    std::map<int,std::string>::iterator iter = m_logFile.find(port);
    if(iter!=m_logFile.end())
    {
        file = [NSString stringWithUTF8String:iter->second.c_str()];
    }
    else
    {
        return;
    }

    
    if (![[NSFileManager defaultManager]fileExistsAtPath:file]) {
        [[NSFileManager defaultManager]createFileAtPath:file contents:nil attributes:nil];
    }

    
    NSFileHandle *f = [NSFileHandle fileHandleForWritingAtPath:file];
    if (f) {
        [f seekToEndOfFile];
        [f writeData:[strCont dataUsingEncoding:NSASCIIStringEncoding]];
        [f closeFile];
    }

}

void NanoHippoDev::_log_file_timestamp(int port,NSString *strtoParse)
{
    NSString *file;
    NSString * strTime = LocalTimeStampStr();
    
    NSString * strCont = @"";
    bool bAppendLogTimeStamp = true;
    
    if ([strtoParse length] == 0) return;
    NSString *str = [strtoParse stringByReplacingOccurrencesOfString:@"\r" withString:@"\n"];
    
    std::map<int,bool>::iterator iter_t = m_bAppendLogTimeStamp.find(port);
    if(iter_t!=m_bAppendLogTimeStamp.end())
    {
        bAppendLogTimeStamp = iter_t->second;
    }
    
    if ([str rangeOfString:@"\n"].location == NSNotFound)
    {
        if (bAppendLogTimeStamp)
        {
            strCont = [NSString stringWithFormat:@"\r\n%@ : \t %@",strTime,str];
            bAppendLogTimeStamp = false;
        }
        else
        {
            strCont = str;
        }
    }
    else
    {
        NSArray *array = [str componentsSeparatedByString:@"\n"];
        NSMutableString *muteStr = [NSMutableString string];
        for (int i = 0; i < array.count; i++)
        {
            if (i == 0 && !bAppendLogTimeStamp)
            {
                [muteStr appendString:[array objectAtIndex:i]];
            }
            else
            {
                [muteStr appendString:[NSString stringWithFormat:@"\r\n%@ : \t %@",strTime,[array objectAtIndex:i]]];
                bAppendLogTimeStamp = true;
            }
            
            if (i == array.count -1 && ([str characterAtIndex:[str length]-1])!='\n')
            {
                bAppendLogTimeStamp = false;
            }
        }
        
        strCont = muteStr;
    }
    
    m_bAppendLogTimeStamp[port] = bAppendLogTimeStamp;
    
    if (1)
    {
#if NANO
        std::map<int,CPubliser *>::iterator iter = m_Pub.find(port);
        if(iter!=m_Pub.end())
        {
            CPubliser *tmp = iter->second;
            tmp->Pulish((void *)[strCont UTF8String],[strCont length]);
        }
#endif
    }
    
    std::map<int,std::string>::iterator iter = m_logFile.find(port);
    if(iter!=m_logFile.end())
    {
        file = [NSString stringWithUTF8String:iter->second.c_str()];
    }
    else
    {
        file = [NSString stringWithFormat:@"%@_%d",m_defaultLogFile,port];
    }
    
    if (![[NSFileManager defaultManager]fileExistsAtPath:file]) {
        [[NSFileManager defaultManager]createFileAtPath:file contents:nil attributes:nil];
    }
    
    NSFileHandle *f = [NSFileHandle fileHandleForWritingAtPath:file];
    if (f) {
        [f seekToEndOfFile];
        [f writeData:[strCont dataUsingEncoding:NSASCIIStringEncoding]];
        [f closeFile];
    }
}

void NanoHippoDev::Log_file_timestamp(int port,char *str)
{
    _log_file_timestamp(port,[NSString stringWithUTF8String:str]);
}

int NanoHippoDev::SetWriteTimeInterval(unsigned int usleeps)
{
    m_writeInterval = usleeps;
    return 0;
}


int NanoHippoDev::WriteString(int port,const char* pbuf)
{
    if (!isOpen) return -1;
    
    @autoreleasepool {
        
        NSString *str = [NSString stringWithFormat:@"%s",pbuf];
        NSError * myError = nil;
        int ret = -1;
        
        if (m_writeInterval == 0)
        {
            if (port == -1)
            {
                @synchronized (m_serialDataBuf)
                {
                    _log_file_timestamp(port,[NSString stringWithFormat:@"\n[SendCmd2]:%@",str]);
                    ret =  (int)[phippo writeSerialData:[str dataUsingEncoding:NSUTF8StringEncoding] andError:&myError];
                }
            }
            else
            {
                @synchronized (m_hippoDataBuf)
                {
                    if ([phippo respondsToSelector:@selector(writeHippoDataToPort:andData:andError:)])
                    {
                        _log_file_timestamp(port,[NSString stringWithFormat:@"\n[SendCmd3]:%@",str]);
                        if ([phippo writeHippoDataToPort:[NSNumber numberWithInt:port] andData:[str dataUsingEncoding:NSUTF8StringEncoding] andError:&myError])
                        {
                            ret = 0;
                        }
                        else
                        {
                            NSLog(@"phippo write error!!!!!");
                            _log_file_timestamp(port,[NSString stringWithFormat:@"\n[SendCmd ERROR]:%@",str]);
                            ret = -1;
                        }
                        
                        if (myError)
                        {
                            NSLog(@"phippo write failed:%@", [myError localizedDescription]);
                            _log_file_timestamp(port,[NSString stringWithFormat:@"\n[SendCmd Error]:%@",[myError localizedDescription]]);
                        }
                    }
                    else
                    {
                        NSLog(@"phippo not repsond!!!!!");
                        _log_file_timestamp(port,[NSString stringWithFormat:@"\n[SendCmd ERROR]:%@",str]);
                        return -1;
                    }
                }
            }
            return ret;
        }
        
        int status = 0;
        
        for (int i = 0; i < strlen(pbuf); i++)
        {
            NSData * data = [NSData dataWithBytes:(pbuf+i) length:1];
            if (port == -1)
            {
                status = (int)[phippo writeSerialData:data andError:&myError];
            }
            else
            {
                status = (int)[phippo writeHippoDataToPort:[NSNumber numberWithInt:port] andData:data andError:&myError];
            }
            usleep(m_writeInterval);
        }
        
        return status;
    }
}

int NanoHippoDev::WriteBytes(int port,unsigned char * ucData, int len)
{
    if (!isOpen) return -1;
    
    
    _log_file_timestamp(port,[NSString stringWithFormat:@"\n[SendCmd]:%s",ucData]);
    
    NSError * myError = nil;

    if (m_writeInterval == 0)
    {
        if (port == -1) return (int)[phippo writeSerialData:[NSData dataWithBytes:(void *)ucData length:len] andError:&myError];
        
        return (int)[phippo writeHippoDataToPort:[NSNumber numberWithInt:port] andData:[NSData dataWithBytes:(void *)ucData length:len] andError:&myError];
    }
    
    
    int status = 0;
    
   
    for (int i = 0; i < len; i++)
    {
        NSData * data = [NSData dataWithBytes:(ucData+i) length:1];
        if (port == -1)
        {
            status = (int)[phippo writeSerialData:data andError:&myError];
        }
        else
        {
            status = (int)[phippo writeHippoDataToPort:[NSNumber numberWithInt:port] andData:data andError:&myError];
        }
        usleep(m_writeInterval);
    }
    return status;
}


int NanoHippoDev::WriteStringBytes(int port,const char * szData)
{
    if (!isOpen) return -1;
    
    if(szData == NULL) return -1;
    if(strlen(szData)<=0) return -2;
    NSArray * arr = [[NSString stringWithUTF8String:szData] componentsSeparatedByString:@","];
    if([arr count]< 1) return -3;
    int size = (int)[arr count];
    unsigned char * ucData = new unsigned char [size];
    for(int i=0; i<size; i++)
    {
        NSScanner * scanner = [NSScanner scannerWithString:[arr objectAtIndex:i]];
        unsigned int tmp;
        [scanner scanHexInt:&tmp];
        ucData[i] = tmp;
    }
    
   return WriteBytes(port,ucData, size);
}




NSData * NanoHippoDev::GetDataBuff(int port)
{
    NSData * data;
    
    if (port >= 0)
    {
        @synchronized(m_hippoDataBuf)
        {
            data = [NSData dataWithData:m_hippoDataBuf];
            if (data && [data length] > 0)
            {
                [m_hippoDataBuf replaceBytesInRange:NSMakeRange(0, [m_hippoDataBuf length]) withBytes:NULL length:0];
            }
            else
            {
                return nil;
            }
        }

    }
    else if (port == -1)
    {
        @synchronized (m_serialDataBuf)
        {
            data = [NSData dataWithData:m_serialDataBuf];
            [m_serialDataBuf resetBytesInRange:NSMakeRange(0, [m_serialDataBuf length])];
            [m_serialDataBuf setLength:0];
        }
    }
    
    return data;
}

NSString * NanoHippoDev::ConvertDataToStr(NSData * data)
{
    NSMutableString * m_reT;
    //NSMutableData * mutdata = nil;
    if (data == nil || [data length] == 0)
    {
        return @"";
    }
    
    if (bFilterUnreadable)
    {
        //mutdata = [[NSMutableData alloc]init];
        unsigned char* dByte = (unsigned char*)data.bytes;
        std::vector<unsigned char> byteData;
        for (int i=0; i<data.length; i++)
        {
            if (dByte[i] != '\0'){
                if(dByte[i] == '\r' || dByte[i] == '\n' || (dByte[i] >= 32))
                {
                    if(dByte[i] >= 127){
                        continue;
                    }
                    byteData.push_back(dByte[i]);
                    
                }
            }
        }
        m_reT = [[NSMutableString alloc] initWithBytes:byteData.data() length:byteData.size() encoding:NSASCIIStringEncoding] ;
    }
    else
    {
        m_reT = [[NSMutableString alloc] initWithBytes:data.bytes length:data.length encoding:NSASCIIStringEncoding] ;
    }
    
    if (bFilterColorCode) {
        NSArray * arrColorCode = [NSArray arrayWithObjects:
                                  @"[0m",
                                  @"[1m",
                                  @"[4m",
                                  @"[5m",
                                  @"[7m",
                                  @"[8m",
                                  @"[30m",
                                  @"[31m",
                                  @"[32m",
                                  @"[33m",
                                  @"[34m",
                                  @"[35m",
                                  @"[36m",
                                  @"[37m",
                                  @"[40m",
                                  @"[41m",
                                  @"[42m",
                                  @"[43m",
                                  @"[44m",
                                  @"[45m",
                                  @"[46m",
                                  @"[47m",
                                  @"[nA",
                                  @"[nB",
                                  @"[nC",
                                  @"[nD",
                                  @"[25;01H",
                                  @"[2J",
                                  @"[K",
                                  @"[s",
                                  @"[u",
                                  @"[?25l",
                                  @"[?25h",
                                  @"............ .E.. ..... .......... ; ;. ..zl",
                                  @"............ .E.. ..... .......... ; ;. ..zj",
                                  @"............ .E.. ..... .......... ; ;. ..zk",
                                  nil];
        
        for (NSString *line in arrColorCode) {
            NSRange range = [m_reT rangeOfString:line];
            if (range.location!=NSNotFound) {
                NSArray * Array = [m_reT componentsSeparatedByString:line];
                [m_reT setString:@""];
                for (NSString *cont in Array) {
                    [m_reT appendString:cont];
                }
            }
        }
    }
    
    NSString * str = [NSString stringWithString:m_reT];
    
    [m_reT setString:@""];
    [m_reT release];
    return str;
}


const char * NanoHippoDev::ReadString(int port)
{
    NSData * data = GetDataBuff(port);
    
    if (!data || [data length] == 0)
    {
        return NULL;
    }
    
    NSString *str = ConvertDataToStr(data);
    [data release];

    return [str UTF8String];
}

const char * NanoHippoDev::ReadBytes(int port)
{
    NSData *data = GetDataBuff(port);
    
    if(data && [data length] > 0)
    {
        return (const char*)[data bytes];
    }
    else
        return NULL;
}

const char *  NanoHippoDev::ReadStringBytes(int port)
{
    NSData *data = GetDataBuff(port);
    NSMutableString *str = [NSMutableString stringWithUTF8String:""];

    if(data && [data length] > 0)
    {
        Byte * pByte = (Byte*)[data bytes];
        for(int i= 0; i<[data length]-1; i++)
        {
            [str appendFormat:@"0x%02X,",pByte[i]];
        }
        [str appendFormat:@"0x%02X",pByte[[data length] -1]] ;
        return [str UTF8String];
    }
    else
        return NULL;
    
}

const char * NanoHippoDev::ReadChannels()
{
    NSMutableString * str;
    long i = 0;
    for (NSNumber * num in m_channel)
    {
        [str appendString:[num stringValue]];
        if (i < m_channel.count - 1) [str appendString:@","];
        i++;
    }
    return [str UTF8String];
}

const char * NanoHippoDev::GetDetectString()
{
    NSLog(@"Get detect string%@",m_MutableDetect);
    return [m_MutableDetect UTF8String];
}

void NanoHippoDev::ClearBuffer(int port)
{
    if (port == -1)
    {
        @synchronized (m_serialDataBuf) {
            [m_serialDataBuf resetBytesInRange:NSMakeRange(0, [m_serialDataBuf length])];
            [m_serialDataBuf setLength:0];
        }
    }
    else
    {
        @synchronized (m_hippoDataBuf) {
            [m_hippoDataBuf replaceBytesInRange:NSMakeRange(0, [m_hippoDataBuf length]) withBytes:NULL length:0];

            [m_channel removeAllObjects];
        }
    }
}

int NanoHippoDev::IsDataReady(int port)
{
    @synchronized (m_hippoDataBuf) {
        if ([m_hippoDataBuf length] > 0) {
            return 0;
        } else {
            return -1;
        }
    }
}

int NanoHippoDev::SetDetectString(const char* det)
{
    std::string strDetect = std::string(det);
    [m_MutableDetect setString:[NSString stringWithFormat:@"%s",strDetect.c_str()]];
    
    return 0;
}

int NanoHippoDev::WaitDetect(int port, int timeout)
{
    int r = -1;
//    NSLog(@" * * * * * \ndylib Detect :%@ * * * * * port:%d timeout:%d \n",m_MutableDetect,port,timeout);
    NSTimeInterval starttime = [[NSDate date]timeIntervalSince1970];
    double tm = (double)timeout/1000.0;
    while (1)
    {
        if (!isOpen) break;
        
        NSString *str = nil;
        if (port == -1)
        {
            @synchronized (m_serialDataBuf)
            {
                str = [[NSString alloc] initWithBytes:m_serialDataBuf.bytes length:m_serialDataBuf.length encoding:NSASCIIStringEncoding];
            }
        }
        else
        {

            @synchronized(m_hippoDataBuf)
            {
                NSData *  tmpData = [NSData dataWithData:m_hippoDataBuf];
                if (tmpData && [tmpData length] > 0)
                {
                    str = ConvertDataToStr(tmpData);
                    [tmpData release];
                    NSRange range  = [str rangeOfString:m_MutableDetect];
                    if (range.location != NSNotFound)
                    {
                        r = 0;
                        [str release];
                        break;
                    }
                }
            }

        }
    
    
        NSTimeInterval now = [[NSDate date]timeIntervalSince1970];
        if ((now-starttime)>=tm)
        {
            r = -2;
            NSLog(@" * * * * * \ndylib Detect :%@ no matched",m_MutableDetect);
            [str release];
            break;
        }

        if (str) [str release];
        [NSThread sleepForTimeInterval:0.01];
    }
    
    return r;  //cancel
}



int NanoHippoDev::SetLogFile(int port, char*path)
{
    if (port == -1)
    {
        [m_defaultLogFile setString:[NSString stringWithUTF8String:path]];
    }
    else
    {
        printf("SetLogFile %d %s\n",port,path);
        m_logFile[port]=std::string(path);
    }
    
    
    printf("SetLogFile %d %s\n",port,m_logFile[port].c_str());
    
    return 0;
}

void NanoHippoDev::SetAppendBufTimeStamp(bool flag)
{
    bAppendBufTimeStamp = flag;
}

void NanoHippoDev::SetFilterColorCode(bool flag)
{
    bFilterColorCode = flag;
}

void NanoHippoDev::SetFilterUnreadable(bool flag)
{
    bFilterUnreadable = flag;
}



//Request CallBack cmd format: [port num]cmd
void * NanoHippoDev::OnRequest(void *pdata, long len)
{
    pthread_mutex_lock(&m_mutex);
    
    NSString *substringForCmdPrefix;
    NSError *error;
    NSString * rData = [[NSString alloc] initWithBytes:pdata length:len encoding:NSUTF8StringEncoding];
    NSRegularExpression *regex = [NSRegularExpression regularExpressionWithPattern:@"\\[([\\-0-9]+)\\]"
                                                                           options:NSRegularExpressionCaseInsensitive
                                                                             error:&error];
    
    NSRange rangeOfCmdPrefix = [regex rangeOfFirstMatchInString:rData options:0 range:NSMakeRange(0, [rData length])];
    
    if (!NSEqualRanges(rangeOfCmdPrefix, NSMakeRange(NSNotFound, 0))&& rangeOfCmdPrefix.location == 0) {
        substringForCmdPrefix = [rData substringWithRange:rangeOfCmdPrefix];
        int port = [[substringForCmdPrefix substringWithRange:NSMakeRange(1, [substringForCmdPrefix length]-2)]intValue];
        int err = WriteString(port, [[rData stringByReplacingCharactersInRange:NSMakeRange(0, rangeOfCmdPrefix.length) withString:@""]UTF8String]);
        NSLog(@"CSocketDevice::OnRequest data:%d data:%@",port,[rData stringByReplacingCharactersInRange:NSMakeRange(0, rangeOfCmdPrefix.length) withString:@""]);
#if NANO
        CReplier::SendStrig((err>=0)?"OK":"Failed,Write to dut failed.please check connection");    //feed back to requester.
#endif
    }
    
    [rData release];
    pthread_mutex_unlock(&m_mutex);
    return nullptr;
}


#pragma mark Write Pass ControlBit
static int __GetHash(Byte ucpNonce[20],Byte hash[20],int stationid)
{
    int status=0;
    [g_LockCB lock];
    status =  get_station_hash(stationid, ucpNonce, hash);
    [g_LockCB unlock];
    return status;
}

int NanoHippoDev::WritePassControlBit(int port, int stationid,char * szCmd)
{
    ReadString(port);
    SetDetectString((char*)":-)");
    int ret = 0;
    ret = WriteString(port,(char*)"getnonce\n");
    if (ret == -1) {
        return -4;//WriteString fail,NanoHippo port was closed
    }
    WaitDetect(port,5000*2);
    
    NSData * databuf = GetDataBuff(port);
    ClearBuffer(port);
    NSString * noncestr = ConvertDataToStr(databuf);
    NSLog(@"Get nonce result: %@",noncestr);
    
    if (databuf == nil || [databuf length]!=55) return -1;//failed to get nonce 55+16*4
    
    Byte *byte = (Byte *)[databuf bytes] ;
    if (byte == NULL) return -101;
    unsigned char ucpNonce[20];
    unsigned char hash[20];
    memset(ucpNonce, 0, sizeof(ucpNonce));
    memset(hash, 0, sizeof(hash));
    memcpy(ucpNonce, byte+10, 20);
    printf("\n start getnonce 20 bytes") ;
    NSMutableString * str = [NSMutableString string];
    for(int i=0 ;i<20 ;i++)
    {
        [str appendFormat:@"%02X,",ucpNonce[i]] ;
        printf("%d\r\n",ucpNonce[i]) ;
    }
    
    
    printf("- - - - - Nounce 20 Byte Hex - - - - - - - -\r\n");
    printf("Nonce:%s\r\n",[str UTF8String]);
    printf("- - - - - Nounce 20 Byte Hex - - - - - - - -\r\n");
    int status  = 0;
    status = __GetHash(ucpNonce, hash,stationid);
    if(status != 0) return -2;//failed to get hash
    
    [str setString:@""];
    for(int i=0 ;i<20 ;i++)
    {
        [str appendFormat:@"%02X,",hash[i]] ;
    }
    printf("Hash: %s",[str UTF8String]);
    
    
    
    SetDetectString(const_cast<char *>(">"));
    WriteString(port,szCmd);
    WaitDetect(port,5000);
    if (ReadString(port) == NULL)
    {
        ClearBuffer(port);
        return -3;//failed to send cbwrite
    }
    ClearBuffer(port);
    usleep(100000);
    
    //just for debug
    SetDetectString((char*)":-)");
    WriteBytes(port,hash, sizeof(hash));
    this->WaitDetect(port,5000*2);
    usleep(500*1000);
    const char* szRtn = ReadString(port);
    ClearBuffer(port);
    if(szRtn){
        if (strstr(szRtn, "Passed") != NULL) return 0;
    }
    return -5;
}

#include "pytest.m"



