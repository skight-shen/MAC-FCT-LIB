//
//  Replier.cpp
//  SocketDev
//
//  Created by Ryan on 12/5/15.


#include "Subscriber.hpp"

#include <iostream>
#include <unistd.h>

#include <vector>
#define CLI_CR_RED          "\033[31m"
#define CLI_CR_YELLOW       "\033[33m"
#define CLI_CR_CLOSE        "\033[0m"

CSubscriber::CSubscriber()
{
    m_pCallBack = nullptr;
    m_pCBcontext = nullptr;
    
    m_bMonitorSubscrib =true;
    
    m_context = nullptr;
    m_socket = nullptr;
}

CSubscriber::~CSubscriber()
{
    close();
}

int CSubscriber::close()
{
    m_bMonitorSubscrib = false;
    //pthread_cancel(m_thread);
    pthread_join(m_thread, nullptr);
    int l = 0;
    zmq_setsockopt(m_socket, ZMQ_LINGER, &l, sizeof(l));
    zmq_close(m_socket);
    //zmq_term(m_context);
    zmq_ctx_destroy(m_context);
    
    return 0;
}

int CSubscriber::connect(const char *address)
{
    m_context = zmq_ctx_new();
    
    if (!m_context) {
        std::cerr<<CLI_CR_RED<<"[Subscriber] "<< "CSubscriber::failed to create context! with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return -1;
    }
    
    m_socket = zmq_socket(m_context, ZMQ_SUB);
    
    
    if (!m_socket) {
        std::cerr<<CLI_CR_RED<<"[Subscriber] " << "CSubscriber::failed to create subscriber socket! with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return -2;
    }
    
    int ret = zmq_setsockopt(m_socket, ZMQ_SUBSCRIBE, m_strFilter.c_str(), m_strFilter.length());
    if (ret !=0) {
        std::cerr<<CLI_CR_RED<<"[Subscriber] " << "CSubscriber::failed to set subscriber filter! with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return -3;
    }
    
    ret = zmq_connect(m_socket, address);
    if (ret <0) {
        std::cerr<<CLI_CR_RED<<"[Subscriber] " << "CSubscriber::Subscriber socket failed to connect port number :"<<address<<" with return value :"<<ret<<"with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return ret;
    }
    else
    {
        std::cout<<"[Replier] "<< "CSubscriber::Create SUBSCRIBER server,connect with address :"<<address<<std::endl;
        m_bMonitorSubscrib = true;
        pthread_create(&m_thread, nullptr, CSubscriber::threadEntry, this);
    }
    
    return 0;
}

int CSubscriber::bind(const char *address)
{
    m_context = zmq_ctx_new();
    
    if (!m_context) {
        std::cerr<<CLI_CR_RED<<"[CSubscriber] "<< "CSubscriber::failed to create context! with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return -1;
    }
    
    m_socket = zmq_socket(m_context, ZMQ_SUB);
    
    if (!m_socket) {
        std::cerr<<CLI_CR_RED<<"[CSubscriber] " << "CSubscriber::failed to create publiser socket! with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return -2;
    }
    
    int ret = zmq_bind(m_socket, address);
    if (ret <0) {
        std::cerr<<CLI_CR_RED<<"[CSubscriber] " << "CSubscriber::Subscriber socket failed to bind port number :"<<address<<" with return value :"<<ret<<"with error :"<<zmq_strerror(zmq_errno())<<std::endl<<CLI_CR_CLOSE;
        return ret;
    }
    else
    {
        std::cout<<"[CSubscriber] "<< "CSubscriber::Create Subscriber server,bind with address :"<<address<<std::endl;
        m_bMonitorSubscrib = true;
        pthread_create(&m_thread, nullptr, CSubscriber::threadEntry, this);
    }
    
    return 0;
}

int CSubscriber::SetCallBack(ReplayCallBack cb, void *ctx)
{
    m_pCallBack = cb;
    m_pCBcontext = ctx;
    return 0;
}

int CSubscriber::SetFilter(const char *filter)
{
    m_strFilter = filter;
    return 0;
}


void * CSubscriber::OnSubscriberData(void *pdata, long len)
{
    if (len>0) {
        if (m_pCallBack) {  //defaule call cb function.
            const char * pret = (const char *)m_pCallBack(pdata,len,m_pCBcontext);
            return (void *)pret;
        }
    }
    else
    {
        //dump out
        std::cout<<"[Replier] Get Data :"<<(const char *)pdata<<std::endl;
    }
    return nullptr;
}

void * CSubscriber::threadEntry(void *arg)
{
    CSubscriber * pThis = (CSubscriber *)arg;
    while (pThis->m_bMonitorSubscrib) {
        pthread_testcancel();
        std::vector<unsigned char> data_buffer;
        data_buffer.clear();
#if 1
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
//                usleep(1000*10);
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
                    data_buffer.push_back(0);   //append 0 char
                    break;
                }
            
                zmq_msg_t part;
                zmq_msg_init(&part);
                zmq_msg_recv(&part, pThis->m_socket, ZMQ_NOBLOCK);
                void * pbuffer = zmq_msg_data(&part);
                size_t len = zmq_msg_size(&part);
            
                data_buffer.push_back('!');//seperator
                data_buffer.push_back('@');
                data_buffer.push_back('#');
                for (int i=0; i<len; i++) {
                    data_buffer.push_back(((unsigned char *)pbuffer)[i]);
                }
                zmq_msg_close(&part);
            }
    #else
            size_t len =0;
            while (1)
            {
                zmq_msg_t message;
                zmq_msg_init (&message);
                zmq_msg_recv (&message, pThis->m_socket, ZMQ_NOBLOCK);
                //  Process the message frame
                void * pbuffer = zmq_msg_data(&message);
                size_t len = zmq_msg_size(&message);
                if (len<=0) {
                    zmq_msg_close(&message);
                    continue;
                }
                for (int i=0; i<len; i++) {
                    data_buffer.push_back(((unsigned char *)pbuffer)[i]);
                }
            
                zmq_msg_close (&message);
                int more;
                size_t more_size = sizeof (more);
                zmq_getsockopt (pThis->m_socket, ZMQ_RCVMORE, &more, &more_size);
                if (!more)
                {
                    data_buffer.push_back(0);
                    break;      //  Last message frame
                }
            }
#endif
            //zmq_msg_close(&msg);
            pThis->OnSubscriberData(&data_buffer[0], data_buffer.size());
        }
    }
    return nullptr;
}
