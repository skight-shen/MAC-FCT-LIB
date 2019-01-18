//
//  DataParse.m
//  TCPIP
//
//  Created by IvanGan on 15/5/25.
//  Copyright (c) 2015年 IA. All rights reserved.
//

#import "DataParse.h"
#include <math.h>

@implementation DataParse


@synthesize myChannel;
@synthesize bBreakParse;
@synthesize F_Frame;

-(id)init
{
    self = [super init];
    if(self)
    {
        for (int i=0; i<DATALOGGER_CHANNEL_NUM; i++) {
            chanBuff[i] = [[NSMutableArray alloc]init];
            buffCount[i] = 0;
            getAllFlag[i] = false;
            k[i] = 1.0;
            b[i] = 0.0;
            _resdiv[i] = 1.0;
            _refVolt[i] = 2.5;
            _gain[i] = 3.91176;
            _res[i] = 0.5;
            iUnitConvert[i] = 1;
            
            bRMS[i] = false;
            powSum[i] = 0.0;
            sum[i] = 0.0;
            bFirstValue[i] = false;
            maxValue[i] = 0.0;
            minValue[i] = 0.0;
            count[i] = 0;
            trigerTime[i] = nil;
        }
        bBreakParse = false;
        
        F_Frame.frametype = F_DATALOGGER;
        F_Frame.datawidth = D_DATAWIDTH_04;
        F_Frame.chn = 0x0;
        F_Frame.frameid = 0x0000;
        F_Frame.userdatainfo = 0x06;
        F_Frame.samplerate = 0x000001;
        F_Frame.sampletime_s = 0x00000000;
        F_Frame.sampletime_ms = 0x0000;
        F_Frame.payloadlen = 0x0000;
        
        memset(F_Frame.payload, 0, PAYLOAD_LENGTH);
        F_Frame.endflag = 0x0000;
        F_Frame.crc = 0x0000;
        myChannel = 4;
    }
    return self;
}

-(int)getArmChannel
{
    return myChannel;
}

-(void)setArmChannel:(int)ch
{
    myChannel = ch;
}

-(void)SetDelegate:(id  <InterfaceProtocol>)object
{
    delegate = object;
}

-(void)dealloc
{
    for (int i = 0; i < DATALOGGER_CHANNEL_NUM; i++)
    {
        [chanBuff[i] release];
    }

    [super dealloc];
}

-(int)parseFrame:(Byte *)data
{
    F_Frame.frametype   = data[0];
    F_Frame.datawidth   = data[1]>>4;
    F_Frame.chn     = data[1]&0x0F;
    F_Frame.frameid     = data[2] + (data[3]<<8);
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
    NSLog(@"channel:%02X\r\n",frame.chn);
    NSLog(@"frame id:%02X\r\n",frame.frameid);
    NSLog(@"user data info:%02X\r\n",frame.userdatainfo);
    NSLog(@"sample rate:%lX\r\n",frame.samplerate);
    NSLog(@"sample time (s):%lX\r\n",frame.sampletime_s);
    NSLog(@"sample time (ms):%04X\r\n",frame.sampletime_ms);
    NSLog(@"payload length:%02X\r\n",frame.payloadlen);
    return 0;
}

-(void)writetoFileEnd:(NSString*)str :(NSString*)fPath
{
    @try {
        NSFileHandle * fh = [NSFileHandle fileHandleForWritingAtPath:fPath];
        if(!fh) return;
        [fh seekToEndOfFile];
        if ([str canBeConvertedToEncoding:NSASCIIStringEncoding])
        {
            [fh writeData:[str dataUsingEncoding:NSASCIIStringEncoding]];
        }
        [fh closeFile];
    } @catch (NSException *exception) {
        NSLog(@"armdl exception !");
    } @finally {
        
    }
   
}

