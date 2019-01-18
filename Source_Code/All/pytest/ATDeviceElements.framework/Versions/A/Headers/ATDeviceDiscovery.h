//
//  ATDeviceDiscovery.h
//  ATDeviceElements
//
//  Created by Sai  on 8/23/17.
//  Copyright © 2017 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>



@interface ATDeviceDiscovery : NSObject

/** deviceSerialPathForCircuitNumber
 * brief find the first ATDevice USB Devices (endpoint0 e.g. Potassium or Sodium) that matches circuit Number.
 *
 * param[in] circuitNum:     circuit Number
 * param[out] aError: nil = NO error, or error set if any device iterating has error. Error code is defined in <ATDeviceElements/ATDeviceCarbonErrors.h>
 * retval NSString:           return the string in /dev/cu.xxxx device.
 *
 *
 */
+(NSString*) deviceSerialPathForCircuitNumber: (uint8_t) circuitNum
                                     andError: (NSError**) aError;

/** findSerialPath
 * brief find the first ATDevice USB Devices (endpoint0 e.g. Potassium or Sodium) that matches  circuit Number and set the serialPath and USBLocationID
 *
 * param[out] serialPath:        this serialPath value will be set by the function. pass nil if you don't need it
 * param[out] usbLocationID:    this usbLocationID value will be set by the function pass nil if you don't need it
 * param[in] circuitNum:     circuit Number
 * param[out] aError: nil = NO error, or error set if any device iterating has error. Error code is defined in <ATDeviceElements/ATDeviceCarbonErrors.h>
 * retval NSString:           return the string in /dev/cu.xxxx device.
 *
 *
 */
+(BOOL)     findSerialPath: (NSString**) serialPath
          andUSBLocationID: (uint32*) usbLocationID
          forCircuitNumber: (uint8_t) circuitNum
                  andError: (NSError**) aError;
@end
