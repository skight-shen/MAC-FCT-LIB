//
//  ZMQNotification.h
//  ZMQX
//
//  Created by Liang on 15-7-9.
//  Copyright (c) 2015年 Liang. All rights reserved.
//

#ifndef __ZMQX__ZMQNotification__
#define __ZMQX__ZMQNotification__

#include <iostream>
#include <thread>

#define NOTIFICATION_NAME_MAX_LENGHT 128
#define ZMQX_POSTER     "Poster"
#define ZMQX_OBSERVER   "Observer"

typedef struct {
    //    int msg_id;  // id of msg
    char name[NOTIFICATION_NAME_MAX_LENGHT];
    unsigned long ulLen;
    char* pmsg; //
} notification_msg_t;

typedef void* (*message_callback_t)(char* name, unsigned long ullen, void* message);

class ZMQNotification
{
public:
    
    ZMQNotification(const char* type, int port, const char* host_ip="127.0.0.1");
    ~ZMQNotification();
    void add_observer(message_callback_t on_message_callback);
    void post_notification(notification_msg_t* nf);
    void remove_observer();
    
    
public:
    std::thread* m_recv_thread;
    unsigned long m_recv_buffer_size;
    char* m_p_recv_buf;
    void* m_socket_pub;
    void* m_socket_sub;
    
protected:
    void* m_zmq_context;
    
private:
    char* m_id;
    char* m_socket_type;
    int m_port;
    int m_timeout;
    char* m_host_ip;
    char* m_p_send_buf;
    unsigned long m_ul_send_buf_size;

    void init_poster_sock();
    void init_observer_sock();
};

#endif /* defined(__ZMQX__ZMQNotification__) */
