//
//  ATDeviceParameters.h
//  ATDeviceElements
//
//  Created by Sai  on 9/6/16.
//  Copyright © 2016 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "ATDeviceVideoParameterStructs.h"
#import "ATDeviceCarbonConnectorChecker.h"

typedef NS_ENUM(uint8_t, ATDCarbonEuropeanPinConfigType) {

    ATDCarbonDontConfigure = 0,
    GPIO_Mode_IN_25MHz_PP_NoPull, //1
    GPIO_Mode_IN_50MHz_PP_NoPull,  //2
    GPIO_Mode_IN_25MHz_PP_PullDown, //3 default
    GPIO_Mode_IN_50MHz_PP_PullDown,  //4
    GPIO_Mode_IN_25MHz_PP_PullUp,   // 5 default
    GPIO_Mode_IN_50MHz_PP_PullUp,   //6
    
    GPIO_Mode_OUT_25MHz_PP_NoPull_Init0, //7
    GPIO_Mode_OUT_25MHz_PP_NoPull_Init1,  //8
    GPIO_Mode_OUT_25MHz_PP_PullDown_Init0, //9
    GPIO_Mode_OUT_25MHz_PP_PullUp_Init1,   //10
    
    GPIO_Mode_OUT_50MHz_PP_NoPull_Init0,//11
    GPIO_Mode_OUT_50MHz_PP_NoPull_Init1,//12
    GPIO_Mode_OUT_50MHz_PP_PullDown_Init0,//13
    GPIO_Mode_OUT_50MHz_PP_PullUp_Init1,//14
    
    GPIO_Mode_OUT_100MHz_PP_NoPull_Init0,//15
    GPIO_Mode_OUT_100MHz_PP_NoPull_Init1,//16
    GPIO_Mode_OUT_100MHz_PP_PullDown_Init0,//17
    GPIO_Mode_OUT_100MHz_PP_PullUp_Init1,//18
    
    GPIO_Mode_AF_PP_NoPull_GPIO_AF_USART1,  //19 //GPIO_AF_USART1
    GPIO_Mode_AF_PP_NoPull_GPIO_AF_USART2,  //20
    GPIO_Mode_AF_PP_NoPull_GPIO_AF_USART3,   //21
    GPIO_Mode_AF_PP_NoPull_GPIO_AF_UART4,   //22
    GPIO_Mode_AF_PP_NoPull_GPIO_AF_UART5,   //23
    GPIO_Mode_AF_PP_NoPull_GPIO_AF_USART6,  //24
    
    GPIO_Mode_AF_PP_NoPull_GPIO_AF_SPI2,  //25
    GPIO_Mode_AF_PP_NoPull_GPIO_AF_SPI3,   //26
    
    GPIO_Mode_AF_OD_NoPull_GPIO_AF_I2C1,  //27
    GPIO_Mode_AF_OD_NoPull_GPIO_AF_I2C2,   //28
    
    GPIO_Mode_AF_PP_NoPull_GPIO_AF_CAN1,  //29
    GPIO_Mode_AF_PP_NoPull_GPIO_AF_CAN2,  //30
    
    GPIO_Mode_AN_AnalogIO,  //31
    
    GPIO_Mode_OUT_25MHz_OD_NoPull, //32 Open drain
    
    ATDCarbonNumOfPortConfigType,
};


typedef NS_ENUM(uint8_t, ATDDisplayPortTxRx){
    
    ATDDisplayPortTX = 0,
    ATDDisplayPortRx
    
};



typedef NS_ENUM(uint32_t, ATDeviceUSBSpeed) {
    ATDeviceUSBLowSpeed   = 0,
    ATDeviceUSBFullSpeed  ,
    ATDeviceUSBHighSpeed  ,
    ATDeviceUSBSuperSpeed ,
    ATDeviceUSBDisconnect
};


typedef NS_ENUM(uint8_t, ATDeviceUSBSelectedIC) {
    ATDeviceUSBFX3            = 0,
    ATDeviceUSBLegacyAce      ,
    ATDeviceUSBSSPlusAceAR    ,
    ATDeviceUSBASMedia        ,
    ATDeviceUSBW5500          ,
    ATDeviceUSBLPC11
};


