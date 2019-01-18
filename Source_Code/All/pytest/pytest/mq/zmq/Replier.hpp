//
//  Replier.hpp
//  SocketDev
//
//  Created by Ryan on 12/5/15.


#ifndef Replier_hpp
#define Replier_hpp

#include <stdio.h>
#include "zmq.h"
#include <pthread.h>

typedef void * (*ReplayCallBack)(void * buf,long len,void * context);
class CReplier {
public:
    CReplier();
    virtual ~CReplier();
    
public:
    virtual int connect(const char * address);
    virtual int bind(const char * address);
    virtual int close();
    
    virtual int SetCallBack(ReplayCallBack cb,void * ctx);
    
    virtual void * OnRequest(void *pdata,long len);
protected:
    
    int Send(void * data,long len);
    int SendStrig(const char * buffer);
    
    static void * threadEntry(void * arg);
    bool m_bMonitorReply;
    void * m_context;
    void * m_socket;
    pthread_t m_thread;
    
    ReplayCallBack m_pCallBack;
    void * m_pCBcontext;
};

#endif /* Replier_hpp */
