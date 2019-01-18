//
//  PwrDataParse.m
//  PwrSequence
//
//  Created by AustinShih on 23/11/16.
//  Copyright © 2016年 AustinShih. All rights reserved.
//
#include "PwrClient.h"
#import "PwrDataParse.h"
#include <math.h>
#include <iostream>

@implementation PwrDataParse

@synthesize getAllFlag;
@synthesize F_Frame;
@synthesize bBreakParse;
@synthesize _chName;
@synthesize _offset;
@synthesize _gain;
@synthesize _onoff;
//@synthesize aTimeStamp;
@synthesize strBL_B;
@synthesize strBL_D;
@synthesize Time_s;
@synthesize Time_ms;
@synthesize myChannel;
@synthesize _1to40_FrameId;
@synthesize _41to80_FrameId;
@synthesize framenum;

-(id)init
{
    self = [super init];
    if (self) {
        framenum = 0;
        myChannel = CHANNEL_NUMBER;
        _onoff = [[NSMutableArray alloc]initWithCapacity:CHANNEL_NUMBER];
        _gain = [[NSMutableArray alloc]initWithCapacity:CHANNEL_NUMBER];
        _chName = [[NSMutableArray alloc]initWithCapacity:CHANNEL_NUMBER];
        _offset = [[NSMutableArray alloc]initWithCapacity:CHANNEL_NUMBER];
        //aTimeStamp = [[NSMutableArray alloc]init];
        strBL_B = [[NSMutableString alloc]init];
        strBL_D = [[NSMutableString alloc]init];
        for (int i = 0; i <CHANNEL_NUMBER; i++)
        {
            chanBuff[i] = [[NSMutableArray alloc]init];
            buffCount[i] = 0;
        }
                
        for (int i=0; i<CHANNEL_NUMBER; i++) {
            [_chName insertObject:@"" atIndex:i];
            [_gain insertObject:@"" atIndex:i];
            [_offset insertObject:@"" atIndex:i];
            [_onoff insertObject:@"" atIndex:i];
        }
        getAllFlag = false;
        bBreakParse = false;
        //Channels * 48 * 25   //reserve 3 length
        //time_step = CHANNEL_NUMBER*48*25/1000;
    
        F_Frame.frametype = F_PWRSEQUENCE;
        F_Frame.datawidth = D_DATAWIDTH_02;
        F_Frame.channel = 0x0;
        F_Frame.frameid = 0x0000;
        F_Frame.userdatainfo = F_PWRSEQUENCE;
        F_Frame.samplerate = 0x009C40;   //40K*K
        F_Frame.sampletime_s = 0x00000000;
        F_Frame.sampletime_ms = 0x0000;
        F_Frame.payloadlen = 0x0000;
        
        memset(F_Frame.payload, 0, PAYLOAD_LENGTH);
        F_Frame.endflag = 0x0000;
        F_Frame.crc = 0x0000;
        [self InitParser];
    }
    return self;
}

-(void)dealloc
{
    for (int i = 0; i < CHANNEL_NUMBER;i++)
    {
        [chanBuff[i] removeAllObjects];
        [chanBuff[i] release];
    }
    [_chName removeAllObjects];
    [_chName release];
    [_gain removeAllObjects];
    [_gain release];
    [_offset removeAllObjects];
    [_offset release];
    [_onoff removeAllObjects];
    [_onoff release];
    //[aTimeStamp removeAllObjects];
    //[aTimeStamp release];
    [strBL_B release];
    [strBL_D release];
    [super dealloc];
}

-(void)SetDelegate:(id<InterfaceProtocol>)object
{
    delegate = object;
}

-(void)InitParser
{
    for (int i = 0; i < CHANNEL_NUMBER;i++)
    {
        [chanBuff[i] removeAllObjects];
        buffCount[i] = 0;
        lastParseCount = 0;
    }
}

