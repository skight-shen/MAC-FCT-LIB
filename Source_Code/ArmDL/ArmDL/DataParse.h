//
//  DataParse.h
//  TCPIP
//
//  Created by IvanGan on 15/5/25.
//  Copyright (c) 2015年 IA. All rights reserved.
//


#define FRAME_LENGTH  (2048)
#define PAYLOAD_LENGTH  (FRAME_LENGTH-20)
#define DATALOGGER_CHANNEL_NUM  (6)

enum F_FrameType{
    F_DATALOGGER  = 0x01,
    F_PWRSEQUENCE  = 0x02,
    F_AUDIO  = 0x10,
    F_SPDIF  = 0x11,
    F_HDMI   = 0x20,
    F_UNKNOWN
};
typedef enum F_FrameType fFrameType;

enum D_DataWidth{
    D_DATAWIDTH_01  = 0x01,
    D_DATAWIDTH_02  = 0x02,
    D_DATAWIDTH_04  = 0x04,
    D_DATAWIDTH_UN
};
typedef enum D_DataWidth dDataWidth;

struct FRAME_CONTENT{
    unsigned char frametype;      //L:1    0x01
    unsigned char datawidth;     //L:1/2  0x4
    unsigned char chn;       //L:1/2  0x1~0x6
    unsigned int frameid;       //L:2    0x0000~0xFFFF
    
    unsigned char userdatainfo;       //L:1     0x01
    unsigned long samplerate;         //L:3     0x000001
    
    unsigned long sampletime_s;       //L:4     0x00000000
    
    unsigned int sampletime_ms;       //L:2     0x0000
    unsigned int payloadlen;          //L:2     0x0000
    
    unsigned char payload[PAYLOAD_LENGTH];    //L:507 * 4
    
    unsigned int endflag;               //L:2     0x0000
    unsigned int crc;                   //L:2     0x0000
};

#import <Foundation/Foundation.h>

@protocol InterfaceProtocol <NSObject>

@required
-(void)SaveLog:(NSString *)str;
@end



@interface DataParse : NSObject
{
    FRAME_CONTENT F_Frame;
    
    NSMutableArray *chanBuff[DATALOGGER_CHANNEL_NUM];
    int buffCount[DATALOGGER_CHANNEL_NUM];
    int myChannel;
    id  <InterfaceProtocol> delegate;
    
 @public
    bool getAllFlag[DATALOGGER_CHANNEL_NUM];
    float k[DATALOGGER_CHANNEL_NUM];
    float b[DATALOGGER_CHANNEL_NUM];
    float _resdiv[DATALOGGER_CHANNEL_NUM];
    float _refVolt[DATALOGGER_CHANNEL_NUM];
    float _gain[DATALOGGER_CHANNEL_NUM];
    float _res[DATALOGGER_CHANNEL_NUM];
    int iUnitConvert[DATALOGGER_CHANNEL_NUM];
    NSString * dataFilePath[DATALOGGER_CHANNEL_NUM];
    NSString * byteFilePath[DATALOGGER_CHANNEL_NUM];
    
    BOOL bRMS[DATALOGGER_CHANNEL_NUM];
    long double powSum[DATALOGGER_CHANNEL_NUM];
    long double sum[DATALOGGER_CHANNEL_NUM];
    BOOL bFirstValue[DATALOGGER_CHANNEL_NUM];
    float maxValue[DATALOGGER_CHANNEL_NUM];
    float minValue[DATALOGGER_CHANNEL_NUM];
    unsigned long count[DATALOGGER_CHANNEL_NUM];
    NSString * trigerTime[DATALOGGER_CHANNEL_NUM];
}
-(int)parseFrame:(Byte*)data;
-(BOOL)parseData:(NSData*)data;
-(void)setArmChannel:(int)ch;
-(int)getArmChannel;

-(void)SetDelegate:(id  <InterfaceProtocol>)object;
-(void)clearData;


@property (assign)int myChannel;
@property (assign)BOOL bBreakParse;
@property (assign)struct FRAME_CONTENT F_Frame;
@end


