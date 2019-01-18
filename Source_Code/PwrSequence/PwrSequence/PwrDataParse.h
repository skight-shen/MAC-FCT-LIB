//
//  PwrDataParse.h
//  PwrSequence
//
//  Created by AustinShih on 23/11/16.
//  Copyright © 2016年 AustinShih. All rights reserved.
//

#define FRAME_LENGTH  (2020)
#define PAYLOAD_LENGTH  (FRAME_LENGTH-20)
#define CHANNEL_NUMBER (80+2)

enum F_FrameType{
    F_DATALOGGER  = 0x01,
    F_PWRSEQUENCE  = 0x02,
    F_AUDIO  = 0x10,
    F_SPDIF  = 0x11,
    F_HDMI   = 0x20,
    F_UNKNOWN
};
typedef enum F_FrameType fFrameType;

enum F_UserDataInfo{
    F_USData_PS = 0x05,
    F_USData_BL = 0x06,
    F_USData_UN
};

enum D_DataWidth{
    D_DATAWIDTH_01  = 0x01,
    D_DATAWIDTH_02  = 0x02,
    D_DATAWIDTH_04  = 0x04,
    D_DATAWIDTH_UN
};
typedef enum D_DataWidth dDataWidth;

struct FRAME_CONTENT{
    unsigned char frametype;      //L:1    0x02
    unsigned char datawidth;     //L:1/2  0x4
    unsigned char channel;       //L:1/2  0x1~0xF    unused
    unsigned int frameid;       //L:2    0x0000~0xFFFF
    
    unsigned char userdatainfo;       //L:1     0x01
    unsigned long samplerate;         //L:3     0x000001
    
    unsigned long sampletime_s;       //L:4     0x00000000
    
    unsigned int sampletime_ms;       //L:2     0x0000
    unsigned int payloadlen;          //L:2     0x0000
    
    unsigned char payload[PAYLOAD_LENGTH];    //L:1000 * 2
    
    unsigned int endflag;               //L:2     0x0000
    unsigned int crc;                   //L:2     0x0000
};

#import <Foundation/Foundation.h>


@protocol InterfaceProtocol <NSObject>

@required
-(void)SaveLog:(NSString *)str logIndex:(int)index;
@end



@interface PwrDataParse : NSObject
{
    FRAME_CONTENT F_Frame;
    
 
    
    //NSMutableArray * aTimeStamp;
    NSMutableString * strBL_B;
    NSMutableString * strBL_D;

    bool getAllFlag;
    int Time_s;
    int Time_ms;
    
    
    int lastParseCount;
    int lastAppendCH1;
    int lastAppendCH2;
    
    id  <InterfaceProtocol> delegate;
    NSMutableArray *chanBuff[CHANNEL_NUMBER];
    int buffCount[CHANNEL_NUMBER];
    int myChannel;
    int framenum;
@private
    unsigned int _1to40_FrameId;
    unsigned int _41to80_FrameId;
}

-(void)SetDelegate:(id  <InterfaceProtocol>)object;
-(void)InitParser;
-(int)parseFrame:(Byte*)data;
-(BOOL)parseData:(NSData*)data;
-(void)DumpLog;

-(void)setPwrSeqChannel:(int)ch;
-(int)getPwrSeqChannel;



//@property (nonatomic, retain)NSMutableArray * aTimeStamp;


@property (assign)int myChannel;
@property (assign)bool getAllFlag;
@property (assign)BOOL bBreakParse;
@property (assign)struct FRAME_CONTENT F_Frame;
@property (nonatomic,retain)NSMutableArray * _chName;
@property (nonatomic,retain)NSMutableArray * _gain;
@property (nonatomic,retain)NSMutableArray * _offset;
@property (nonatomic,retain)NSMutableArray * _onoff;

@property (nonatomic, retain)NSMutableString * strBL_B;
@property (nonatomic, retain)NSMutableString * strBL_D;
@property (assign)int Time_s;
@property (assign)int Time_ms;
@property (assign)int framenum;
@property (assign)unsigned int _1to40_FrameId;
@property (assign)unsigned int _41to80_FrameId;

@end