-(int)parseFrame:(Byte*)data
{
    framenum++;
    F_Frame.frametype = data[0];
    F_Frame.datawidth = data[1]>>4;
    F_Frame.channel   = data[1]&0x0F;
    F_Frame.frameid   = data[2] + (data[3]<<8);

//    NSLog(@"Parse Frame type:%d datawidth:%d Frame id:%x channel:%d",F_Frame.frametype,F_Frame.datawidth,data[2] + (data[3]<<8),F_Frame.channel);
    
    F_Frame.userdatainfo = data[4];
    F_Frame.samplerate  = data[5] + (data[6]<<8) + (data[7]<<16);
    F_Frame.sampletime_s = data[8] + (data[9]<<8) + (data[10]<<16) + (data[11]<<24);
    F_Frame.sampletime_ms = data[12] + (data[13]<<8);
    F_Frame.payloadlen = data[14] + (data[15]<<8);
    memcpy(F_Frame.payload, &data[16], PAYLOAD_LENGTH);
    
    //[self printFrame:F_Frame];
    return 0;
}

-(int)printFrame:(FRAME_CONTENT)frame
{
    NSLog(@"frame type:%02X\r\n",frame.frametype);
    NSLog(@"data width:%02X\r\n",frame.datawidth);
    NSLog(@"channel:%02X\r\n",frame.channel);
    NSLog(@"frame id:%02X\r\n",frame.frameid);
    NSLog(@"user data info:%02X\r\n",frame.userdatainfo);
    NSLog(@"sample rate:%lX\r\n",frame.samplerate);
    NSLog(@"sample time (s):%lX\r\n",frame.sampletime_s);
    NSLog(@"sample time (ms):%04X\r\n",frame.sampletime_ms);
    NSLog(@"payload length:%02X\r\n",frame.payloadlen);
    return 0;
}

-(void)SaveErrorDateData:(NSData *)dateData
{
    Byte* dByte = (Byte*)[dateData bytes];
    NSMutableString *stringData = [NSMutableString string];
    NSLog(@"dateDate length:%lu",(unsigned long)[dateData length]);
//    std::cout << "hex dateData:";
//    for (int i=0; i<[dateData length]; i++) {
//        printf("%02X ",dByte[i]);
//    }
//    std::cout << std::endl;
    for (int i=0; i<[dateData length]; i++) {
        [stringData appendFormat:@"%02X ",dByte[i]];
    }
    NSLog(@"SaveErrorDateData stringData:%@",stringData);

    
    //NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
    //[dateFormatter setDateFormat:@"yyyy-MM-dd-HH-mm-ss"];
    //[dateFormatter setDateFormat:@"yyyy-MM-dd"];
    //NSDate* stopTime = [NSDate date];
    //NSString * strStopTime=[dateFormatter stringFromDate:stopTime];
    //[dateFormatter release];
    
    NSString *fileName = [NSString stringWithFormat:@"/vault/Intelli_log/IA_log/UUT%d_PwrFrameLog.txt",[(PwrClient *)delegate channelID]];
    NSFileManager *fm = [NSFileManager defaultManager];
    if (![fm fileExistsAtPath:fileName]) {
        [fm createFileAtPath:fileName contents:nil attributes:nil];
    }
    NSFileHandle * fh = [NSFileHandle fileHandleForWritingAtPath:fileName];
    if(!fh) return;
    [fh seekToEndOfFile];
    [fh writeData:[stringData dataUsingEncoding:NSASCIIStringEncoding]];
    [fh closeFile];
}

