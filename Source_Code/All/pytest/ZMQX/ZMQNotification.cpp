//
//  ZMQNotification.cpp
//  ZMQX
//
//  Created by Liang on 15-7-9.
//  Copyright (c) 2015年 Liang. All rights reserved.
//

#include "ZMQNotification.h"
#include <string>
#include <unistd.h>
#include "zmq.h"
#include "zhelpers.h"


void recv_thread(void* zmq_notif_obj, message_callback_t on_message_callback);

ZMQNotification::ZMQNotification(const char* type, int port, const char* host_ip)
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
    m_socket_pub = NULL;
    m_socket_sub = NULL;
    
    m_recv_thread = NULL;
    m_recv_buffer_size = 1024*1024;
    m_p_recv_buf = new char[m_recv_buffer_size];
    
    m_ul_send_buf_size = 1024*1024;
    m_p_send_buf = new char[m_ul_send_buf_size];
    
    
    m_zmq_context = zmq_ctx_new();
    if (m_zmq_context)
    {
        std::string str_socket_type = m_socket_type;
        
        if (str_socket_type.compare(ZMQX_POSTER) == 0){
            init_poster_sock();
        }
        else if (str_socket_type.compare(ZMQX_OBSERVER) == 0){
            init_observer_sock();
        }
        else
        {
            std::cout << "zmqw::zmqw specified socket type is not supported.\n";
            return ;
        }
    }
    else
    {
        std::cout << "zmqw::zmqw failed to create zmq context.\n";
        return ;
    }
}

ZMQNotification::~ZMQNotification()
{
    delete m_p_send_buf;
    if (m_recv_thread)
    {
        delete m_recv_thread;
        m_recv_thread = NULL;
    }
    if (m_socket_type) {
        delete m_socket_type;
    }
    zmq_close(m_socket_pub);
    zmq_close(m_socket_sub);
    zmq_ctx_destroy(m_zmq_context);
}

void ZMQNotification::init_poster_sock()
{
    //bind publisher socket
    m_socket_pub = zmq_socket (m_zmq_context, ZMQ_PUB);
    if (m_socket_pub == NULL) {
        std::cout << "zmqw::zmqw failed to create ZMQ_PUB socket.\n";
        return;
    }
    
    char szBuf[128] = {0};
    sprintf(szBuf, "tcp://*:%d", m_port);
    if (zmq_bind (m_socket_pub, szBuf) < 0) {
        std::cout << "zmqw::zmqw failed to bind address " << szBuf << " for ZMQ_PUB socket.\n";
        return;
    }
}
void ZMQNotification::init_observer_sock()
{
    m_socket_sub = zmq_socket (m_zmq_context, ZMQ_SUB);
    if (m_socket_sub == NULL) {
        std::cout << "zmqw::zmqw failed to create ZMQ_SUB socket.\n";
        return;
    }
    
    if(zmq_setsockopt (m_socket_sub, ZMQ_SUBSCRIBE, "", 0) < 0){
        std::cout << "zmqw::zmqw failed to set ZMQ_SUB socket ZMQ_SUBSCRIBE option.\n";
        return ;
    }
    
    //if does not set receiving timeout, zmq_recv function will block current thread.
    //timeout unit:ms
    if (m_timeout > 0) {
        if (zmq_setsockopt(m_socket_sub, ZMQ_RCVTIMEO, &m_timeout, sizeof(m_timeout)) < 0)
        {
            std::cout << "zmqw::zmqw failed to set ZMQ_SUB socket timeout option.\n";
            return ;
        }
    }
    
    //"tcp://127.0.0.1:5561"
    char szBuf[128] = {0};
    sprintf(szBuf, "tcp://%s:%d", m_host_ip, m_port);
    
    if (zmq_connect (m_socket_sub, szBuf) < 0) {
        std::cout << "zmqw::zmqw failed to connect to address " << szBuf << " for ZMQ_SUB socket.\n";
        return;
    }
}

