//
//  CPwrSeq.h
//  PwrSequence
//
//  Created by AustinShih on 23/11/16.
//  Copyright © 2016年 AustinShih. All rights reserved.
//


#ifndef __PWR_SEQ__
#define __PWR_SEQ__

#include <iostream>
#include "PwrClient.h"

class CPWRSEQ{
public:
    CPWRSEQ();
    CPWRSEQ(int mid);
    CPWRSEQ(int mid, const char* name);
    ~CPWRSEQ();
    
public:
    int CreateTCPClient(const char* name, const char* ip, short port);
    int CreatZmqPub(const char* address, int writeLog=0);
    int CreatZmqPub_BKLT(const char* address, int writeLog=0);
    
    int  startDataLogger(const char * logPath, int flag);
    int  stopDataLogger(int flag);
    void updateConfig(const char* config, int flag,int configID);
    
    void setPwrSeqChannel(int ch);
    int getPwrSeqChannel();
    int ConnectClient();
    int DisconnectClient();
    void ResetTimeStamp();

protected:
    PwrClient* client;
    int mId;
    char libName[8];
    bool saveAllData;
};


#define EXPORT_C extern "C"
#define NCPWRSEQ CPWRSEQ *dev = (CPWRSEQ *)obj ;

EXPORT_C void *createCPWRSEQ()
{
    return new CPWRSEQ();
}
EXPORT_C void destroyCPWRSEQ(void *obj)
{
    NCPWRSEQ
    delete dev ;
}
EXPORT_C int CreateTCPClient(void * obj,const char* name, const char* ip, short port)
{
    NCPWRSEQ
    return dev->CreateTCPClient(name,ip,port);
}
EXPORT_C int CreatZmqPub(void * obj,const char * address,int writeLog=0)
{
    NCPWRSEQ
    return dev->CreatZmqPub(address,writeLog);
}

EXPORT_C int startDataLogger(void * obj,const char * logPath, int flag)
{
    NCPWRSEQ
    return dev->startDataLogger(logPath,flag);
}
EXPORT_C int stopDataLogger(void * obj, int flag)
{
    NCPWRSEQ
    return dev->stopDataLogger(flag);
}
EXPORT_C void updateConfig(void * obj,const char* config, int flag,int configID)
{
    NCPWRSEQ
    dev->updateConfig(config,flag,configID);
}

EXPORT_C int ConnectClient(void * obj)
{
    NCPWRSEQ
    return dev->ConnectClient();
}
EXPORT_C int DisconnectClient(void * obj)
{
    NCPWRSEQ
    return dev->DisconnectClient();
}



#endif /* defined(__PWR_SEQ__) */

