//
//  DLClient.h
//  TCPManager
//
//  Created by Liang on 15-4-27.
//  Copyright (c) 2015年 Liu Liang. All rights reserved.
//

#import <Foundation/Foundation.h>
//#import "GCDAsyncSocket.h"
#import "GCDAsyncSocket.h"
#import "DataParse.h"
#import "Publisher.hpp"

@interface DLClient : NSObject<InterfaceProtocol>
{
    GCDAsyncSocket* m_ClientSock;
    NSMutableString* m_strServerIp;
    short m_port;
    BOOL m_ConnState;
    BOOL bParseFinished;
    NSMutableString* m_strConfigPath;
    NSMutableString* m_strStringToDetect;
    NSMutableData* m_dataRecvBuffer;
    NSMutableString* m_strReadBuffer;
    NSMutableString* m_strOutput;
    NSLock* m_lockBuffer;
    DataParse * dp;
    
    @private
    NSThread *threadParseManage;
    bool getGainFlag;
    CPubliser * zmqPub0;

    NSMutableData* dataLast;
}

- (id)initWithIPPort:(NSString*)hwName :(NSString*)ip :(short)port;
- (int)initZmqPub:(const char*)address;

- (BOOL)getConnectState;
- (NSData*)getStubData;
- (void)clearStubData;

- (void)clearBuffer;
- (void)setDetectString:(NSString*)strDetectString;
- (int)send:(NSString*)str;
- (int)waitString:(int)timeout;
- (NSString*)readString;
- (NSString*)sendRecv:(NSString*)str :(int)timeout;

-(void)clearDataLast;
-(void)getLinearIndex;

- (int)disconnect;

-(void)StartDL;
-(void)StopDL;

-(void)updateConfig:(int)channel :(float)resdiv :(float)gain :(float)refVolt :(float)res :(int)flag :(int)unitConvert;
-(void)updateCalFactor:(int)channel :(float)gain :(float)offset;
-(void)setLogPath:(const char *)header :(const char*) filename;
-(void)SaveLog:(NSString *)str;

//RMS
- (NSString *)startRMS:(int)channel;
- (NSString *)endRMS:(int)channel;
- (double)getRMS:(int)channel;
- (double)getAverage:(int)channel;
- (float)getMax:(int)channel;
- (float)getMin:(int)channel;
- (unsigned long)getCount:(int)channel;
- (void)setArmChannel:(int)ch;
- (int)getArmChannel;

@property(assign) BOOL logOn;
@property (nonatomic, retain) GCDAsyncSocket * m_ClientSock;
@property(nonatomic, retain)  NSMutableData* dataLast;

@end
