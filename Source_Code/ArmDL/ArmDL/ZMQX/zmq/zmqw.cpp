//
//  zmqw.cpp
//  testwzm
//
//  Created by Liang on 15-5-9.
//  Copyright (c) 2015年 Liang. All rights reserved.
//

#include "zmqw.hpp"
#include <string>
#include <unistd.h>


using std::string;


#if 0
zmqw::zmqw(const char* szIdentifier)
{
    m_zmq_context = NULL;
    
    m_socket_type = NULL;
    m_port = 0;
    m_timeout = 0;
    m_socket_pub = NULL;
    m_socket_sub = NULL;
    m_socket_pub_rep = NULL;
    m_socket_sub_req = NULL;
    
    m_recv_thread = NULL;
    m_recv_buffer_size = 1024*1024;
    m_p_recv_buf = new char[m_recv_buffer_size];
    
    m_ul_send_buf_size = 1024*1024;
    m_p_send_buf = new char[m_ul_send_buf_size];

    
    int r = parse_identifier(szIdentifier);
    if (r < 0) {
        return;
    }
    m_zmq_context = zmq_ctx_new();
    if (m_zmq_context)
    {
        string str_socket_type = m_socket_type;
        
        if (str_socket_type.compare("pub") == 0)
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
            
            m_socket_pub_rep = zmq_socket (m_zmq_context, ZMQ_REP);
            if (m_socket_pub_rep == NULL) {
                std::cout << "zmqw::zmqw failed to create ZMQ_PUB reply service socket.\n";
                return;
            }
            
            //zmq_bind (m_repService, "tcp://*:5562");
            memset(szBuf, 0, sizeof(szBuf));
            sprintf(szBuf, "tcp://*:%d", m_port + 1);
            if (zmq_bind (m_socket_pub_rep, szBuf) < 0) {
                std::cout << "zmqw::zmqw failed to bind address " << szBuf << "for ZMQ_PUB reply service socket.\n";
                return;
            }
            
        }
        
        else if (str_socket_type.compare("sub") == 0)
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
            sprintf(szBuf, "tcp://127.0.0.1:%d", m_port);
            
            if (zmq_connect (m_socket_sub, szBuf) < 0) {
                std::cout << "zmqw::zmqw failed to connect to address " << szBuf << " for ZMQ_SUB socket.\n";
                return;
            }
            
            m_socket_sub_req = zmq_socket (m_zmq_context, ZMQ_REQ);
            if (m_socket_sub_req == NULL) {
                std::cout << "zmqw::zmqw failed to create ZMQ_SUB request client socket.\n";
                return ;
            }
            
            memset(szBuf, 0, sizeof(szBuf));
            sprintf(szBuf, "tcp://127.0.0.1:%d", m_port + 1);
            if (zmq_connect (m_socket_sub_req, szBuf) < 0) {
                std::cout << "zmqw::zmqw failed to connect to address " << szBuf << " for ZMQ_SUB socket.\n";
                return ;
            }
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
#endif

zmqw::~zmqw()
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
    zmq_close(m_socket_pub_rep);
    zmq_close(m_socket_sub);
    zmq_close(m_socket_sub_req);
    zmq_ctx_destroy(m_zmq_context);
}

int zmqw::pub_send(const char* szMessage)
{
    int r = 0;
    //publish message
    if (szMessage)
    {
        r = zmq_send(m_socket_pub, szMessage, strlen(szMessage), 0);
        if (r < 0) {
            std::cout << "zmqw::pub_send failed to send message with error:" << zmq_strerror(errno) << "\n";
        }else
        {
            r = 0;//success
        }
    }else
    {
        r = -9999;
    }
    return r;
}
int zmqw::pub_recv(char* szBuf, int iLen)
{
    int r = 0;
    
    errno = 0;
    if (szBuf)
    {
        r = zmq_recv(m_socket_pub_rep, szBuf, iLen, 0);
        if (r < 0) {
            std::cout << "zmqw::pub_recv failed to receive message with error:" << zmq_strerror(errno) << "\n";
        }else
        {
            //success
        }
        
        zmq_send(m_socket_pub_rep, "", 0, 0);
    }else
    {
        r = -9999;
    }
    
    return r;
}
int zmqw::sub_recv(char* szBuf, int iLen)
{
    int r = 0;
    
    errno = 0;
    if (szBuf)
    {
        r = zmq_recv(m_socket_sub, szBuf, iLen, 0);
        if (r < 0) {
            std::cout << "zmqw::sub_recv failed to receive message with error:" << zmq_strerror(errno) << "\n";
        }else
        {
            //success
        }
    }else
    {
        r = -9999;
    }

    return r;
}
int zmqw::sub_send(const char* szMessage)
{
    int r = 0;
    
    errno = 0;
    if (szMessage) {
        r = zmq_send(m_socket_sub_req, szMessage, strlen(szMessage), 0);
        if (r < 0) {
            std::cout << "zmqw::sub_send failed to receive message with error:" << zmq_strerror(errno) << "\n";
        }else
        {
            //success
        }
        char szBuffer[4096] = {0};
        zmq_recv(m_socket_sub_req, szBuffer, sizeof(szBuffer), 0);
    }else
    {
         r = -9999;
    }
    
    return r;
}