void ZMQNotification::post_notification(notification_msg_t* nf)//for pub
{
    //publish message
    if (nf) {
        if (nf->ulLen > m_ul_send_buf_size) {
            delete m_p_send_buf;
            m_p_send_buf = new char[nf->ulLen+1024];
            m_ul_send_buf_size = nf->ulLen+1024;
        }
        memset(m_p_send_buf, 0, m_ul_send_buf_size);
        char* pnum = (char*)&nf->name;
        memcpy(m_p_send_buf, pnum, sizeof(nf->name));
        pnum = (char*)&nf->ulLen;
        memcpy(m_p_send_buf+sizeof(nf->name), pnum, sizeof(nf->ulLen));
        int offset = sizeof(nf->name)+sizeof(nf->ulLen);
        memcpy(m_p_send_buf + offset, nf->pmsg, 8);
        unsigned long ptr_param = *((unsigned long*)(nf->pmsg+8));
        if (ptr_param > 0) {
            memcpy(m_p_send_buf + offset + 8,(char*)ptr_param, nf->ulLen-8);
        }else
        {
            memset(m_p_send_buf + offset + 8, 0, 8);
        }
        
//        printf("send buffer = %lx\n", (unsigned long)m_p_send_buf);
        
        int r = zmq_send(m_socket_pub, m_p_send_buf, sizeof(nf->name)+nf->ulLen+sizeof(nf->ulLen), 0);
        if (r< 0) {
            std::cout << "zmqw::post_notification failed to send message with error:" << zmq_strerror(errno) << "\n";
        }
    }
}

void ZMQNotification::add_observer(message_callback_t on_message_callback)
{
    if (m_recv_thread == NULL) {
        m_recv_thread = new std::thread(recv_thread, this, on_message_callback);
    }
}

void ZMQNotification::remove_observer()
{
    if (m_recv_thread) {
        delete m_recv_thread;
        m_recv_thread = NULL;
    }
}


void recv_thread(void* zmq_notif_obj, message_callback_t on_message_callback)
{
    ZMQNotification* o = (ZMQNotification*)zmq_notif_obj;
    while (o->m_recv_thread)
    {
        if (o->m_p_recv_buf)
        {
            notification_msg_t nf;
            //o->sub_recv(o->m_p_recv_buf, (int)o->m_recv_buffer_size);
            errno = 0;
            if (zmq_recv(o->m_socket_sub, o->m_p_recv_buf, (int)o->m_recv_buffer_size, 0) < 0) {
                std::cout << "zmq::zmq_recv failed to receive message with error:" << zmq_strerror(errno) << "\n";
            }

            if (*((unsigned long*)&o->m_p_recv_buf[sizeof(nf.name)])>0)
            {
                if ((*((unsigned long*)&o->m_p_recv_buf[sizeof(nf.name)])+sizeof(nf.name)+sizeof(nf.ulLen) > o->m_recv_buffer_size))
                {
                    unsigned long new_size = (*(unsigned long*)&o->m_p_recv_buf[sizeof(nf.name)])+1024;
                    char* pbuf = new char[new_size];
                    memcpy(pbuf, o->m_p_recv_buf, o->m_recv_buffer_size);
                    
                    //o->sub_recv(&pbuf[o->m_recv_buffer_size], int(new_size - o->m_recv_buffer_size));
                    if (zmq_recv(o->m_socket_sub, &pbuf[o->m_recv_buffer_size], (int)(new_size - o->m_recv_buffer_size), 0) < 0) {
                        std::cout << "zmq::zmq_recv failed to receive message with error:" << zmq_strerror(errno) << "\n";
                    }
                    
                    delete[] o->m_p_recv_buf;
                    o->m_recv_buffer_size = new_size;
                    o->m_p_recv_buf = pbuf;
                }
                on_message_callback(o->m_p_recv_buf, (*(unsigned long*)&o->m_p_recv_buf[sizeof(nf.name)]), &o->m_p_recv_buf[sizeof(nf.name) + sizeof(nf.ulLen)]);
            }
            else
            {
                on_message_callback(o->m_p_recv_buf, 0, NULL);
            }
        }
        //usleep(1*1000);
        std::chrono::milliseconds dura(1);
        std::this_thread::sleep_for(dura);
    }
}
