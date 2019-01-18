//
//  ZMQReqRep.cpp
//  ZMQX
//
//  Created by Liang on 15-7-9.
//  Copyright (c) 2015年 Liang. All rights reserved.
//

#include "ZMQReqRep.h"
#include <string>
#include <unistd.h>
#include "zmq.h"
#include "zhelpers.h"


ZMQReqRep::ZMQReqRep(int port, const char* host_ip,const char* type)
{
    m_zmq_context = NULL;
    
    m_id = NULL;
    m_socket_type = NULL;
    m_host_ip = NULL;
    m_port = 0;
    m_timeout = 0;
    if (type) {
        m_socket_type = new char[strlen(type)+1];
        strcpy(m_socket_type, type);
    }
    if (host_ip) {
        m_host_ip = new char[strlen(host_ip)+1];
        strcpy(m_host_ip, host_ip);
    }
    m_port = port;
    m_socket_req = NULL;
    m_zmq_context = zmq_ctx_new();
    if (m_zmq_context)
    {
        std::string str_socket_type = m_socket_type;
        if (str_socket_type.compare(ZMQX_CLIENT) == 0){
            init_req_sock();
        }
        else
        {
            std::cout << "zmqx::zmqx specified socket type is not supported.\n";
            return;
        }
    }
    else
    {
        std::cout << "zmqx::zmqx failed to create zmq context.\n";
        return;
    }
}

ZMQReqRep::~ZMQReqRep()
{
    if (m_socket_type) {
        delete m_socket_type;
    }
    zmq_close(m_socket_req);
    zmq_ctx_destroy(m_zmq_context);
}


void ZMQReqRep::init_req_sock()
{
    m_socket_req = zmq_socket (m_zmq_context, ZMQ_REQ);
    if (m_socket_req == NULL) {
        std::cout << "zmqx::zmqx failed to create ZMQ_REQ client socket.\n";
        return ;
    }
    
    char szBuf[128];
    memset(szBuf, 0, sizeof(szBuf));
    sprintf(szBuf, "tcp://%s:%d",m_host_ip, m_port);
    if (zmq_connect (m_socket_req, szBuf) < 0) {
        std::cout << "zmqx::zmqx failed to connect to address " << szBuf << " for ZMQ_REQ socket.\n";
        return ;
    }

}

void ZMQReqRep::send(void* buffer, unsigned long len)
{
    if (m_socket_req) {
        errno = 0;
        if (buffer) {
            if (zmq_send(m_socket_req, buffer, len, 0) < 0) {
                std::cout << "zmqw::sub_send failed to receive message with error:" << zmq_strerror(errno) << "\n";
            }
        }
    }
}

void ZMQReqRep::receive(void* buffer, unsigned long len)
{
    if (m_socket_req) {
        if (buffer) {
            zmq_recv(m_socket_req, buffer, len, 0);
        }
    }
}