-(BOOL)parseData:(NSData *)data
{
    NSMutableData * dataTmp = [NSMutableData data];
    [dataTmp appendData:data];
    
    long dLen = [dataTmp length];
    if (dLen!=FRAME_LENGTH) {
        return NO;
    }
    memset(&F_Frame, 0, FRAME_LENGTH);
    
    Byte * dByte = (Byte*)[dataTmp bytes];
    [self parseFrame:dByte];
    int AdcData = 0;
    
    if (F_Frame.frametype == F_DATALOGGER) {
        //NSLog(@"frame id:%d, payload lenth:%d\r\n",F_Frame.frameid,F_Frame.payloadlen);
        if (F_Frame.payloadlen == PAYLOAD_LENGTH) {
            for (int i=0; i<PAYLOAD_LENGTH; i+=F_Frame.datawidth) {
                if (bBreakParse) {
                    NSLog(@"Break parseData");
                    break;
                }
                
                //Data field
                AdcData = 0;   //0x01234567   0x67452301
                int channel = F_Frame.payload[i]&0x0F;
                if (channel>=myChannel || channel<0) {   //discard all garbage data
                    continue;
                }
                
                AdcData = (F_Frame.payload[i]&0xF0) + (F_Frame.payload[i+1]<<8) + (F_Frame.payload[i+2]<<16) + (F_Frame.payload[i+3]<<24);
                float realV = 0.0;
                AdcData = AdcData&0xFFFFFFFF;
                if (AdcData > 0x80000000) {
                    realV = (float)(AdcData-0x80000000)*_refVolt[channel]/(float)0x80000000;
                }else{
                    realV = -1 * (float)(0x80000000-AdcData)*_refVolt[channel]/(float)0x80000000;
                }
                realV = ((realV/_gain[channel])/_res[channel])*_resdiv[channel];
                
                //Time stamp
                int Time_s = F_Frame.sampletime_s&0xFFFFFFFF;
                int Time_ms = F_Frame.sampletime_ms+(i/F_Frame.datawidth);
                Time_s += (Time_ms/1000);
                Time_ms = Time_ms%1000;
                
                time_t t = (time_t)Time_s;
                tm * local = localtime(&t);
                char buf[64];
                memset(buf, 0, sizeof(buf));
                
                strftime(buf, 64, "%m/%d/%Y %H:%M:%S", local);
                [chanBuff[channel] addObject:[NSString stringWithFormat:@"%s.%03d,%.6f",buf,Time_ms,realV]];
                buffCount[channel]++;
                [self DumpLog];
             
                if (bRMS[channel]) {
                    sum[channel] = sum[channel] + realV;
                    powSum[channel] = powSum[channel] + realV * realV;
                    if (bFirstValue[channel]) {
                        trigerTime[channel] = [NSString stringWithFormat:@"%s:%d",buf,Time_ms];
                        maxValue[channel] = realV;
                        minValue[channel] = realV;
                        bFirstValue[channel] = false;
                    }
                    if(maxValue[channel] < realV)
                        maxValue[channel] = realV;
                    if(minValue[channel] > realV)
                        minValue[channel] = realV;
                    count[channel] = count[channel] + 1;
                }
            }
        }
    }else{
        NSLog(@"NOT MATCH DATALOGGER FORMAT");
        return NO;
    }
    
    return YES;
}

-(void)DumpLog
{
    int minCount = buffCount[0];
    int maxCount = buffCount[0];
    
    NSMutableString * str = [[NSMutableString alloc]init];
    
    for (int i = 0 ; i < myChannel; i++)
    {
        minCount = (minCount < buffCount[i]) ? minCount : buffCount[i];
        maxCount = (maxCount < buffCount[i]) ? buffCount[i] : maxCount;
    }
    
    //    if (maxCount > minCount + 1)
    //    {
    //        NSLog(@"[%d]channel num missed,maxCoun=%d,minCound=%d",myChannel,maxCount,minCount);
    //    }
    
    if (minCount > 0)
    {
        for (int i = 0; i < minCount; i++)
        {
            for (int j = 0; j < myChannel; j++)
            {
                //                [delegate SaveLog:[chanBuff[j] objectAtIndex:lastParseCount+i] logIndex:1];
                [str appendString:[chanBuff[j] objectAtIndex:i]];
                if (j== myChannel -1)
                {
                    [str appendString:@"\r\n"];
                }
                else
                {
                    [str appendString:@","];
                }
                //                [delegate SaveLog:[chanBuff[j] objectAtIndex:i+1] logIndex:2];
            }
            
            
        }
        
        [delegate SaveLog:str];
        
        for (int i = 0; i < myChannel; i++)
        {
            [chanBuff[i] removeObjectsInRange:NSMakeRange(0, minCount)];
            buffCount[i] = buffCount[i] - minCount;
        }
        
    }
    [str setString:@""];
    [str release];
}


-(void)clearData
{
    for (int i=0; i<DATALOGGER_CHANNEL_NUM; i++)
    {
        [chanBuff[i] removeAllObjects];
        buffCount[i] = 0;
    }
}

@end
