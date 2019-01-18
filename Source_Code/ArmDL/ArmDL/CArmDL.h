
#ifndef __ARMDL__
#define __ARMDL__

#include <iostream>
#include "DLClient.h"

class CArmDL{
public:
    CArmDL();
    CArmDL(int mid);
    CArmDL(int mid, const char * sname);
    ~CArmDL();
public:
    int CreateTCPClient(const char* name, const char* ip, short port);
    int CreatZmqPub(const char * address);
    int SendString(char* szString);
    int SetDetectString(const char* detectString);
    int WaitForString(int timeout);//ms
    int DetectString(char* szDetectString, int iTimeout);
    char* ReadString();
    const char* SendReceive(char* str, int timeout);
    
    const char* getStubData();
    int clearStubData();
    void RemoveTCPClient();
    int getID();
    const char* GetUUID();
    const char* GetModuleName();
    
    int  setLogPath(const char* header,const char* filename);
    int  startDataLogger();
    int  stopDataLogger();
    
    void updateConfig(int channel,float resdiv, float gain, float refVolt, float res, int flag=0, int unitConvert=1);
    void updateCalFactor(int channel,float gain, float offset);
    
    //RMS
    const char * startRMS(int chn);
    const char * endRMS(int chn);
    double getRMS(int chn);
    double getAverage(int chn);
    float getMax(int chn);
    float getMin(int chn);
    unsigned long getCount(int chn);
    
    void setArmChannel(int ch);
    int getArmChannel();

protected:
//    pthread_mutex_t mMutexLock ;
//    pthread_cond_t  mCondLock ;
    DLClient* client;
    int mId;
    char libName[8];
    bool saveAllData;
};




#define EXPORT_C extern "C"
#define DATALOG CArmDL *dev = (CArmDL *)obj ;

EXPORT_C void *createArmDl()
{
    return new CArmDL() ;
}
EXPORT_C void destroyArmdl(void *obj)
{
    DATALOG
    delete dev ;
}
EXPORT_C int CreateTCPClient(void * obj,const char* name, const char* ip, short port)
{
    DATALOG
    return dev->CreateTCPClient(name,ip,port);
}
EXPORT_C int CreatZmqPub(void * obj,const char * address)
{
    DATALOG
    return dev->CreatZmqPub(address);
}

EXPORT_C void setLogPath(void * obj,const char* header,const char* filename)
{
    DATALOG
    dev->setLogPath(header,filename);
}
EXPORT_C int startDataLogger(void * obj)
{
    DATALOG
    return dev->startDataLogger();
}
EXPORT_C int stopDataLogger(void * obj)
{
    DATALOG
    return dev->stopDataLogger();
}
EXPORT_C void updateConfig(void * obj,int channel,float resdiv, float gain, float refVolt, float res, int flag=0, int unitConvert=1)
{
    DATALOG
    dev->updateConfig(channel,resdiv,gain,refVolt,res,flag,unitConvert);
}


#endif /* defined(__ARMDL__) */

