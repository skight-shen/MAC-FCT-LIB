//
//  main.m
//  req
//
//  Created by Liang on 15-8-5.
//  Copyright (c) 2015年 Liang. All rights reserved.
//

#import <Foundation/Foundation.h>
#include "ZMQReqRep.h"

int main(int argc, const char * argv[])
{
    ZMQReqRep* req = new ZMQReqRep(6543);
    
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
            req->send(Buffer, strlen(Buffer));
            memset(Buffer, 0, sizeof(Buffer));
            req->receive(Buffer, sizeof(Buffer));
            printf("%s\n", Buffer);
        }
        memset(Buffer, 0, sizeof(Buffer));
    }
    return 0;
}

