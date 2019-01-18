//
//  ATDCCGDevice.h
//  ATDeviceElements
//
//  Created by Corey Lange on 1/3/17.
//  Copyright © 2017 htwe. All rights reserved.
//

#import <ATDeviceElements/ATDeviceElements.h>

typedef NS_ENUM(uint8_t, CCGDeviceMode) {
    BOOT_MODE = 0,
    FAILSAFE_MODE,
    MAIN_FW_MODE,
};

typedef NS_ENUM(uint8_t, CCGFirmwareType) {
    FAILSAFE_FW = 1,
    MAIN_FW = 2
};

typedef NS_ENUM(uint8_t, CCGSerialNumberType) {
    APPLE_SN = 1,
    BINARY_UUID,
    ASCII_UUID,
    VENDOR_SN
};

@interface ATDCCGDevice : ATDPDDevice

//  will try both SOP and SOP'
- (BOOL) openCCGWithError:(NSError **) error;

//  try to talk to SOP only
- (BOOL) openCCGTargetSopWithError:(NSError **) error;

//  try to talk to SOP' (Cable Plug) only.
- (BOOL) openCCGTargetSopPrimeWithError:(NSError **) error;

//
// Update Functions
//
- (BOOL) enterUpdateModeWithError:(NSError**)error;

- (BOOL) getCCGDeviceMode:(CCGDeviceMode*)mode withError:(NSError**)error;

- (BOOL) jumpToBootloaderWithError:(NSError**)error;

- (BOOL) enterFlashingModeWithError:(NSError**)error;

- (BOOL) writeFlashRow:(uint16_t)row_number withData:(uint8_t*)data ofSize:(uint8_t)size withError:(NSError**)error;

- (BOOL) validateFirmware:(CCGFirmwareType)type withError:(NSError**)error;

- (BOOL) resetDeviceWithError:(NSError**)error;

- (BOOL) getConfigTableChecksum:(uint32_t*)checksum fromRow:(uint16_t)starting_row withError:(NSError**)error;

- (BOOL) getDeviceVersions:(uint32_t*)versions withError:(NSError**)error;

- (BOOL) getSiliconID:(uint32_t*)siliconId withError:(NSError**)error;

- (BOOL) getReasonForBoot:(uint32_t*)reason withError:(NSError**)error;

- (BOOL) readFlashRow:(uint16_t)row_number intoData:(uint8_t*)data withError:(NSError**)error;

//
// Serial Number Functions
//
- (BOOL) supportsAppleSerialNumberModeWithError:(NSError**)error;

- (BOOL) writeAppleSerialNumber:(NSString*)serialNumber lockAfterWrite:(BOOL)lock withError:(NSError**)error;

- (BOOL) writeVendorSerialNumber:(NSString*)serialNumber lockAfterWrite:(BOOL)lock withError:(NSError**)error;

- (BOOL) getSerialNumberOfType:(CCGSerialNumberType)type intoString:(NSString**)string withError:(NSError**)error;

@end
