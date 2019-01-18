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

#include <string>

typedef void * (*ReplayCallBack)(void * buf,long len,void * context);
class CSubscriber {
public:
    CSubscriber();
    virtual ~CSubscriber();
    
public:
    virtual int connect(const char * address);
    virtual int bind(const char * address);
    virtual int close();
    
    virtual int SetFilter(const char * filter);
    virtual int SetCallBack(ReplayCallBack cb,void * ctx);
    
    virtual void * OnSubscriberData(void *pdata,long len);
protected:
    static void * threadEntry(void * arg);
    bool m_bMonitorSubscrib;
    void * m_context;
    void * m_socket;
    pthread_t m_thread;
    
    ReplayCallBack m_pCallBack;
    void * m_pCBcontext;
    std::string m_strFilter;
};

#endif /* Replier_hpp */
