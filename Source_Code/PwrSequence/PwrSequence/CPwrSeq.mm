//
//  CPwrSeq.m
//  PwrSequence
//
//  Created by AustinShih on 23/11/16.
//  Copyright © 2016年 AustinShih. All rights reserved.
//

#import "CPwrSeq.h"

#define PORT_BASE 0


CPWRSEQ::CPWRSEQ()
{
    client = [[[PwrClient alloc]init]retain];
    mId = 0;
    saveAllData = false;
    strcpy(libName, "NULL");
}

CPWRSEQ::CPWRSEQ(int mid)
{
    client = [[[PwrClient alloc]init]retain];
    mId = mid;
    strcpy(libName, "NULL");
    saveAllData = false;
}

CPWRSEQ::CPWRSEQ(int mid, const char* name)
{
    mId = mid;
    client = [[[PwrClient alloc]init]retain];
    strcpy(libName, name);
    saveAllData = false;
}

CPWRSEQ::~CPWRSEQ()
{
    if (client) {
        [client disconnect];
        [client release];
    }
}

int CPWRSEQ::ConnectClient()
{
    return [client connect];
}

int CPWRSEQ::DisconnectClient()
{
    return [client disconnect];
}

int CPWRSEQ::CreateTCPClient(const char* name, const char* ip, short port)
{
    if (port < PORT_BASE || (int)port > 32768) {
        return -1;
    }
    client = (PwrClient*)[[PwrClient alloc]initWithIPPort:[NSString stringWithUTF8String:name] :[NSString stringWithUTF8String:ip] :port];
    return [client getConnectState];
}

int CPWRSEQ::CreatZmqPub(const char* address, int writeLog)
{
    if (client) {
        return [client initZmqPub:address :writeLog];
    }
    return -1;
}

int CPWRSEQ::CreatZmqPub_BKLT(const char* address, int writeLog)
{
    if (client) {
        return [client initZmqPub_BKLT:address :writeLog];
    }
    return -1;
}

int CPWRSEQ::startDataLogger(const char* logPath,int flag)
{
    //NSLog(@"lua in: %s",logPath);
    NSString* filePath = [NSString stringWithFormat:@"%s",logPath];
    [client clearDataLast];
    
    if (flag == 1 or client.m_channels > 0) {  //Power sequence
        if (saveAllData>0) {
//            NSString* str = [filePath stringByDeletingPathExtension];
//            filePath = [NSString stringWithFormat:@"%@_PS_DATA.csv",str];
            NSLog(@"startDataLogger filePath:%@",filePath);
            client.dataFilePath = filePath;
            if (![[NSFileManager defaultManager]fileExistsAtPath:filePath]) {
                [[NSFileManager defaultManager]createFileAtPath:filePath contents:nil attributes:nil];
               
            }
            
//            NSString* str = [filePath stringByDeletingPathExtension];
//            filePath = [NSString stringWithFormat:@"%@_PS_BYTE.txt",str];
//            client.byteFilePath = filePath;
//            if (![[NSFileManager defaultManager]fileExistsAtPath:filePath]) {
//                [[NSFileManager defaultManager]createFileAtPath:filePath contents:nil attributes:nil];
//            }
            
        }
    }else{   //Backlight
        if (saveAllData>0) {
            NSString* str = [filePath stringByDeletingPathExtension];
            filePath = [NSString stringWithFormat:@"%@_BL_DATA.csv",str];
            if (![[NSFileManager defaultManager]fileExistsAtPath:filePath]) {
                [[NSFileManager defaultManager]createFileAtPath:filePath contents:nil attributes:nil];
                client.dataFilePath = filePath;
            }
//            filePath = [NSString stringWithFormat:@"%@_BL_BYTE.csv",str];
//            if (![[NSFileManager defaultManager]fileExistsAtPath:filePath]) {
//                [[NSFileManager defaultManager]createFileAtPath:filePath contents:nil attributes:nil];
//                client.byteFilePath = filePath;
//            }
        }
    }
    
    [client StartDL:flag];
    return 0;
}

int CPWRSEQ::stopDataLogger(int flag)
{
    [client StopDL:flag];
    return 0;
}

void CPWRSEQ::updateConfig(const char * config, int flag, int configID)
{
    if (client) {
        saveAllData = (flag>0);
        [client updateConfig:config :flag :configID];
    }
}

void CPWRSEQ::setPwrSeqChannel(int ch)
{
    return [client setPwrSeqChannel:ch];
}

int CPWRSEQ::getPwrSeqChannel()
{
    return [client getPwrSeqChannel];
}

void CPWRSEQ::ResetTimeStamp()
{
    [client resetTimeStamp];
}

