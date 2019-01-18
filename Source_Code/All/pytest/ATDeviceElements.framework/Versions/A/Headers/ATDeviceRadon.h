//
//  ATDeviceRadon.h
//  ATDeviceElements
//
//  Created by Sai  on 9/6/16.
//  Copyright © 2016 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <ATDeviceElements/ATDeviceUSBC.h>
#import <ATDeviceElements/ATDeviceParameters.h>

@interface ATDeviceRadon : ATDeviceUSBC


- (id) initWithCommunicationInterface: (ATDeviceBusInterface*) aCommInterface;


// Get the RG & BG CRC Values on incoming HDMI Streams on A1 and A2 for specified frames
// parameters
//      numOfFrames:input  Number of Frames to run the CRC Check on
//      expectedA1CRC:input  pass in nil if you don't use it
//      expectedA2CRC:input  pass in nil if you don't use it
//      A1CRC:output   A1 Antena 1's CRC. pass in address of ATDVideoHDMICrc or Pass in nil if you only need A2's CRC
//      A2CRC:output  A2 Antena 2's CRC. Pass in nil if you only need A1's CRC
//      andMismatchedFrames:output pass in nil if you don't need it or pass in an address of an NSUInteger
//      videoLinkStatus:
//                  0 = No Link (i.e. Link dropped during the CRC test)
//                  1 = DVI Link established
//                  2 = HDMI1.x Link established
//                  3 = HDMI2.x Link established
//      linkdroppedFrameNumber:
//                   Frame number on which HDMI Link dropped
// return value
// BOOL:	YES = successed with no Error. The Function doesn't check the CRCs.
//          NO  = Error occured;

- (BOOL) hdmiCRCWithNumOfFrames: (NSUInteger) numOfFrames
                  expectedA1CRC: (ATDVideoHDMICrc*) aExpectedA1CRC
                  expectedA2CRC: (ATDVideoHDMICrc*) aExpectedA2CRC
                          A1CRC: (ATDVideoHDMICrc**) aA1CRCResult
                          A2CRC: (ATDVideoHDMICrc**) aA2CRCResult
            andMismatchedFrames: (NSUInteger*) numOfMismatchedFrames
             andVideoLinkStatus: (NSUInteger*)  videoLinkStatus
          andDroppedFrameNumber: (NSUInteger*) linkdroppedFrameNumber
                       andError: (NSError**) aError;

// Get Video Timing info on the incoming HDMI Stream
// parameters
//  aTimingInfo:output  can't be nil.
// return value
// BOOL:	YES = successed with no Error. The Function doesn't check the CRCs.
//          NO  = Error occured;
- (BOOL) hdmiTimingInfo:  (ATDHDMITimingInfoData*) aTimingInfo
               andError: (NSError**) aError;


//Get the AVI InfoFrame data from HDMI Source
// parameters
//  aAVIINfo  can't be nil.
- (BOOL) hdmiAVIInfoFrameData: (ATDAVIInfoFrameData*) aAVIInfo
                     andError: (NSError**) aError;

//Toggle HDMI HPD
- (BOOL) toggleHdmiHPDWithError: (NSError**) aError;

//Set HDMI HPD High or Low
// parameters
//      high:input   set High to YES for (HIGH) or setHigh to NO (LOW)
- (BOOL) assertHdmiHPD: (BOOL) high andError: (NSError**) aError;

// Query HDMI HPD state
// return value
//  0 = HPD Low, 1 = HPD High
- (NSInteger) hdmiHPDModeWithError: (NSError**) aError;

//Get the HDCP functionality info on HDMI IN port
// parameters
//  funcInfo  can't be nil.
// return value
// BOOL:	YES = successed with no Error.
//          NO  = Error occured;
- (BOOL) hdmiHDCPFunctionalityInfo: (ATDHdcpFunctionalityInfo*) funcInfo
                          andError: (NSError**) aError;
// Set HDMI CEC Low or High
// parameters
//      high:input   set High to YES for (HIGH) or setHigh to NO (LOW)
- (BOOL) assertHdmiCEC: (BOOL) high andError: (NSError**) aError;

// Query HDMI CEC state
// return value
//  0 = CEC Low, 1 = CEC High
- (NSInteger) hdmiCECStateWithError: (NSError**) aError;

//Register 110 (0x6E) - Radon Video Mode State
- (NSInteger) videoModeStateWithError: (NSError**) aError;

- (NSInteger) readCEC: (NSError**) aError;



@end
