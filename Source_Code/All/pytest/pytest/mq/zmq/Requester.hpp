//
//  Requester.hpp
//  DUT
//
//  Created by Ryan on 12/6/15.


#ifndef Requester_hpp
#define Requester_hpp

#include <stdio.h>

class CRequester
{
public:
    CRequester();
    ~CRequester();
public:
    virtual int connect(const char * address);
    virtual int bind(const char * address);
    virtual int close();
    
    virtual int Request(void * data,long len,bool bNeedReply=true);
    virtual int RequestString(const char * str,bool bNeedReply=true);
    virtual int SetTimeOut(int timeout=3000);
    
    int Recv(void * buffer,long * len);
protected:
    void * m_context;
    void * m_socket;
    
};

#endif /* Requester_hpp */