-(BOOL)parseData:(NSData*)data
{
    NSMutableData* dataTmp = [NSMutableData data];
    [dataTmp appendData:data];
    
    long dLen = [dataTmp length];
    if (dLen<FRAME_LENGTH) {
        return NO;
    }

    Byte* dByte = (Byte*)[dataTmp bytes];
    [self parseFrame:dByte];
    int AdcData = 0;
    int channel = 0;
    
    if (F_Frame.frametype == F_PWRSEQUENCE) {
        if (Time_ms<=0 && Time_s<=0) {  //only get the time stamp in the received first data frame
            Time_s = F_Frame.sampletime_s&0xFFFFFFFF;
            Time_ms = F_Frame.sampletime_ms;
            
            int stp = (Time_ms/1000);
            Time_s += stp;
            time_t t = (time_t)Time_s;
            time_t now = time(NULL);
            //NSLog(@"ARM t : %lu",t);
            //NSLog(@"ARM now : %lu",now);

            long diff = now - t;
            if (diff >= 2*60*60) {
                NSLog(@"ARM timestamp is very different with current time");
                //[self SaveErrorDateData:dataTmp];
            }
            
        }
        
        if (F_Frame.userdatainfo == F_USData_PS)
        {
            @autoreleasepool
            {
        
                if (F_Frame.payloadlen == PAYLOAD_LENGTH)
                {
                    for (long i=0; i<PAYLOAD_LENGTH; i+=F_Frame.datawidth*2) {   //include 2 data, channal id & data
    //                     NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
                        if (bBreakParse) {
                            NSLog(@"Break parseData");
                            break;
                        }
                        
                        AdcData = F_Frame.payload[i+2] + (F_Frame.payload[i+3]<<8);
                        channel = F_Frame.payload[i];// + (F_Frame.payload[i+1]<<8);
                        int tmpChannel = channel;
                        int firstFrame = F_Frame.payload[i+1];
                        if (firstFrame == 1)
                        {
                            
                            if ((F_Frame.frameid - _1to40_FrameId) == 2)
                            {
                                // 1-40 miss one frame,
                                for(long j=0; j<PAYLOAD_LENGTH; j+=F_Frame.datawidth*2){
                                    channel = F_Frame.payload[j];// + (F_Frame.payload[i+1]<<8);
                                    [self RecordNewChannelPacket:channel realVolt:-10 AdcData:0];
                                }
//                                [(PwrClient *)delegate SaveFrameLog:[NSString stringWithFormat:@"Frame 1to40 miss: %d",F_Frame.frameid-1]];
                                channel = tmpChannel;
                            }
                            _1to40_FrameId = F_Frame.frameid;

                        }
                        if (firstFrame == 2)
                        {
                            if ((F_Frame.frameid - _41to80_FrameId) == 2)
                            {
                                // 40-80 miss one frame,
                                for(long j=0; j<PAYLOAD_LENGTH; j+=F_Frame.datawidth*2){
                                    channel = F_Frame.payload[j];// + (F_Frame.payload[i+1]<<8);
                                    channel = channel + 40;
                                    [self RecordNewChannelPacket:channel realVolt:-10 AdcData:0];
                                }
//                                [(PwrClient *)delegate SaveFrameLog:[NSString stringWithFormat:@"Frame 41to80 miss: %d",F_Frame.frameid-1]];
                                channel = tmpChannel;
                            }
                            _41to80_FrameId = F_Frame.frameid;
                            channel = channel + 40;
                        }
                        
                        
                        float realVolt = 0.0;//(float)AdcData*2.0/(float)0x10000 + 2.0/2;
                        short Data_T = AdcData;
                        realVolt = (float)Data_T * 1.0/(float)0x8000;
                        if (channel >= myChannel)
                        {
    //                        NSLog(@"invalid chanel num:%d",channel);
                            break;
                        }
                        float gain = [[_gain objectAtIndex:channel]floatValue];
                        float offset = [[_offset objectAtIndex:channel]floatValue];
                        realVolt = realVolt*gain + offset;
                        [self RecordNewChannelPacket:channel realVolt:realVolt AdcData:AdcData];
    //                    [pool release];
                    }
                }
                else
                {
    //                NSLog(@"INVALID PARYLOAD LENGTH:");
                    return NO;
                }
                [self DumpLog];
            }
            
        }
        else if (F_Frame.userdatainfo == F_USData_BL)
        {
            [strBL_B setString:@""];
            [strBL_D setString:@""];
            for (long i=0; i<PAYLOAD_LENGTH; i+=F_Frame.datawidth)
            {
                if (bBreakParse)
                {
//                    NSLog(@"Break parseData");
                    break;
                }
                AdcData = 0;
                AdcData = F_Frame.payload[i] + (F_Frame.payload[i+1]<<8);
                
                float realVolt = 0.0;//(float)AdcData*2.0/(float)0x10000 + 2.0/2;
                short Data_T = AdcData;
                realVolt = (float)Data_T * 2.0/(float)0x10000;
                
                [strBL_D appendString:[NSString stringWithFormat:@"%.6f,",realVolt]];
                [strBL_B appendString:[NSString stringWithFormat:@"%04X,",AdcData]];
            }
        }
        else
        {
            [(PwrClient *)delegate SaveFrameLog:@"USER DATA INFO NOT MATCH 0x05"];
            [self SaveErrorDateData:dataTmp];
            //NSLog(@"USER DATA INFO NOT MATCH <POWER SEQUENCE> OR <BACKLIGHT> FORMAT");
            return NO;
        }
    }
    else
    {
        
        [(PwrClient *)delegate SaveFrameLog:@"FRAME TYPE NOT MATCH 0x02"];
        [self SaveErrorDateData:dataTmp];
        return NO;
    }
    return YES;
}



