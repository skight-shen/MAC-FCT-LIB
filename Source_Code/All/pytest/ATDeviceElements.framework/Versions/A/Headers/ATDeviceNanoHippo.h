//
//  ATDeviceNanoHippo.h
//
//  Created by Sai  on 11/11/16.
//  Copyright © 2016 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "ATDHippoCommon.h"

@interface ATDeviceNanoHippo : NSObject

//--------------------------------------------------------------
//--------------------------------------------------------------
// Write to Hippo Channel Data is  packetized.
//--------------------------------------------------------------
//--------------------------------------------------------------
//args:
//  des_port: The Destination UDP port number (Hippo Channel number)
//  dataToSend: The data to be sent.
//  aError:  The error message when something wrong happened.
//return:
//     YES = successed , NO = failed
-(BOOL) writeHippoDataToPort: (NSNumber *_Nonnull) des_port
                     andData: (NSData*_Nonnull) dataToSend
                    andError: (NSError *_Nullable*_Nullable) aError;

//--------------------------------------------------------------
//--------------------------------------------------------------
// Write to the serial port. Data is Not packetized.
//--------------------------------------------------------------
//--------------------------------------------------------------
//args:
//  dataToSend: The data to be sent.
//  aError:  The error message when something wrong happened.
//return:
//     YES = successed , NO = failed
-(BOOL) writeSerialData: (NSData * _Nonnull) dataToSend
               andError: (NSError *_Nullable*_Nullable) aError;

//--------------------------------------------------------------
//--------------------------------------------------------------
// close the serial connection
//--------------------------------------------------------------
//--------------------------------------------------------------
-(void) close;

//--------------------------------------------------------------
//--------------------------------------------------------------
// open the serial connection
//--------------------------------------------------------------
//--------------------------------------------------------------
//args:
//  aPath: The serial path e.g.  /dev/cu.usbmodem143422
//  serialCallBack:   serial data callback block. Data will be passed in
//  hippoCallBack:    Hippo data callback block.  A UDP port number (Hippo Channel number) and data will be passed in.
//  newHippoAddedCallBack:  New hippo channel added callback block. A UDP port number (Hippo Channel number) will be passed in.
//return:
//     YES = successed , NO = failed

-(BOOL) openWithSerialPath: ( NSString *_Nonnull) aPath
     andSerialDataCallBack: (SerialDataCallBack _Nullable) serialCallBack
          andHippoCallBack: (HippoChannelCallBack _Nonnull ) hippoCallBack
andNewHippoChannelAddedCallBack: (NewHippoChannelAddedCallBack _Nonnull ) newHippoAddedCallBack
                  andError:(NSError *_Nullable*_Nullable) error ;

@end
