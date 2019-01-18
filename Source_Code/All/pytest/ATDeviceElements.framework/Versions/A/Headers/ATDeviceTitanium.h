//
//  ATDeviceTitanium.h
//  ATDeviceElements
//
//  Created by Sai  on 8/14/17.
//  Copyright © 2017 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <ATDeviceElements/ATDevicePalladium.h>
#import <ATDeviceElements/ATDeviceParameters.h>

@interface ATDeviceTitanium :  ATDevicePalladium

// Supported Functions inheriated from Palladium
//
//
//- (ATDeviceDisplayPortLinkStatus*) displayPortLinkStatusWithError: (NSError**) aError;
//
//

/** readFPGARegisterAt
 * brief Read FPGA Register register
 *
 * param address:           FPGA Register Address
 * param[out] aError: nil = NO error, or error set. Error code is defined in <ATDeviceElements/ATDeviceCarbonErrors.h>
 * retval uint32_t:         value from FPGA register;
 *
 */
- (uint16_t) readFPGARegisterAt: (NSUInteger) address andError: (NSError**) aError;


/** writeFPGARegisterAt
 * brief write FPGA Register register
 *
 * param address:           FPGA Register Address
 * param writeData:         uint16_t data to write
 * param[out] aError: nil = NO error, or error set. Error code is defined in <ATDeviceElements/ATDeviceCarbonErrors.h>
 * retval BOOL:             Command Sucess or Fail
 *
 */
- (BOOL)    writeFPGARegisterAt: (NSUInteger) address withData:(uint16_t) writeData andError: (NSError**) aError;


/** readDPCDRegisterAt
 * brief Read DPCD register
 *
 * param address:           DP Address
 * param aTxOrRx:           Read DPTt or DPRx
 * param coreSpace:         Set it to YES if reading DP core space
 * param DPRxIndex:         DPRX0 or DPRX1.
 * param[out]               upperReg    upper 64bit of the DPCD register
 * param[out]               lowerReg    lower 64bit of the DPCD register
 * param[out] aError: nil = NO error, or error set. Error code is defined in <ATDeviceElements/ATDeviceCarbonErrors.h>
 * retval uint32_t:         value from DPCD register;
 *
 *
 */
- (BOOL)     readDPCDRegisterAt: (uint32_t) address
                      andTxOrRx: (ATDDisplayPortTxRx) aTxOrRx
                 andIsCoreSpace: (BOOL) coreSpace
                   andDPRXIndex: (NSInteger) DPRxIndex
               andUpperRegister: (uint64_t*) upperReg
               andLowerRegister: (uint64_t*) lowerReg
                       andError: (NSError**) aError;


/** writeDPCDRegisterAt
 * brief write DPCD register
 *
 * param address:           DP Address
 * param writeData:         uint16_t data to write
 * param aTxOrRx:           Read DPTt or DPRx
 * param coreSpace:         Set it to YES if reading DP core space
 * param DPRxIndex:         DPRX0 or DPRX1.
 * param[out] aError: nil = NO error, or error set. Error code is defined in <ATDeviceElements/ATDeviceCarbonErrors.h>
 * retval BOOL:             Command Sucess or Fail
 *
 *
 */

- (BOOL)    writeDPCDRegisterAt: (uint32_t) address
                       withData: (uint16_t) writeData
                      andTxOrRx: (ATDDisplayPortTxRx) aTxOrRx
                 andIsCoreSpace: (BOOL) coreSpace
                   andDPRXIndex: (NSInteger) DPRxIndex
                       andError: (NSError**) aError;

/** imageCRCWithNumberOfFrames
 * brief getting the CRC from the Test Device.
 *
 * param numFrames:           Number frames to capture
 * param expectedDP0Red:         expected DPRX0 Red
 * param expectedDP0Green:       expected DPRX0 Green
 * param expectedDP0Blue:        expected DPRX0 Blue
 * param expectedDP1Red:         expected DPRX1 Red
 * param expectedDP1Green:       expected DPRX1 Green
 * param expectedDP1Blue:        expected DPRX1 Blue
 * param[out] aError: nil = NO error, or error set. Error code is defined in <ATDeviceElements/ATDeviceCarbonErrors.h>
 * retval ATDeviceColor32bitCRC:             the Struct of the CRC
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

/** symbolErrorCountWithDurationInMilliSeconds
 * brief getting the symbol error counts for all lanes from the Test Device.
 *
 * param numFrames:           duration
 * param[out] aError: nil = NO error, or error set. Error code is defined in <ATDeviceElements/ATDeviceCarbonErrors.h>
 * retval ATDeviceSymbolErrorCount:      the Struct of symbol error counts for all lanes
 *
 */
- (ATDeviceSymbolErrorCount *) symbolErrorCountWithDurationInMilliSeconds: (NSUInteger) duration
                                                                 andError: (NSError**) aError;


@end
