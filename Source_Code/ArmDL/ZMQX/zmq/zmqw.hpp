//
//  zmqw.h
//  testwzm
//
//  Created by Liang on 15-5-9.
//  Copyright (c) 2015年 Liang. All rights reserved.
//

#ifndef __testwzm__zmqw__
#define __testwzm__zmqw__

#include <iostream>

#include "../zmq.h"
#include "zhelpers.h"
//#include <pthread.h>
#include <thread>

#define NOTIFICATION_NAME_MAX_LENGHT 128

typedef struct {
//    int msg_id;  // id of msg
    char name[NOTIFICATION_NAME_MAX_LENGHT];
    unsigned long ulLen;
    char* pmsg; //
} notification_msg_t;

typedef void* (*message_callback_t)(char* name, unsigned long ullen, void* message);

class zmqw
{
public:
    
    zmqw(const char* type, const char* host_ip, int port);
    ~zmqw();
    void add_observer(message_callback_t on_message_callback);
    void post_notification(notification_msg_t* nf);
    void remove_observer();

    
public:
    std::thread* m_recv_thread;
    unsigned long m_recv_buffer_size;
    char* m_p_recv_buf;
    
protected:
    void* m_zmq_context;
    
private:
    char* m_socket_type;
    int m_port;
    int m_timeout;
    char* m_host_ip;
    
    void* m_socket_pub;
    void* m_socket_sub;
    void* m_socket_pub_rep;
    void* m_socket_sub_req;
    
    
    char* m_p_send_buf;
    unsigned long m_ul_send_buf_size;
    int parse_identifier(const char* szIdentifier);
    
public:
    //zmqw(const char* szIdentifier);
    int pub_send(const char* szMessage);
    int pub_recv(char* szBuf, int iLen);
    int sub_recv(char* szBuf, int iLen);
    int sub_send(const char* szMessage);
};

void recv_thread(zmqw* zmqw_obj, message_callback_t on_message_callback);


#endif /* defined(__testwzm__zmqw__) */
