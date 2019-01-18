//
//  DataQ.m
//  socket_udp
//
//  Created by AustinShih on 2/12/16.
//  Copyright © 2016年 AustinShih. All rights reserved.
//

#import "DataQ.h"

#include <sys/ioctl.h>
#include <iostream>


CDataQ::CDataQ()
{
    m_DataBuf = [[NSMutableData alloc]init];
    pthread_mutex_init(&m_mutex, NULL);
}

CDataQ::~CDataQ()
{
    if (m_DataBuf) {
        [m_DataBuf release];
    }
    pthread_mutex_destroy(&m_mutex);
}

long CDataQ::PushData(void* pbuf, long len)
{
    pthread_mutex_lock(&m_mutex);
    long ret = len;
    [m_DataBuf appendBytes:pbuf length:len];
    pthread_mutex_unlock(&m_mutex);
    return ret;
}

long CDataQ::GetData(void* pbuf, long len)
{
    pthread_mutex_lock(&m_mutex);
    unsigned char* pByte = (unsigned char*)[m_DataBuf bytes];
    memcpy(pbuf, pByte, [m_DataBuf length]);
    [m_DataBuf setLength:0];
    pthread_mutex_unlock(&m_mutex);
    return [m_DataBuf length];
}

long CDataQ::GetBufLen()
{
    return [m_DataBuf length];
}

long CDataQ::ClearBuf()
{
    pthread_mutex_lock(&m_mutex);
    [m_DataBuf setLength:0];
    pthread_mutex_unlock(&m_mutex);
    return 0;
}

