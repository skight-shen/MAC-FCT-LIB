//
//  ATDeviceCarbonConnectorChecker.h
//  ATDeviceElements
//
//  Created by Sai  on 9/22/16.
//  Copyright © 2016 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>

#define kNumOfPinInEuropeanRow 32
#define kNumOfPinInWholeConnector 96

typedef NS_ENUM(uint8_t, ATCarbonEuropeanConnectorRow) {
    EuropeanPortRowA       = 0,
    EuropeanPortRowB,
    EuropeanPortRowC,
    NumOfEurpeanRowType,
    
};
typedef NS_ENUM(uint8_t, ATCarbonWriteGPIOType) {
    GPIOwriteHigh       = 1,
    GPIOwriteLow,
    GPIOwriteToggle,
    NumOfWriteType,
    
};

@class ATDCarbonEuropeanConnector;

@interface ATDeviceCarbonConnectorChecker : NSObject

- (BOOL) isThisConfigureOK: (ATDCarbonEuropeanConnector*) connector andError: (NSError**) aError ;

@end
