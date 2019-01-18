//
//  ATDCTDRegisters.h
//  ATDeviceElements
//
//  Created by Sai  on 9/7/16.
//  Copyright © 2016 htwe. All rights reserved.
//

#ifndef ATDCTDRegisters_h
#define ATDCTDRegisters_h



typedef NS_ENUM(uint32_t, ATDCTDIRegsitersMap) {
    ATDCTDIRegVendorID                  = 0,
    ATDCTDIRegDeviceID                  = 0x01,
    ATDCTDIRegProtoVer                  = 0x02,
    ATDCTDIRegMode                      = 0x03,
    ATDCTDIDataReadActualLengthReg      = 0x0A,
    ATDCTDIRegVersion                   = 0x0F,
    ATDCTDIRegIDPageLock                = 0x16,
    ATDCTDIRegVendorSerialNum           = 0x17,
    ATDCTDIRegDeviceUpTime              = 0x19,
    ATDCTDIRegLifeTimeUpTime            = 0x1A,
    ATDCTDIRegModeStatus                = 0x1C,
    ATDCTDIRegAppleSerialNum            = 0x23,
    ATDCTDIRegGalliumPresence           = 0x40,
    ATDCTDIRegPortStatus                = 0x41,
    ATDCTDIRegNegotiatedContract        = 0x47,
    ATDCTDIRegCCLineConfig              = 0x48,
    ATDCTDIRegExtraP1SourceCapability   = 0x50,
    ATDCTDIRegExtraP1SinkCapability     = 0x51,
    ATDCTDIRegExtraP2SourceCapability   = 0x52,
    ATDCTDIRegExtraP2SinkCapability     = 0x53,
   
};


typedef NS_ENUM(uint32_t, ATDCTDIRadonRegsitersMap) {

    ATDCTDIVideoModeState = 0x6E,
    
};

#define kATDCTDIRegDefaultSize 4

#endif /* ATDCTDRegisters_h */
