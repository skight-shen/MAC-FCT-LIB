//
//  ZMQReqRep.h
//  ZMQX
//
//  Created by Liang on 15-7-9.
//  Copyright (c) 2015年 Liang. All rights reserved.
//

#ifndef __ZMQX__ZMQReqRep__
#define __ZMQX__ZMQReqRep__

#include <iostream>
#include <thread>

#define ZMQX_SERVER   "Server"
#define ZMQX_CLIENT   "Client"

class ZMQReqRep
{
public:
    
    ZMQReqRep(int port, const char* host_ip="127.0.0.1", const char* type=ZMQX_CLIENT);
    ~ZMQReqRep();
    void send(void* buffer, unsigned long len);
    void receive(void* buffer, unsigned long len);
    
    
protected:
    void* m_zmq_context;
    
private:
    char* m_id;
    char* m_socket_type;
    int m_port;
    int m_timeout;
    char* m_host_ip;
    void* m_socket_req;
    
    void init_req_sock();
};


#endif /* defined(__ZMQX__ZMQReqRep__) */
