//
//  ATDevicePalladium.h
//  ATDeviceElements
//
//  Created by Sai  on 3/15/17.
//  Copyright © 2017 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>

#import <ATDeviceElements/ATDeviceUSBC.h>
#import <ATDeviceElements/ATDeviceParameters.h>

@interface ATDevicePalladium : ATDeviceUSBC

// Get the RG & BG CRC Values on incoming HDMI Streams on A1 and A2 for specified frames
//
// return value
// ATDeviceDisplayPortLinkStatus:
//           BOOL      statusPassed;
//           NSInteger cedarP0laneCount;
//           NSInteger cedarP0linkBandwidthGbps;
//           NSInteger cedarP0status;
//           NSInteger cedarP1laneCount;
//           NSInteger cedarP1linkBandwidthGbps;
//           NSInteger cedarP1status;
//           NSData * rawData; Data from back from the Palladium. They match what in the User Manual
- (ATDeviceDisplayPortLinkStatus*) displayPortLinkStatusWithError: (NSError**) aError;

// return value
// ATDeviceDisplayPortSymbolErrorCount:
//      NSInteger totalErrorCount;
//      NSInteger cedarP0ErrorCount;
//      NSInteger cedarP1ErrorCount;
//      NSInteger cedarP0Lane0ErrorCount;
//      NSInteger cedarP0Lane1ErrorCount;
//      NSInteger cedarP0Lane2ErrorCount;
//      NSInteger cedarP0Lane3ErrorCount;
//      NSInteger cedarP1Lane0ErrorCount;
//      NSInteger cedarP1Lane1ErrorCount;
//      NSInteger cedarP1Lane2ErrorCount;
//      NSInteger cedarP1Lane3ErrorCount;
- (ATDeviceDisplayPortSymbolErrorCount*) displayPortSymbolErrorCountWithDurationInMilliSeconds: (NSUInteger) duration
                                                                                      andError: (NSError**) aError;

/** symbolErrorCountWithDurationInMilliSeconds
 * brief getting the symbol error counts for all lanes from the Test Device. This function is the same as displayPortSymbolErrorCountWithDurationInMilliSeconds .
 *
 * param numFrames:           duration
 * param[out] aError: nil = NO error, or error set. Error code is defined in <ATDeviceElements/ATDeviceCarbonErrors.h>
 * retval ATDeviceSymbolErrorCount:      the Struct of symbol error counts for all lanes
 *
 */
- (ATDeviceSymbolErrorCount *) symbolErrorCountWithDurationInMilliSeconds: (NSUInteger) duration
                                                                 andError: (NSError**) aError;


- (ATDeviceColorCRC*) displayPortSymbolCRCWithNumberOfFrames: (uint16_t) numFrames
                                          expectedCedarP0Red: (uint16_t) expectedCedarP0Red
                                        expectedCedarP0Green: (uint16_t) expectedCedarP0Green
                                         expectedCedarP0Blue: (uint16_t) expectedCedarP0Blue
                                          expectedCedarP1Red: (uint16_t) expectedCedarP1Red
                                        expectedCedarP1Green: (uint16_t) expectedCedarP1Green
                                         expectedCedarP1Blue: (uint16_t) expectedCedarP1Blue
                                                       error: (NSError**) aError;
/** imageCRCWithNumberOfFrames
 * brief getting the CRC from the Test Device. This function is the same as displayPortSymbolCRCWithNumberOfFrames.
 *
 * param numFrames:           Number frames to capture
 * param expectedDP0Red:         expected DPRX0 Red
 * param expectedDP0Green:       expected DPRX0 Green
 * param expectedDP0Blue:        expected DPRX0 Blue
 * param expectedDP1Red:         expected DPRX1 Red
 * param expectedDP1Green:       expected DPRX1 Green
 * param expectedDP1Blue:        expected DPRX1 Blue
 * param[out] aError: nil = NO error, or error set. Error code is defined in <ATDeviceElements/ATDeviceCarbonErrors.h>
 * retval ATDeviceColor32bitCRC:      the Struct of the CRC.
 *
 */
- (ATDeviceColor32bitCRC*)  imageCRCWithNumberOfFrames: (uint16_t) numFrames
                                        expectedDP0Red: (uint32_t) expectedDP0Red
                                      expectedDP0Green: (uint32_t) expectedDP0Green
                                       expectedDP0Blue: (uint32_t) expectedDP0Blue
                                        expectedDP1Red: (uint32_t) expectedDP1Red
                                      expectedDP1Green: (uint32_t) expectedDP1Green
                                       expectedDP1Blue: (uint32_t) expectedDP1Blue
                                                 error: (NSError**) aError;

@end
