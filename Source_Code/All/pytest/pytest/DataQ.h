//
//  DataQ.h
//  socket_udp
//
//  Created by AustinShih on 2/12/16.
//  Copyright © 2016年 AustinShih. All rights reserved.
//


#ifndef DATA_Q_H
#define DATA_Q_H

#include <stdio.h>
#include <Foundation/Foundation.h>

class CDataQ
{
public:
    CDataQ();
    virtual ~CDataQ();
public:
    long PushData(void* pbuf,long len);
    long GetData(void* pbuf,long len);
    long GetBufLen();
    long ClearBuf();
    
    NSMutableData * m_DataBuf;
    pthread_mutex_t m_mutex;
};

#endif /* DATA_Q_H */
