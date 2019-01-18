//
//  ATDeviceDust.h
//  ATDeviceElements
//
//  Created by Sai  on 2/3/17.
//  Copyright © 2017 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "ATDeviceElement.h"


typedef NS_ENUM(uint32_t, ATDeviceDustUSBPortMask) {
    
    ATDeviceDustUSBPortAllOff   = 0x00,
    ATDeviceDustUSBPort_1_On    = 0x01,
    ATDeviceDustUSBPort_2_On    = 0x02,
    ATDeviceDustUSBPort_3_On    = 0x04,
    ATDeviceDustUSBPort_4_On    = 0x08,
    ATDeviceDustUSBPort_5_On    = 0x10,
    ATDeviceDustUSBPort_6_On    = 0x20,
    ATDeviceDustUSBPort_7_On    = 0x40,
    ATDeviceDustUSBPort_8_On    = 0x80,
    ATDeviceDustUSBPortAllOn    = 0xFF,
};


@interface ATDeviceDust : ATDeviceElement

// mirageStartStagger
// Turns off all USB outputs on Mirage, and then stagger starts them according to the saved stagger start timing.

- (BOOL) mirageStartStagger: (NSError**) aError;

// mirageSetStaggerDelayInMiliSeconds
// timeInMiliSeconds - is the time that you would like to delay between turning on each successive USB port.
// this function only write to Mirage EEPROM, you will need to call mirageStartStagger after this function.
- (BOOL) mirageSetStaggerDelayInMiliSeconds: (uint32_t) timeInMiliSeconds andError: (NSError**) aError;

// mirageSetUSBOutputs

// Disable All USB Port = 0 or ATDeviceDustUSBPortAllOff
// enable USB Port 1 = 0x01 or ATDeviceDustUSBPort_1_On
// enable USB Port 2 = 0x02 or ATDeviceDustUSBPort_2_On
// enable USB Port 3 = 0x04 or ATDeviceDustUSBPort_3_On
// enable USB Port 4 = 0x08 or ATDeviceDustUSBPort_4_On
// enable USB Port 5 = 0x10 or ATDeviceDustUSBPort_5_On
// enable USB Port 6 = 0x20 or ATDeviceDustUSBPort_6_On
// enable USB Port 7 = 0x40 or ATDeviceDustUSBPort_7_On
// enable USB Port 8 = 0x80 or ATDeviceDustUSBPort_8_On
// enable All USB Port = 0xFF or ATDeviceDustUSBPortAllOn

// usbPortsMask - masks of the eight ports . Each number entered will turn on the corresponding USB port on Mirage. A zero clears all outputs.
// you can use combination of these mask. e.g. TO enable Port 1 and 2, usbPortsMask = ATDeviceDustUSBPort_1_On | ATDeviceDustUSBPort_2_On

//      USB Ports Mapping on Mirage
//  |------------------------------------|
//  |  ====     ====     ====     ====   |
//  |  ====     ====     ====     ====   |
//  |------------------------------------|

//  |------------------------------------|
//  |  =01=     =03=     =05=     =07=   |
//  |  =02=     =04=     =06=     =08=   |
//  |------------------------------------|

- (BOOL) mirageSetUSBOutputs: (uint32_t) usbPortsMask andError: (NSError**) aError;




@end