-(int)RecordNewChannelPacket:(int)channel realVolt:(float)realVolt AdcData:(short)AdcData
{
    if (channel == 0) {
        //Time stamp
        Time_ms += 1;
        int stp = (Time_ms/1000);
        Time_s += stp;
        Time_ms -= (stp*1000);
        
        time_t t = (time_t)Time_s;
        tm * local = localtime(&t);
        char buf[64];
        memset(buf, 0, sizeof(buf));
        strftime(buf, 64, "%m/%d/%Y %H:%M:%S", local);
        
        [chanBuff[channel] addObject:[NSString stringWithFormat:@"\r\n%s.%03d,%.6f",buf,Time_ms,realVolt]];
//        [chanBuff[channel] addObject:[NSString stringWithFormat:@"\r\n%s:%03d,%04X",buf,Time_ms,AdcData]];
        if (myChannel >= 80) {
            [chanBuff[80] addObject:[NSString stringWithFormat:@",%d",F_Frame.frameid]];
            buffCount[80]++;
        }
        buffCount[channel]++;
        
    }
    else
    {
        [chanBuff[channel] addObject:[NSString stringWithFormat:@",%.6f",realVolt]];
//        [chanBuff[channel] addObject:[NSString stringWithFormat:@",%04X",AdcData]];
        if ((myChannel >= 80) && (channel == 40)) {
            [chanBuff[81] addObject:[NSString stringWithFormat:@",%d",F_Frame.frameid]];
            buffCount[81]++;
        }
        buffCount[channel]++;
    }
    return 0;
}


-(void)DumpLog
{
    int minCount = buffCount[0];
    //int maxCount = buffCount[0];
    
    NSMutableString * str = [[NSMutableString alloc]init];
    
    int channelNum = myChannel;
    if (myChannel >= 80)
    {
        channelNum = myChannel + 2;
    }

    for (int i = 0 ; i < channelNum; i++)
    {
        minCount = (minCount < buffCount[i]) ? minCount : buffCount[i];
        //maxCount = (maxCount < buffCount[i]) ? buffCount[i] : maxCount;
    }
    
//    if (maxCount > minCount + 1)
//    {
//        NSLog(@"[%d]channel num missed,maxCoun=%d,minCound=%d",myChannel,maxCount,minCount);
//    }

    if (minCount > 0)
    {
        for (int i = 0; i < minCount; i++)
        {
            for (int j = 0; j < channelNum; j++)
            {
//                [delegate SaveLog:[chanBuff[j] objectAtIndex:lastParseCount+i] logIndex:1];
                [str appendString:[chanBuff[j] objectAtIndex:i]];
//                [delegate SaveLog:[chanBuff[j] objectAtIndex:i+1] logIndex:2];
            }
        }
        
        [delegate SaveLog:str logIndex:1];
        
        for (int i = 0; i < channelNum; i++)
        {
//            for (int j =0 ; j < minCount; j++) {
//                [chanBuff[i][j] release];
//            }
            [chanBuff[i] removeObjectsInRange:NSMakeRange(0, minCount)];
            buffCount[i] = buffCount[i] - minCount;
        }
        
//        lastParseCount += minCount;
    }
    [str setString:@""];
    [str release];
}

-(void)setPwrSeqChannel:(int)ch
{
    myChannel = ch;
}

-(int)getPwrSeqChannel
{
    return myChannel;
}




@end