int zmqw::parse_identifier(const char* szIdentifier)
{
    if (szIdentifier && strlen(szIdentifier)>0) {
        string s = szIdentifier;
        unsigned long index1 = 0;
        unsigned long index2 = 0;
        index1 = s.find(":");
        if (index1 == string::npos) {
            std::cout << "Invalid parameter\n";
            return -1;
        }
        index2 = s.find(":", index1+1);
        if (index2 == string::npos) {
            std::cout << "Invalid parameter\n";
            return -2;
        }
        string s_type = s.substr(0, index1);
        m_socket_type = new char[s_type.length()+1];
        strcpy(m_socket_type, s_type.c_str());
        m_port = atoi(s.substr(index1+1, index2-index1-1).c_str());
        m_timeout = atoi(s.substr(index2+1, s.length()-index2-1).c_str());
        
        if (m_port > 65535) {
            return -3;
        }
        
        std::cout << m_socket_type << "\n";
        std::cout << m_port << "\n";
        std::cout << m_timeout << "\n";
    }else
    {
        return -4;
    }
    return 0;
}









zmqw::zmqw(const char* type, const char* host_ip, int port)
{
    m_zmq_context = NULL;
    
    m_socket_type = NULL;
    m_host_ip = NULL;
    m_port = 0;
    m_timeout = 0;
    
    if (type) {
        if (m_socket_type) {
            delete m_socket_type;
        }
        m_socket_type = new char[strlen(type)+1];
        strcpy(m_socket_type, type);
    }
    
    if (host_ip) {
        if (m_host_ip) {
            delete m_host_ip;
        }
        m_host_ip = new char[strlen(host_ip)+1];
        strcpy(m_host_ip, host_ip);
    }
    
    m_port = port;
    
    
    m_socket_pub = NULL;
    m_socket_sub = NULL;
    m_socket_pub_rep = NULL;
    m_socket_sub_req = NULL;
    
    m_recv_thread = NULL;
    m_recv_buffer_size = 1024*1024;
    m_p_recv_buf = new char[m_recv_buffer_size];
    
    m_ul_send_buf_size = 1024*1024;
    m_p_send_buf = new char[m_ul_send_buf_size];
    

    m_zmq_context = zmq_ctx_new();
    if (m_zmq_context)
    {
        string str_socket_type = m_socket_type;
        
        if (str_socket_type.compare("pub") == 0)
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
            
            m_socket_pub_rep = zmq_socket (m_zmq_context, ZMQ_REP);
            if (m_socket_pub_rep == NULL) {
                std::cout << "zmqw::zmqw failed to create ZMQ_PUB reply service socket.\n";
                return;
            }
            
            //zmq_bind (m_repService, "tcp://*:5562");
            memset(szBuf, 0, sizeof(szBuf));
            sprintf(szBuf, "tcp://*:%d", m_port + 1);
            if (zmq_bind (m_socket_pub_rep, szBuf) < 0) {
                std::cout << "zmqw::zmqw failed to bind address " << szBuf << "for ZMQ_PUB reply service socket.\n";
                return;
            }
            
        }
        
        else if (str_socket_type.compare("sub") == 0)
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
            //sprintf(szBuf, "tcp://127.0.0.1:%d", m_port);
            sprintf(szBuf, "tcp://%s:%d", m_host_ip, m_port);
            
            if (zmq_connect (m_socket_sub, szBuf) < 0) {
                std::cout << "zmqw::zmqw failed to connect to address " << szBuf << " for ZMQ_SUB socket.\n";
                return;
            }
            
            m_socket_sub_req = zmq_socket (m_zmq_context, ZMQ_REQ);
            if (m_socket_sub_req == NULL) {
                std::cout << "zmqw::zmqw failed to create ZMQ_SUB request client socket.\n";
                return ;
            }
            
            memset(szBuf, 0, sizeof(szBuf));
            //sprintf(szBuf, "tcp://127.0.0.1:%d", m_port + 1);
            sprintf(szBuf, "tcp://%s:%d", m_host_ip, m_port + 1);
            if (zmq_connect (m_socket_sub_req, szBuf) < 0) {
                std::cout << "zmqw::zmqw failed to connect to address " << szBuf << " for ZMQ_SUB socket.\n";
                return ;
            }
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

void zmqw::post_notification(notification_msg_t* nf)//for pub
{
    //publish message
    if (nf) {
        if (nf->ulLen > m_ul_send_buf_size) {
            delete m_p_send_buf;
            m_p_send_buf = new char[nf->ulLen+1024];
            m_ul_send_buf_size = nf->ulLen+1024;
        }
        
        char* pnum = (char*)&nf->name;
        memcpy(m_p_send_buf, pnum, sizeof(nf->name));
        pnum = (char*)&nf->ulLen;
        memcpy(m_p_send_buf+sizeof(nf->name), pnum, sizeof(nf->ulLen));
        memcpy(m_p_send_buf+sizeof(nf->name)+sizeof(nf->ulLen), nf->pmsg, nf->ulLen);
        
        int r = zmq_send(m_socket_pub, m_p_send_buf, sizeof(nf->name)+nf->ulLen+sizeof(nf->ulLen), 0);
        if (r< 0) {
            std::cout << "zmqw::post_notification failed to send message with error:" << zmq_strerror(errno) << "\n";
        }
    }
}

void zmqw::add_observer(message_callback_t on_message_callback)
{
    if (m_recv_thread == NULL) {
        m_recv_thread = new std::thread(recv_thread, this, on_message_callback);
    }
}

void zmqw::remove_observer()
{
    if (m_recv_thread) {
        delete m_recv_thread;
        m_recv_thread = NULL;
    }
}


void recv_thread(zmqw* zmqw_obj, message_callback_t on_message_callback)
{
    while (zmqw_obj->m_recv_thread)
    {
        if (zmqw_obj->m_p_recv_buf)
        {
            notification_msg_t nf;
            zmqw_obj->sub_recv(zmqw_obj->m_p_recv_buf, (int)zmqw_obj->m_recv_buffer_size);
            if (*((unsigned long*)&zmqw_obj->m_p_recv_buf[sizeof(nf.name)])>0)
            {
                if ((*((unsigned long*)&zmqw_obj->m_p_recv_buf[sizeof(nf.name)])+sizeof(nf.name)+sizeof(nf.ulLen) > zmqw_obj->m_recv_buffer_size))
                {
                    unsigned long new_size = (*(unsigned long*)&zmqw_obj->m_p_recv_buf[sizeof(nf.name)])+1024;
                    char* pbuf = new char[new_size];
                    memcpy(pbuf, zmqw_obj->m_p_recv_buf, zmqw_obj->m_recv_buffer_size);
                   
                    zmqw_obj->sub_recv(&pbuf[zmqw_obj->m_recv_buffer_size], int(new_size-zmqw_obj->m_recv_buffer_size));
                    
                    delete zmqw_obj->m_p_recv_buf;
                    zmqw_obj->m_recv_buffer_size = new_size;
                    zmqw_obj->m_p_recv_buf = pbuf;
                }
                on_message_callback(zmqw_obj->m_p_recv_buf, (*(unsigned long*)&zmqw_obj->m_p_recv_buf[sizeof(nf.name)]), &zmqw_obj->m_p_recv_buf[sizeof(nf.name) + sizeof(nf.ulLen)]);
            }
            else
            {
                on_message_callback(zmqw_obj->m_p_recv_buf, 0, NULL);
            }
        }
        usleep(1*1000);
    }
}
