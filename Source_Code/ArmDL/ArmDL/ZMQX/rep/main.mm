//
//  main.m
//  rep
//
//  Created by Liang on 15-8-5.
//  Copyright (c) 2015年 Liang. All rights reserved.
//

#import <Foundation/Foundation.h>
#include "zmq.h"
#include <iostream>
#include <string>
#include <unistd.h>

int main(int argc, const char * argv[])
{
    void* ctx = zmq_ctx_new();
    void* sock = NULL;
    if (ctx)
    {
        sock = zmq_socket (ctx, ZMQ_REP);
        if (sock == NULL) {
            std::cout << "zmqw::zmqw failed to create ZMQ_PUB reply service socket.\n";
        }else
        {
            char szBuf[128];
            //zmq_bind (m_repService, "tcp://*:5562");
            memset(szBuf, 0, sizeof(szBuf));
            sprintf(szBuf, "tcp://*:%d", 6543);
            if (zmq_bind (sock, szBuf) < 0) {
                std::cout << "zmqw::zmqw failed to bind address " << szBuf << "for ZMQ_PUB reply service socket.\n";
            }
        }
    }
    
    
    printf("Please enter your command : \r\n");
    char Buffer[1024];
    memset(Buffer, 0, sizeof(Buffer));
    while (1) {
        fgets(Buffer, sizeof(Buffer), stdin);
        if (strcmp(Buffer, "q\n") == 0) {
            break;
        }
        else
        {
            int r = 0;
            errno = 0;
            memset(Buffer, 0, sizeof(Buffer));
            r = zmq_recv(sock, Buffer, sizeof(Buffer), 0);
            if (r < 0) {
                std::cout << "zmqw::pub_recv failed to receive message with error:" << zmq_strerror(errno) << "\n";
            }else
            {
                //success
                printf("%s\n", Buffer);
            }
            char szTmp[1200] = {0};
            sprintf(szTmp, "reply for [%s]", Buffer);
            zmq_send(sock, szTmp, strlen(szTmp)+ 1, 0);
        }
        memset(Buffer, 0, sizeof(Buffer));
    }

    return 0;
}

