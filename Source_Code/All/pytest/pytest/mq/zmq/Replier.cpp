//
//  Replier.cpp
//  SocketDev
//
//  Created by Ryan on 12/5/15.

#include "Replier.hpp"

#include <iostream>
#include <unistd.h>

#include <vector>
#define CLI_CR_RED          "\033[31m"
#define CLI_CR_YELLOW       "\033[33m"
#define CLI_CR_CLOSE        "\033[0m"

CReplier::CReplier()
{
    m_pCallBack = nullptr;
    m_pCBcontext = nullptr;
    
    m_bMonitorReply =true;
    
    m_context = nullptr;
    m_socket = nullptr;
}

CReplier::~CReplier()
{
    close();
}

int CReplier::close()
{
    m_bMonitorReply = false;
    //pthread_cancel(m_thread);
    pthread_join(m_thread, nullptr);
    int l = 0;
    zmq_setsockopt(m_socket, ZMQ_LINGER, &l, sizeof(l));
    zmq_close(m_socket);
    //zmq_term(m_context);
    zmq_ctx_destroy(m_context);
    
    return 0;
}

int CReplier::connect(const char *address)
{
    m_context = zmq_ctx_new();
    
    if (!m_context) {
        std::cerr<<CLI_CR_RED<<"[Replier] "<< "CReplier::failed to create context! with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return -1;
    }
    
    m_socket = zmq_socket(m_context, ZMQ_REP);
    
    if (!m_socket) {
        std::cerr<<CLI_CR_RED<<"[Replier] " << "CReplier::failed to create publiser socket! with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return -2;
    }
    
    int ret = zmq_connect(m_socket, address);
    if (ret <0) {
        std::cerr<<CLI_CR_RED<<"[Replier] " << "CReplier::Reply socket failed to connect port number :"<<address<<" with return value :"<<ret<<"with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return ret;
    }
    else
    {
        std::cout<<"[Replier] "<< "CReplier::Create REPLY server,connect with address :"<<address<<std::endl;
        m_bMonitorReply = true;
        pthread_create(&m_thread, nullptr, CReplier::threadEntry, this);
        usleep(1000*500);   //sleep some time
    }
    
    return 0;
}

int CReplier::bind(const char *address)
{
    m_context = zmq_ctx_new();
    
    if (!m_context) {
        std::cerr<<CLI_CR_RED<<"[Replier] "<< "CReplier::failed to create context! with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return -1;
    }
    
    m_socket = zmq_socket(m_context, ZMQ_REP);
    
    if (!m_socket) {
        std::cerr<<CLI_CR_RED<<"[Replier] " << "CReplier::failed to create publiser socket! with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return -2;
    }
    
    int ret = zmq_bind(m_socket, address);
    if (ret <0) {
        std::cerr<<CLI_CR_RED<<"[Replier] " << "CReplier::Reply socket failed to bind port number :"<<address<<" with return value :"<<ret<<"with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return ret;
    }
    else
    {
        std::cout<<"[Replier] "<< "CReplier::Create REPLY server,bind with address :"<<address<<std::endl;
        m_bMonitorReply = true;
        pthread_create(&m_thread, nullptr, CReplier::threadEntry, this);
        usleep(1000*500);   //sleep some time
    }
    
    return 0;
}

int CReplier::SetCallBack(ReplayCallBack cb, void *ctx)
{
    m_pCallBack = cb;
    m_pCBcontext = ctx;
    return 0;
}

int CReplier::Send(void *data, long len)
{
    return zmq_send(m_socket, data, len, 0);
}

int CReplier::SendStrig(const char *buffer)
{
    if (!buffer) {
        return -1;
    }
    return Send((void *)buffer, strlen(buffer));
}

void * CReplier::OnRequest(void *pdata, long len)
{
    if (len>0) {
        if (m_pCallBack) {
            const char * pret = (const char *)m_pCallBack(pdata,len,m_pCBcontext);
            SendStrig(pret);  //send back to requester
        }
    }
    else
    {
        //dump out
        std::cout<<"[Replier] Get Data :"<<(const char *)pdata<<std::endl;
    }
    return nullptr;
}

void * CReplier::threadEntry(void *arg)
{
    CReplier * pThis = (CReplier *)arg;
    while (pThis->m_bMonitorReply) {
        pthread_testcancel();
//        usleep(1000*10);
        std::vector<unsigned char> data_buffer;
        data_buffer.clear();

        zmq_pollitem_t pollitem[1];
        pollitem[0].socket = pThis->m_socket;
        pollitem[0].events = ZMQ_POLLIN;

        int rc = zmq_poll(pollitem, 1, 500);
        if(rc>0)
        {
            zmq_msg_t msg;
            zmq_msg_init(&msg);
            zmq_msg_recv(&msg, pThis->m_socket, ZMQ_NOBLOCK);
            void * pbuffer = zmq_msg_data(&msg);
            size_t len = zmq_msg_size(&msg);
//            if (len<=0) {
//                zmq_msg_close(&msg);
//                continue;
//            }

            for (int i=0; i<len; i++) {
                data_buffer.push_back(((unsigned char *)pbuffer)[i]);
            }
            zmq_msg_close(&msg);
        
        
            while (true) {
            //get more data in a frame
                long more;
                size_t more_len=sizeof(more);
                int ret =zmq_getsockopt(pThis->m_socket, ZMQ_RCVMORE, &more, &more_len);
                if (ret<0) {
                    std::cout<<"Get More data failed!"<<zmq_strerror(zmq_errno())<<std::endl;
                    return nullptr;
                }
                if (!more) {    //no more data
                    //data_buffer.push_back(0);
                    break;
                }
            
                zmq_msg_t msg;
                zmq_msg_init(&msg);
                zmq_msg_recv(&msg, pThis->m_socket, ZMQ_NOBLOCK);
                void * pbuffer = zmq_msg_data(&msg);
                size_t len = zmq_msg_size(&msg);
            
                for (int i=0; i<len; i++) {
                    data_buffer.push_back(((unsigned char *)pbuffer)[i]);
                }
                zmq_msg_close(&msg);
            
            }
        
            pThis->OnRequest(&data_buffer[0], data_buffer.size());
        }
    }
    return nullptr;
}
