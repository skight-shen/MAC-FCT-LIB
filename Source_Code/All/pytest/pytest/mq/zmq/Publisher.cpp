//
//  Publisher.cpp
//  SocketDev
//


#include "Publisher.hpp"
#include "zmq.h"
#include <unistd.h>

#include <iostream>
#define CLI_CR_RED          "\033[31m"
#define CLI_CR_YELLOW       "\033[33m"
#define CLI_CR_CLOSE        "\033[0m"

CPubliser::CPubliser()
{
    m_context = nullptr;
    m_socket = nullptr;
}

CPubliser::~CPubliser()
{
}

int CPubliser::close()
{
    int l = 0;
    zmq_setsockopt(m_socket, ZMQ_LINGER, &l, sizeof(l));//fix destroy hungs
    zmq_close(m_socket);
    //zmq_term(m_context);
    zmq_ctx_destroy(m_context);
    return 0;
}

int CPubliser::connect(const char *address)
{
    m_context = zmq_ctx_new();
    
    if (!m_context) {
        std::cerr<<CLI_CR_RED<<"[Publisher] "<< "CPublisher::failed to create context! with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return -1;
    }
    
    m_socket = zmq_socket(m_context, ZMQ_PUB);
    
    if (!m_socket) {
        std::cerr<<CLI_CR_RED<<"[Publisher] " << "CPublisher::failed to create publiser socket! with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return -2;
    }
    
    int ret = zmq_connect(m_socket, address);
    if (ret <0) {
        std::cerr<<CLI_CR_RED<<"[Publisher] " << "CPublisher::Reply socket failed to bind port number :"<<address<<" with return value :"<<ret<<"with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return ret;
    }
    else
    {
        std::cout<<"[Replier] "<< "CPublisher::Create REPLY server,bind with address :"<<address<<std::endl;
        usleep(1000*500);   //sleep some time
    }
    return 0;
}

int CPubliser::bind(const char *address)
{
    m_context = zmq_ctx_new();
    
    if (!m_context) {
        std::cerr<<CLI_CR_RED<<"[Publisher] "<< "CPublisher::failed to create context! with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return -1;
    }
    
    m_socket = zmq_socket(m_context, ZMQ_PUB);
    
    if (!m_socket) {
        std::cerr<<CLI_CR_RED<<"[Publisher] " << "CPublisher::failed to create publiser socket! with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return -2;
    }
    
    int ret = zmq_bind(m_socket, address);
    if (ret <0) {
        std::cerr<<CLI_CR_RED<<"[Publisher] " << "CPublisher::Reply socket failed to bind port number :"<<address<<" with return value :"<<ret<<"with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return ret;
    }
    else
    {
        std::cout<<"[Publisher] "<< "CPublisher::Create REPLY server,bind with address :"<<address<<std::endl;
        usleep(1000*500);   //sleep some time
    }
    return 0;
}

int CPubliser::Pulish(void *data, long len)
{
    return zmq_send(m_socket, data, len, 0);
}

int CPubliser::PulishString(const char *str)
{
    return Pulish((void *)str, strlen(str));
}
