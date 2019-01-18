//
//  NanoHippoDev.h
//  socket_udp
//
//  Created by AustinShih on 1/12/16.
//  Copyright © 2016年 AustinShih. All rights reserved.
//


#ifndef NanoHippoDev_h
#define NanoHippoDev_h


#import <Foundation/Foundation.h>
#include <stdio.h>
#include <string.h>
#import <pthread.h>
#import <map>
#include <atomic>


#define NANO 1
#if NANO
#include "mq/zmq/Publisher.hpp"
#include "mq/zmq/Replier.hpp"
#endif

//#import <ATDeviceElements/ATDeviceElements.h>


#if NANO
class NanoHippoDev : CPubliser, CReplier//, CDataQ
#else
class NanoHippoDev
#endif
{
public:
    NanoHippoDev();
    ~NanoHippoDev();
    
public:
    //port=-1 for serial others for hippo;
    int CreatePub(const char *publish,int port);
    int CreateRep(const char *reply);
    int Open(const char * serialdev);
    int Close();
    int CloseZMQ();
    int SetPubOpt(int needPub);
    
    
    //set write wait micro sec per byte
    int SetWriteTimeInterval(unsigned int usleeps);
    int WriteString(int port,const char* pbuf);
    int WriteBytes(int port,unsigned char * ucData, int len);
    int WriteStringBytes(int port,const char * szData);
    
    const char * ReadString(int port);
    const char * ReadBytes(int port);
    const char * ReadStringBytes(int port);
    const char * ReadChannels();
    const char * GetDetectString();
    void ClearBuffer(int port);
    int SetDetectString(const char* det);
    int WaitDetect(int port, int timeout);  //msec
    int IsDataReady(int port);
    
    //port=-1 for default log file
    int SetLogFile(int port,  char*path);

    void SetAppendBufTimeStamp(bool flag);
    void SetFilterColorCode(bool flag);
    void SetFilterUnreadable(bool flag);
    int  WritePassControlBit(int port, int stationid,char * szCmd);
    void Log_file_timestamp(int port,char *str);
    

    NSData *GetDataBuff(int port);
    NSString * ConvertDataToStr(NSData * data);
    NSString * LocalTimeStampStr();
    void _log_file_timestamp(int port,NSString *str);
    void _log_smc_file(int port, NSString *string);
    
    bool m_bPotassiumFlag;
protected:
    virtual void * OnRequest(void * pdata, long len);
    static void * Init(void * arg);
    
  
private:
    bool bNeedPub;
    bool bFilterUnreadable;
    bool bFilterColorCode;
    bool bAppendBufTimeStamp;
 
    
    char m_serialdev[1024];
    
    unsigned int m_writeInterval;
    
    std::map<int,bool> m_bAppendLogTimeStamp;
#if NANO
    std::map<int,CPubliser *> m_Pub;
#endif
    std::map<int,std::string> m_logFile;
    
    char * cstrLogMainSeven;
    char * cstrLogMainNine;
    NSMutableString * m_defaultLogFile;
    pthread_t m_thread;
    
public:
    std::atomic<bool> isOpen;
    std::atomic<bool> isThreadExit;
    pthread_mutex_t m_mutex;
    NSMutableString * m_MutableDetect;
    
    NSMutableData * m_serialDataBuf;
    NSMutableData * m_hippoDataBuf;
    NSData *m_returnData;
    
    NSMutableDictionary * m_hippoDataArrayByPort;
    NSMutableArray  * m_channel;


    
    
   
};

#endif /* NanoHippoDev_h */

