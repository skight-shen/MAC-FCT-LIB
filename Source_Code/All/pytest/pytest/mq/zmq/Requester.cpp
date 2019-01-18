//
//  Requester.cpp
//  DUT
//
//  Created by Ryan on 12/6/15.


#include "Requester.hpp"
#include "zmq.h"
#include <iostream>
#include <unistd.h>

#define CLI_CR_RED          "\033[31m"
#define CLI_CR_YELLOW       "\033[33m"
#define CLI_CR_CLOSE        "\033[0m"

CRequester::CRequester()
{
    m_context = nullptr;
    m_socket = nullptr;
}

CRequester::~CRequester()
{
}

int CRequester::close()
{
    int l = 0;
    zmq_setsockopt(m_socket, ZMQ_LINGER, &l, sizeof(l));
    zmq_close(m_socket);
    //zmq_term(m_context);
    zmq_ctx_destroy(m_context);
    return 0;
}

int CRequester::connect(const char *address)
{
    m_context = zmq_ctx_new();
    
    if (!m_context) {
        std::cerr<<CLI_CR_RED<<"[Requester] "<< "CRequester::failed to create context! with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return -1;
    }
    
    m_socket = zmq_socket(m_context, ZMQ_REQ);
    
    if (!m_socket) {
        std::cerr<<CLI_CR_RED<<"[Requester] " << "CRequester::failed to create requester socket! with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return -2;
    }
    
    int ret = zmq_connect(m_socket, address);
    if (ret <0) {
        std::cerr<<CLI_CR_RED<<"[Requester] " << "CRequester::Request socket failed to bind port number :"<<address<<" with return value :"<<ret<<"with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return ret;
    }
    else
    {
        std::cout<<"[Requester] "<< "CRequester::Create REQUESTER server,bind with address :"<<address<<std::endl;
        usleep(1000*500);   //sleep some time
    }
    
    SetTimeOut();
    return 0;
}

int CRequester::bind(const char *address)
{
    m_context = zmq_ctx_new();
    
    if (!m_context) {
        std::cerr<<CLI_CR_RED<<"[CRequester] "<< "CRequester::failed to create context! with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return -1;
    }
    
    m_socket = zmq_socket(m_context, ZMQ_PUB);
    
    if (!m_socket) {
        std::cerr<<CLI_CR_RED<<"[CRequester] " << "CRequester::failed to create requester socket! with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return -2;
    }
    
    int ret = zmq_bind(m_socket, address);
    if (ret <0) {
        std::cerr<<CLI_CR_RED<<"[CRequester] " << "CRequester::Request socket failed to bind port number :"<<address<<" with return value :"<<ret<<"with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return ret;
    }
    else
    {
        std::cout<<"[CRequester] "<< "CRequester::Create REQUEST server,bind with address :"<<address<<std::endl;
        usleep(1000*500);   //sleep some time
    }
    SetTimeOut();
    return 0;
}

int CRequester::SetTimeOut(int timeout)
{
    return zmq_setsockopt(m_socket, ZMQ_RCVTIMEO, &timeout, sizeof(timeout));
}
int CRequester::Request(void *data, long len,bool bNeedReply)
{
    int ret = zmq_send(m_socket, data, len, 0);
    if (ret<0) {
        return ret;
    }
    if (bNeedReply) {
        char buffer[128];
        long len;
        ret = Recv(buffer, &len);
        std::cout<<"recv:"<<buffer<<std::endl;
    }
    return ret;
}

int CRequester::Recv(void *buffer, long *len)
{
    zmq_msg_t msg;
    zmq_msg_init(&msg);
    int ret = zmq_msg_recv(&msg, m_socket, 0);
    if (ret>=0) {
        void * pbuffer = zmq_msg_data(&msg);
        size_t len = zmq_msg_size(&msg);
        memcpy(buffer, pbuffer, len);
    }
    else{
        std::cout<<"[Requester:] CRequester receive failed:"<<zmq_strerror(zmq_errno())<<std::endl;
    }
    
    zmq_msg_close(&msg);
    return ret;
}

int CRequester::RequestString(const char *str,bool bNeedReply)
{
    return Request((void*)str, strlen(str),bNeedReply);
}
