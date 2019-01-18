//
//  ATDeviceVideoParameterStructs.h
//  ATDeviceElements
//
//  Created by Sai  on 9/7/16.
//  Copyright © 2016 htwe. All rights reserved.
//

#ifndef ATDeviceVideoParameterStructs_h
#define ATDeviceVideoParameterStructs_h



#define kATDHDMIcrcDataSize 13
#define kATDHDMIcrcWriteDataSize 8


#pragma pack(push, 1)  //  pack aligment to 1 = no padding
typedef union {
    uint8_t data[kATDHDMIcrcDataSize];
    
    // in
    struct {
        uint16_t a1ExpectedRedGreenCRC;
        uint16_t a1ExpectedBlueGreenCRC;
        uint16_t a2ExpectedRedGreenCRC;
        uint16_t a2ExpectedBlueGreenCRC;
    };
    
    // out
    struct {
        uint16_t numOfMismatched;
        uint16_t a1CalculatdedRedGreenCRC;
        uint16_t a1CalculatdedBlueGreenCRC;
        uint16_t a2CalculatdedRedGreenCRC;
        uint16_t a2CalculatdedBlueGreenCRC;
        uint8_t  videoLinkStatus;
        uint16_t linkdroppedFrameNumber;
    };
} ATDHDMICrcData;


typedef struct {
    uint8_t VideoLinkStatus;
    uint8_t ScanningMethod;
    uint8_t HSYNC_Polarity;
    uint8_t VSYNC_Polarity;
    uint32_t PixelFrequencry;
    
    uint16_t vTotal;
    uint16_t vActive;
    uint16_t vSync;
    uint16_t vFrontPorch;
    uint16_t hTotal;
    uint16_t hActive;
    uint16_t hSync;
    uint16_t hFrontPorch;
    
} ATDHDMITimingInfoData;



typedef struct {
    uint8_t VideoResolutionID;
    uint8_t a3DMode;
    uint8_t PictureAspectRadio;
    uint8_t PixelRepetition;
    uint8_t SpaceColorimetryQuantRange;
    uint8_t ChromaSampling;
    uint8_t BitDepth;
    uint8_t NonUniformPictureScaling;
    uint8_t ScanInfo;
    uint8_t ITContentType;
    uint8_t ITContentFlag;
    uint8_t ActiveFormatFlag;
    uint8_t VerticalBarInfoValid;
    uint8_t HorizontalBarInfoValid;
    uint16_t VerticalBarInfoLineNumOfEndOfTopBar;
    uint16_t VerticalBarInfoLineNumOfStartOfBottomBar;
    uint16_t HorizontalBarInfoPixelNumOfEndOfLeftBar;
    uint16_t HorizontalBarInfoPixelNumOfStartOfRightBar;
    
} ATDAVIInfoFrameData;


typedef struct {
  
    uint8_t     HDCPAccessStatus;
    uint8_t     HDCPAuthenticationStatus;
    uint32_t    RxIDKey1to4Byte;
    uint8_t     RxIDKey5Byte;
    uint32_t    BKSVKey1to4Byte;
    uint8_t     BKSVKey5Byte;
    uint8_t     LocalContentProtectionTX0Status;
    uint8_t     LocalContentProtectionTX1Status;
    uint8_t     LocalContentProtectionTX2Status;
    
    
} ATDHdcpFunctionalityInfo;





#pragma pack(pop)

#endif /* ATDeviceRadonStructs_h */