typedef NS_ENUM(uint32_t, ATDeviceCaesiumSpeed) {
    ATDeviceCaesiumLowSpeed         = 0,
    ATDeviceCaesiumFullSpeed        = 1,
    ATDeviceCaesiumHighSpeed        = 2,
    ATDeviceCaesiumSuperSpeed       = 3,
    ATDeviceCaesiumSuperSpeedPlus   = 4,
    ATDeviceCaesiumDisconnect       = 0xFF
};


typedef NS_ENUM(uint8_t, ATDeviceCaesiumSelectedIC) {
    ATDeviceCaesiumFX3          = 0,
    ATDeviceCaesiumASMedia      = 1,
    ATDeviceCaesiumLSController = 2,
    ATDeviceCaesiumAce          = 3,
    ATDeviceCaesiumW5500        = 4,
    ATDeviceCaesiumSATA         = 5,
};

typedef NS_ENUM(uint8_t, ATDeviceBananaUSBState) {
    ATDeviceBananaUnconnected   = 0,
    ATDeviceBananaDefault       = 1,
    ATDeviceBananaAddressed     = 2,
    ATDeviceBananaConfigured    = 3,
    ATDeviceBananaSuspended     = 4,
};

typedef NS_ENUM(uint8_t, ATDeviceModifierKeys) {
    ATDeviceModifierKeyLeftControl  = 1,
    ATDeviceModifierKeyLeftShift    = 2,
    ATDeviceModifierKeyLeftOption   = 4,
    ATDeviceModifierKeyLeftCommand  = 8,
    ATDeviceModifierKeyRightControl = 16,
    ATDeviceModifierKeyRightShift   = 32,
    ATDeviceModifierKeyRightOption  = 64,
    ATDeviceModifierKeyRightCommand = 128,
};

typedef NS_ENUM(uint8_t, ATDeviceSpecialKeys) {
    ATDeviceSpecialKeyPlayPause     = 1,
    ATDeviceSpecialKeyNextTrack     = 2,
    ATDeviceSpecialKeyPrevTrack     = 4,
    ATDeviceSpecialKeyEject         = 8,
    ATDeviceSpecialKeyMute          = 16,
    ATDeviceSpecialKeyVolumeDown    = 32,
    ATDeviceSpecialKeyVolumeUp      = 64,
};



typedef struct{
    uint8 row, column;
} ATDEuroConnectorLocation;

typedef struct{
    ATDEuroConnectorLocation MOSI;
    ATDEuroConnectorLocation MISO;
    ATDEuroConnectorLocation SCK;
    ATDEuroConnectorLocation SS;
} ATDEuroConnectorSPILocation;

typedef struct{
    ATDEuroConnectorLocation SDA;
    ATDEuroConnectorLocation SCL;
} ATDEuroConnectorI2cLocation;


@interface ATDVideoHDMICrc : NSObject

- (id) initWithRedGreenCRC: (NSNumber*) aRedGreenCRC andBlueGreenCRC: (NSNumber*) aBlueGreenCRC;

@property (nonatomic, strong) NSNumber* RedGreenCRC;
@property (nonatomic, strong) NSNumber* BlueGreenCRC;
@end




@interface ATDCarbonEuropeanConnectorPin : NSObject

//initWithRow
// Args:
//      Row can be 'A', 'B', or 'C'
//      pin can between 1 to 32.
//
// Return:
//  Invalid pin or Row will return nil.
//
- (id) initWithRow: (ATCarbonEuropeanConnectorRow) aRow andPin: (int) aPin andType: (ATDCarbonEuropeanPinConfigType) aType;

@property (nonatomic) unsigned int row; // 0 based . 0 = A, 1 = B, 2 = C
@property (nonatomic) unsigned int pin; // 1 based and total 32
@property (nonatomic) unsigned int index; // total 96
@property (nonatomic) ATDCarbonEuropeanPinConfigType type;

@end



@interface ATDCarbonEuropeanConnector : NSObject
// Args:
//      Row can be 'EuropeanPortRowA', 'EuropeanPortRowB', or 'EuropeanPortRowC'  Must be Upper case.
//      pin can between 1 to 32.
//      type is one of the ATDCarbonEuropeanPinConfigType
// Return:
//  Invalid pin or Row will return NO.
//
- (BOOL) addPinWithRow: (ATCarbonEuropeanConnectorRow) aRow andPin: (int) aPin andType: (ATDCarbonEuropeanPinConfigType) aType andError: (NSError**) aError;
//
- (BOOL) addPinWithRawData:(uint8_t*)rawData andError: (NSError**) aError ;

