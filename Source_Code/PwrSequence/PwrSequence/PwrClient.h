//
//  PwrClient.h
//  PwrSequence
//
//  Created by AustinShih on 23/11/16.
//  Copyright © 2016年 AustinShih. All rights reserved.
//


#import <Foundation/Foundation.h>
#import "GCDAsyncSocket.h"
#import "PwrDataParse.h"
#import "Publisher.hpp"
#include <condition_variable>
#include <mutex>

@interface PwrClient :  NSObject<InterfaceProtocol>
{
    GCDAsyncSocket_PS* m_ClientSock;
    NSMutableString* m_strServerIp;
    short m_port;
    
    BOOL m_ConnState;
    BOOL bParseFinished;
    
    NSMutableData* m_dataRecvBuffer;
    NSLock* m_lockBuffer;
    PwrDataParse* dp;
    
    NSString* dataFilePath;
    NSString* byteFilePath;
    
    
    //for channel 41-80
    NSString* dataFilePath2;
    NSString* byteFilePath2;
    NSMutableData* dataLast;
    
@public
    int m_channels;
    
@private
    NSThread* threadParseManage;
    CPubliser * zmqPub;
    CPubliser * zmqPub_BKLT;
    
    int ps_flag;    //1: Power sequencer  other:backlight
    
    long parseBuffLoc;
    long dataLenth;
    long receiveCount;
    std::mutex m_data;
    std::condition_variable cv_data;
    FILE* LogManager;
    int channelID;
}

- (id)initWithIPPort:(NSString*)hwName :(NSString*)ip :(short)port;
- (int)initZmqPub:(const char*)address :(int)writeLog;
- (int)initZmqPub_BKLT:(const char*)address :(int)writeLog;
- (BOOL)getConnectState;
- (void)clearStubData;
- (void)clearDataLast;

- (int)connect;
- (int)disconnect;

- (void)StartDL:(int)flag;
- (void)StopDL:(int)flag;
- (void)updateConfig:(const char*)config :(int)flag :(int)configID;
- (void)SaveLog:(NSString *)str logIndex:(int)index;
- (void)SaveFrameLog:(NSString *)data;

-(void)setPwrSeqChannel:(int)ch;
-(int)getPwrSeqChannel;
-(void)resetTimeStamp;

@property(retain) NSString * dataFilePath;
@property(retain) NSString * byteFilePath;//triger file
@property(assign) BOOL logOn;
@property(assign) int m_channels;
@property(assign) int channelID;
@property (nonatomic, retain) GCDAsyncSocket_PS * m_ClientSock;
@property(nonatomic,retain) NSMutableData * dataLast;

@end
