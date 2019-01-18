
#include "SocketDevice.h"
#define EXPORT_C extern "C"



#define SDEV CSocketDevice *sdev = (CSocketDevice *)obj ;
EXPORT_C void *createSDev()
{
    return new CSocketDevice() ;
}
EXPORT_C void destroySDev(void *obj)
{
    SDEV
    delete sdev ;
}

EXPORT_C int CreateIPC(void *obj , const char *reply,const char *publiser)
{
    SDEV
    return sdev->CreateIPC(reply,publiser);
}

EXPORT_C int PublishLog(void *obj ,char *data)
{
    SDEV
    return sdev->PublishLog(data);
}

EXPORT_C int Open(void *obj ,const char * name,int port)
{
    SDEV
    return sdev->Open(name,port);
}

EXPORT_C int Close(void *obj )
{
    SDEV
    return sdev->Close();
}
EXPORT_C int SDevWriteString(void *obj,const char * buffer,bool mutilflag = false)
{
    SDEV
    return sdev->WriteString(buffer,mutilflag);
}
EXPORT_C const char * SDevReadString(void *obj)
{
    SDEV
    return sdev->ReadString();
}
EXPORT_C const char * SDevReadString2(void *obj)
{
    SDEV
    return sdev->ReadString2();
}
//
EXPORT_C int SDevSetDetectString(void *obj,const char * det)
{
    SDEV
    return sdev->SetDetectString(det);
}
EXPORT_C int SDevWaitDetect(void *obj,int timeout)
{
    SDEV
    return sdev->WaitDetect(timeout);
}
EXPORT_C void SetHexmode(void *obj,bool mode)
{
    SDEV
    sdev->SetHexmode(mode);
}
EXPORT_C void SDevSetFilterColorCode(void *obj,bool mode)
{
    SDEV
    sdev->SetFilterColorCode(mode);
}

#define TONANOHIPPO NanoHippoDev *dev = (NanoHippoDev *)obj ;
//NanoHippoDev *dev = new NanoHippoDev();
EXPORT_C void *createNanoHippoDev()
{
    return new NanoHippoDev() ;
}
EXPORT_C void destroyNanoHippoDev(void *obj)
{
    TONANOHIPPO
    delete dev ;
}



EXPORT_C int CreatePub(void *obj,const char *publish,int port)
{
    TONANOHIPPO
    return dev->CreatePub(publish,port) ;
}
EXPORT_C int CreateRep(void *obj,const char *reply)
{
    TONANOHIPPO
    return dev->CreateRep(reply) ;
}



EXPORT_C int openSerial(void *obj,const char *serialDev)
{
    TONANOHIPPO
    return dev->Open(serialDev) ;
}
EXPORT_C int closeAll(void *obj)
{
    TONANOHIPPO
    return dev->Close() ;
}
EXPORT_C int SetWriteTimeInterval(void *obj,int usleeps)
{
    TONANOHIPPO
    return dev->SetWriteTimeInterval(usleeps);
}
EXPORT_C int WriteString(void *obj,int port , const char* str )
{
    TONANOHIPPO
    return dev->WriteString(port, str) ;
}
EXPORT_C int WriteBytes(void *obj,int port ,  const char* data , int len)
{
    TONANOHIPPO
    return dev->WriteBytes(port, (unsigned char *)data, len);
}
EXPORT_C int WriteStringBytes(void *obj,int port , const char* str )
{
    TONANOHIPPO
    return dev->WriteString(port, str) ;
}
struct Buffer
{
    NSData *data ;
    NSString *str ;
    NanoHippoDev *dev;
    Buffer(NanoHippoDev *dev , NSData *data) : dev(dev) ,data(data) , str(nil){

    }
    ~Buffer(){
        if(data){
            [data release];
            data = nil;
        }
        if(str){
            [str release];
            str = nil;
        }
    }
};
EXPORT_C void *readBuffer(void *obj,int port)
{
    TONANOHIPPO
    NSData * data = dev->GetDataBuff(port);
    if(data)
        return (void *)(new Buffer(dev, data));
    else
        return 0 ;
}
EXPORT_C const char* getStringFromBuffer(void *buffer)
{
    Buffer *buf = (Buffer *)buffer ;
    if(buf){
        if(buf->str == nil){
            buf->str = buf->dev->ConvertDataToStr(buf->data);
        }
        return [buf->str UTF8String];
    }
    return NULL;
}
EXPORT_C int getBufferLength(void *buffer)
{
    Buffer *buf = (Buffer *)buffer ;
    if(buf){
        return [buf->data length];
    }
    return 0 ;
}
EXPORT_C int getBytesFromBuffer(void *buffer , char* bytes , int length){
    Buffer *buf = (Buffer *)buffer ;
    if(buf){
        if( length < 0 ||  length > [buf->data length] )
            length = [buf->data length];
        memcpy(bytes , [buf->data bytes], length);
        return length;
    }
    return 0 ;
}
EXPORT_C void destroyBuffer(void *buffer)
{
    Buffer *buf = (Buffer *)buffer ;
    if(buf){
        delete buf;
    }
}



EXPORT_C int SetLogFile(void *obj,int nPort, char* cstrPath)
{
    TONANOHIPPO
    return dev->SetLogFile(nPort,cstrPath);
}



EXPORT_C const char * ReadString(void *obj,int nPort)
{
    TONANOHIPPO
    return dev->ReadString(nPort);
}
EXPORT_C const char * ReadChannels(void *obj)
{
    TONANOHIPPO
    return dev->ReadChannels();
}

EXPORT_C void SetFilterColorCode(void *obj,bool flag)
{
    TONANOHIPPO
    dev->SetFilterColorCode(flag);
}
EXPORT_C void SetFilterUnreadable(void *obj,bool flag)
{
    TONANOHIPPO
    dev->SetFilterUnreadable(flag);
}

EXPORT_C const char * GetDetectString(void *obj)
{
    TONANOHIPPO
    return dev->GetDetectString();
}

EXPORT_C void ClearBuffer(void *obj,int port)
{
    TONANOHIPPO
    dev->ClearBuffer(port);
}

EXPORT_C int IsDataReady(void *obj,int port)
{
    TONANOHIPPO
    return  dev->IsDataReady(port);
}

EXPORT_C int SetDetectString(void *obj,const char* det)
{
    TONANOHIPPO
    return dev->SetDetectString(det);
}

EXPORT_C int WaitDetect(void *obj,int port, int timeout)
{
    TONANOHIPPO
    return dev->WaitDetect(port, timeout);
}
EXPORT_C int WritePassControlBit(void *obj,int port, int stationid,char * szCmd)
{
    TONANOHIPPO
    return dev->WritePassControlBit(port, stationid,szCmd);
}




//#include "../CNanohippo.hpp"