- (BOOL) isEqualToConnector: (ATDCarbonEuropeanConnector*) connector;
    // array of ATDCarbonEuropeanConnectorPin
@property (nonatomic, readonly) NSArray* pins;

@end

@interface ATDLogEntry : NSObject

@property (nonatomic) NSUInteger status;
@property (nonatomic) NSInteger entryIndex;
@property (nonatomic) NSUInteger upTime;
@property (nonatomic) NSUInteger lifeTime;
@property (nonatomic, copy) NSString* message; // decoded message if the test device support it

- (id) initWithStatus: (NSUInteger) aStatus
        andEntryIndex: (NSInteger)  aEntryIndex
            andUpTime: (NSUInteger) aUpTime
          andLifeTime: (NSUInteger) aLifeTime
           andMessage: (NSString *) aMessage;

@end



@interface ATDeviceDisplayPortLinkStatus : NSObject

//Overall Status PASSED or FAILED
@property (nonatomic) BOOL      statusPassed;
@property (nonatomic) NSInteger cedarP0laneCount;
@property (nonatomic) NSInteger cedarP0linkBandwidthGbps;
@property (nonatomic) NSInteger cedarP0status;
@property (nonatomic) NSInteger cedarP1laneCount;
@property (nonatomic) NSInteger cedarP1linkBandwidthGbps;
@property (nonatomic) NSInteger cedarP1status;

//The raw data coming back from test device. this matches the Palladium User manual.
@property (nonatomic,strong) NSData * rawData;

- (id) initWithStatusPassed: (BOOL)       aPassed
             andP0LaneCount: (NSInteger)  aP0LaneCount
             andP0BandWidth: (NSInteger)  aP0linkBandwdidth
                andP0Status: (NSUInteger) aP0Status
             andP1LaneCount: (NSInteger)  aP1LaneCount
             andP1BandWidth: (NSInteger)  aP1linkBandwdidth
                andP1Status: (NSUInteger) aP1Status
                 andRawData: (NSData*)    aData;

@end


@interface ATDeviceDisplayPortSymbolErrorCount : NSObject

@property (nonatomic) NSInteger totalErrorCount;
@property (nonatomic) NSInteger cedarP0ErrorCount;
@property (nonatomic) NSInteger cedarP1ErrorCount;
@property (nonatomic) NSInteger cedarP0Lane0ErrorCount;
@property (nonatomic) NSInteger cedarP0Lane1ErrorCount;
@property (nonatomic) NSInteger cedarP0Lane2ErrorCount;
@property (nonatomic) NSInteger cedarP0Lane3ErrorCount;
@property (nonatomic) NSInteger cedarP1Lane0ErrorCount;
@property (nonatomic) NSInteger cedarP1Lane1ErrorCount;
@property (nonatomic) NSInteger cedarP1Lane2ErrorCount;
@property (nonatomic) NSInteger cedarP1Lane3ErrorCount;

- (id) initWithTotalErrorCount: (NSInteger) totalErrCnt
          andCedarP0ErrorCount: (NSInteger) cedarP0ErrCnt
          andCedarP1ErrorCount: (NSInteger) cedarP1ErrCnt
     andCedarP0Lane0ErrorCount: (NSInteger) cedarP0L0ErrCnt
     andCedarP0Lane1ErrorCount: (NSInteger) cedarP0L1ErrCnt
     andCedarP0Lane2ErrorCount: (NSInteger) cedarP0L2ErrCnt
     andCedarP0Lane3ErrorCount: (NSInteger) cedarP0L3ErrCnt
     andCedarP1Lane0ErrorCount: (NSInteger) cedarP1L0ErrCnt
     andCedarP1Lane1ErrorCount: (NSInteger) cedarP1L1ErrCnt
     andCedarP1Lane2ErrorCount: (NSInteger) cedarP1L2ErrCnt
     andCedarP1Lane3ErrorCount: (NSInteger) cedarP1L3ErrCnt;

@end



@interface ATDeviceSymbolErrorCount : NSObject

@property (nonatomic) NSInteger dP0Lane0ErrorCount;
@property (nonatomic) BOOL      dP0Lane0CountValid;
@property (nonatomic) NSInteger dP0Lane1ErrorCount;
@property (nonatomic) BOOL      dP0Lane1CountValid;
@property (nonatomic) NSInteger dP0Lane2ErrorCount;
@property (nonatomic) BOOL      dP0Lane2CountValid;
@property (nonatomic) NSInteger dP0Lane3ErrorCount;
@property (nonatomic) BOOL      dP0Lane3CountValid;

