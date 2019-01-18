//
//  ATDeviceMCUCommon.h
//  ATDeviceElements
//
//  Created by sai on 2/23/17.
//  Copyright © 2017 htwe. All rights reserved.
//

#ifndef ATDeviceMCUCommon_h
#define ATDeviceMCUCommon_h

typedef NS_ENUM(uint8_t, ATCarbonADCResolutions) {
    CarbonADC_Resolution_12b       = 0,
    CarbonADC_Resolution_10b,
    CarbonADC_Resolution_8b,
    CarbonADC_Resolution_6b,
    NumOfCarbonADC_Resolution
};

typedef NS_ENUM(uint8_t, ATCarbonI2CAckAddressMode) {
    CarbonI2C_AckAddress_7bit       = 0,
    CarbonI2C_AckAddress_10bit,
    NumOfCarbonI2CAckAddressMode
};

typedef NS_ENUM(uint8_t, ATCarbonI2CMode) {
    CarbonI2C_Mode_I2C       = 0,
    CarbonI2C_Mode_SMBusDevice,
    CarbonI2C_Mode_SMBusHost,
    NumOfCarbonI2CMode
};

typedef NS_ENUM(uint8_t, ATCarbonUARTwordLength) {
    CarbonUART_WordLength_8B =0,
    CarbonUART_WordLength_9B,
    NumOfCarbonUartWordLength
};

typedef NS_ENUM(uint8_t, ATCarbonUARTStopBitType) {
    CarbonUART_StopBits_1 =0,
    CarbonUART_StopBits_0_5,
    CarbonUART_StopBits_2,
    CarbonUART_StopBits_1_5,
    NumOfCarbonUartStopBitsType
};

typedef NS_ENUM(uint8_t, ATCarbonUARTParityType) {
    CarbonUART_Parity_None =0,
    CarbonUART_Parity_Even,
    CarbonUART_Parity_Odd,
    NumOfCarbonUartParityType
};

typedef NS_ENUM(uint8_t, ATCarbonUARTFlowControl) {
    CarbonUART_HW_FlowControl_None =0,
    CarbonUART_HW_FlowControl_RTS,
    CarbonUART_HW_FlowControl_CTS,
    CarbonUART_HW_FlowControl_RTS_CTS,
    NumOfCarbonUartFlowControl
};

typedef NS_ENUM(uint8_t, ATCarbonSpiDirection){
    CarbonSPI_Direction_2Lines_FullDuplex = 0,
    CarbonSPI_Direction_2Lines_RxOnly,
    CarbonSPI_Direction_1Line_Rx,
    CarbonSPI_Direction_1Line_Tx,
    NumOfCarbonSPI_Direction
};

typedef NS_ENUM(uint8_t, ATCarbonSpiMode){
    
    CarbonSPI_Mode_Slave= 0,
    CarbonSPI_Mode_Master
};

typedef NS_ENUM(uint8_t, ATCarbonSpiDataSize){
    
    CarbonSPI_DataSize_8b= 0,
    CarbonSPI_DataSize_10b
};

typedef NS_ENUM(uint8_t, ATCarbonSpiCPOL){
    
    CarbonSPI_CPOL_Low= 0,  //Clock Idle = Low
    CarbonSPI_CPOL_High     //Clock Idle = High
};

typedef NS_ENUM(uint8_t, ATCarbonSpiCPHA){
    CarbonSPI_CPHA_1Edge= 0, //Leading Edge Falling edge
    CarbonSPI_CPHA_2Edge//Trailing Edge  Rising Edge
};

typedef NS_ENUM(uint8_t, ATCarbonSpiSS){
    
    CarbonSPI_NSS_Hardware= 0, // Use STM32's defined Pin to do Chip Select
    CarbonSPI_NSS_Software  // using spiTransferWithBusId's port and pin to do Chip Select
};


typedef NS_ENUM(uint8_t, ATCarbonSpiFirstBit){
    
    CarbonSPI_FirstBit_MSB= 0,
    CarbonSPI_FirstBit_LSB
};
typedef NS_ENUM(uint8_t, ATCarbonSpiBaudRate){
    
    CarbonSPI_BaudRatePrescaler_21MHz =0,
    CarbonSPI_BaudRatePrescaler_10_5MHz,
    CarbonSPI_BaudRatePrescaler_5_25MHz,
    CarbonSPI_BaudRatePrescaler_2_63MHz,
    CarbonSPI_BaudRatePrescaler_1_31MHz,
    CarbonSPI_BaudRatePrescaler_656kHz,
    CarbonSPI_BaudRatePrescaler_328kHz,
    CarbonSPI_BaudRatePrescaler_164kHz,
    NumOFCarbonSPI_BaudRate,
};


typedef NS_ENUM(uint8_t, ATDeviceCanBusMode){

    ATD_CANBusModeNormal = 0,
    ATD_CANBusModeLoopBack,
    ATD_CANBusModeSilent,
    ATD_CANBusModeSilentLoopBack, //loopback combined with silent mode
};

typedef NS_ENUM(uint8_t, ATDeviceCanBusMessageType){
    
    ATD_CANBusStandard11Bit = 0x0,
    ATD_CANBusExtended29Bit = 0x00000004
};

#endif /* ATDeviceMCUCommon_h */
