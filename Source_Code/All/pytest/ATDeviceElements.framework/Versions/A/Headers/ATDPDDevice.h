//
//  ATPDDevice.h
//  ATPDDevice
//
//  Created by Sai  on 12/13/16.
//  Copyright © 2016 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>

@class AppleHPMUserClient;

@interface ATDPDDevice : NSObject
{
    @protected
    uint32_t deviceAddress;
    AppleHPMUserClient * pdClient;
}

- (id)  initWithRid:(uint8_t)rid
           andRoute: (uint64_t) route
   andDeviceAddress: (uint32_t) address;


// Default device address will be 0
- (id)  initWithRid:(uint8_t)rid
           andRoute: (uint64_t) route;

- (BOOL) openWithError:(NSError **) error;

- (IOReturn)registerWrite:(void*)buffer
                 ofLength:(uint64_t)length
                atAddress:(uint32_t)address;

- (IOReturn)registerRead:(void*)buffer
                ofLength:(uint64_t)length
               atAddress:(uint32_t)address
     andActualReadLength:(uint64_t*)read_length;

- (IOReturn)executeIECSCommand:(uint32)command;

- (BOOL) close;

@end