@property (nonatomic) NSInteger dP1Lane0ErrorCount;
@property (nonatomic) BOOL      dP1Lane0CountValid;
@property (nonatomic) NSInteger dP1Lane1ErrorCount;
@property (nonatomic) BOOL      dP1Lane1CountValid;
@property (nonatomic) NSInteger dP1Lane2ErrorCount;
@property (nonatomic) BOOL      dP1Lane2CountValid;
@property (nonatomic) NSInteger dP1Lane3ErrorCount;
@property (nonatomic) BOOL      dP1Lane3CountValid;

- (id) initWithDPLane0ErrorCount: (NSInteger)   aDP0Lane0ErrorCount
           andDP0Lane0CountValid: (BOOL)        aDP0Lane0CountValid
          andaDP0Lane1ErrorCount: (NSInteger)   aDP0Lane1ErrorCount
           andDP0Lane1CountValid: (BOOL)        aDP0Lane1CountValid
          andaDP0Lane2ErrorCount: (NSInteger)   aDP0Lane2ErrorCount
           andDP0Lane2CountValid: (BOOL)        aDP0Lane2CountValid
          andaDP0Lane3ErrorCount: (NSInteger)   aDP0Lane3ErrorCount
           andDP0Lane3CountValid: (BOOL)        aDP0Lane3CountValid

          andaDP1Lane0ErrorCount: (NSInteger)   aDP1Lane0ErrorCount
           andDP1Lane0CountValid: (BOOL)        aDP1Lane0CountValid
          andaDP1Lane1ErrorCount: (NSInteger)   aDP1Lane1ErrorCount
           andDP1Lane1CountValid: (BOOL)        aDP1Lane1CountValid
          andaDP1Lane2ErrorCount: (NSInteger)   aDP1Lane2ErrorCount
           andDP1Lane2CountValid: (BOOL)        aDP1Lane2CountValid
          andaDP1Lane3ErrorCount: (NSInteger)   aDP1Lane3ErrorCount
           andDP1Lane3CountValid: (BOOL)        aDP1Lane3CountValid;

@end






@interface ATDeviceColorCRC : NSObject
@property (nonatomic) NSInteger numberOfMisMatched;
@property (nonatomic) uint16_t cedarP0RedCRC;
@property (nonatomic) uint16_t cedarP0GreenCRC;
@property (nonatomic) uint16_t cedarP0BlueCRC;
@property (nonatomic) uint16_t cedarP1RedCRC;
@property (nonatomic) uint16_t cedarP1GreenCRC;
@property (nonatomic) uint16_t cedarP1BlueCRC;


- (id) initWithMisMatched: (NSInteger) numMisMatch
             andCedarP0RCRCRed: (uint16_t) cedarP0RedCRC
            andCedarP0CRCGreen: (uint16_t) cedarP0GreenCRC
             andCedarP0CRCBlue: (uint16_t) cedarP0BlueCRC
             andCedarP1RCRCRed: (uint16_t) cedarP1RedCRC
            andCedarP1CRCGreen: (uint16_t) cedarP1GreenCRC
             andCedarP1CRCBlue: (uint16_t) cedarP1BlueCRC;
@end

@interface ATDeviceColor32bitCRC : NSObject
@property (nonatomic) NSInteger numberOfMisMatched;
@property (nonatomic) uint32_t dPRX0RedCRC;
@property (nonatomic) uint32_t dPRX0GreenCRC;
@property (nonatomic) uint32_t dPRX0BlueCRC;
@property (nonatomic) uint32_t dPRX1RedCRC;
@property (nonatomic) uint32_t dPRX1GreenCRC;
@property (nonatomic) uint32_t dPRX1BlueCRC;


- (id) initWithMisMatched: (NSInteger) numMisMatch
            andDP0RCRCRed: (uint32_t) aDP0RedCRC
           andDP0CRCGreen: (uint32_t) aDP0GreenCRC
            andDP0CRCBlue: (uint32_t) aDP0BlueCRC
            andDP1RCRCRed: (uint32_t) aDP1RedCRC
           andDP1CRCGreen: (uint32_t) aDP1GreenCRC
            andDP1CRCBlue: (uint32_t) aDP1BlueCRC;

- (id) initWithATDeviceColorCRC: (ATDeviceColorCRC*) crc;
@end


