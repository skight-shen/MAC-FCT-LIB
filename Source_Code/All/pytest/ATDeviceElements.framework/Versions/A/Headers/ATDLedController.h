//
//  ATDLedController.h
//  LEDdevices
//
//  Created by Sai  on 12/6/16.
//  Copyright © 2016 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "ATDPDDevice.h"

typedef NS_ENUM(uint32_t, ATDLedId) {
    ATDLedId_1 = 1,
    ATDLedId_2 = 2,
    ATDLedId_3 = 3,
};

typedef NS_ENUM(uint32_t, ATDLedColor) {
    ATDLedCOMBINED_DCSD_OFF= 0,
    ATDLedCOMBINED_DCSD_RED = 1,
    ATDLedCOMBINED_DCSD_YELLOW = 2,
    ATDLedCOMBINED_DCSD_GREEN= 3,
};

typedef NS_ENUM(uint32_t, ATDLedState) {
    ATDLedState_OFF= 0,
    ATDLedState_ON = 1,
    ATDLedState_SLOW = 2,
    ATDLedState_FAST = 3,
};

@interface ATDLedController : ATDPDDevice

//----------------------------------------
//    Open the LED Device
//----------------------------------------
//  will try both SOP and SOP'
- (BOOL) openLEDControllerWithError:(NSError **) error;

//  try to talk to SOP only
- (BOOL) openLEDControllerTargetSopWithError:(NSError **) error;

//  try to talk to SOP' (Cable Plug) only.
- (BOOL) openLEDControllerTargetSopPrimeWithError:(NSError **) error;


//----------------------------------------
//    Change the LED colors
//----------------------------------------
- (BOOL) changeCombinedDcsdLED: (ATDLedId) led andColor:(ATDLedColor) ledColor andState: (ATDLedState) state andError:(NSError **) error;

- (BOOL) changeDcsdLED: (ATDLedId)led andState: (ATDLedState) state andError:(NSError **) error;

//----------------------------------------
//    Set the TimeOut
//    Host is required to reset the timeout before it times out. When it times out, a red LED will blink on some devices
//----------------------------------------

- (BOOL) resetTimeOutInMilliseconds: (uint32_t) milliseconds andError:(NSError **) error;

@end
