//
//  ATDeviceOxygen.h
//  ATDeviceElements
//
//  Created by sai on 2/23/17.
//  Copyright © 2017 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <ATDeviceElements/ATDeviceMCUCommon.h>
#import <ATDeviceElements/ATDeviceExtensionBoard.h>

@class ATDeviceCarbon;

@interface ATDeviceOxygen : ATDeviceExtensionBoard


@property (nonatomic, readonly) NSUInteger eepromLength;

// Oxygen must configure with a controller card such as Carbon.
//
-(BOOL) configureWithCarbon: (nonnull ATDeviceCarbon*) carbon
                   andError: (NSError *_Nullable*_Nullable) aError;

//
// To Attach Extensionboard, you can use Base Class  attachExtensionBoard: (ATDeviceExtensionBoard*) board;
//

//--------------------------------------------------------------
//Read Digital IN
//args:
//  indexOfDIN = DIN 0 to 23
//
- (uint8) readDIO: (uint8) indexOfDIN
         andError: (NSError *_Nullable*_Nullable) aError;

//--------------------------------------------------------------
//Write Digital OUT
//args:
//  indexOfDOUT = DOUT 0 to 15
//  highOrLow YES = High or NO = Low
//
- (BOOL) writeDIO: (uint8)indexOfDOUT
        withValue: (BOOL)high
         andError: (NSError *_Nullable*_Nullable) aError;

//--------------------------------------------------------------
//Check  Bank OK or not
//args:
//      bankIndex can be bank 0 or bank 1.
- (BOOL) isDigitalOutputOKAtBank: (uint8) bankIndex
                        andError: (NSError *_Nullable*_Nullable) aError;


//--------------------------------------------------------------
//Read EUI
//args:
//      None
//return value:
//  NSData of the GUI
//
- (nullable NSData*) readEUI:(NSError *_Nullable*_Nullable) aError;

//--------------------------------------------------------------
//Write EEPROM at Offset
//args:
//      Offset
//      Count
//      Data
- (BOOL) writeEEPROMatOffset: (uint8) offset
                    andCount: (uint8) numBytes
                    withData: (nonnull uint8*) data
                    andError: (NSError *_Nullable*_Nullable) aError;




//--------------------------------------------------------------
//Read EEPROM at Offset
//args:
//      Offset
//      Count
//      Data
- (BOOL) readEEPROMatOffset: (uint8) offset
                   andCount: (uint8) numBytes
                   withData: (nonnull uint8*) data
                   andError: (NSError *_Nullable*_Nullable) aError;
//--------------------------------------------------------------
//--------------------------------------------------------------
//  Configure I2C
//--------------------------------------------------------------
//--------------------------------------------------------------
//args:
//  mode:
//      CarbonI2C_Mode_I2C          = 0,
//      CarbonI2C_Mode_SMBusDevice,
//      CarbonI2C_Mode_SMBusHost,
// i2cAddress:
//      own address
// clockSpeed:
//      Max 400kHz or 400,000Hz
//  enableAck:
//      Enable ACK or not.
//  ackAddressMode:
//      CarbonI2C_AckAddress_7bit or CarbonI2C_AckAddress_10bit
//--------------------------------------------------------------
//--------------------------------------------------------------
-(BOOL) configureI2CWithMode: (ATCarbonI2CMode) mode
          andI2cAddr: (uint16_t) i2cAddress
       andClockSpeed: (uint32_t) clockSpeed
        andEnableAck: (BOOL) enableAck
       andAckAddress: (ATCarbonI2CAckAddressMode)ackAddressMode
            andError: (NSError *_Nullable*_Nullable) aError;
//--------------------------------------------------------------
//--------------------------------------------------------------
//  I2C Transfer
//--------------------------------------------------------------
//--------------------------------------------------------------
// parameters
//
//      aAdress:  7 bit i2c address. Some vendors incorrectly provide two 8-bit slave addresses for their device,
//                one to write to the device and one to read from the device.
//                  This 8-bit number actually encodes the 7-bit slave address and the read/write bit.
//                  it is important to only use the top 7 bits of the address as the slave address.
//                  That is why you need shift the address 1 bit to get rid of the  read/write bit.
//                  e.g. 24LC02 EEPROM i2c address is 0xA0 = Write address and 0xA1 is the read address. The actual Address is (0xA0 >> 1).
//
//      writeLen: write dnumber of data in byte.
//      readLen: Read number of data in byte
//      data:  Write and Read both share this array. Size of this array must be bigger than writeLen and readLen. Max size is 255.
// return value
//
- (BOOL) i2cTransferWithAddress: (uint8_t) aAdress
                    andWriteLen: (uint8_t) writeLen
                     andReadLen: (uint8_t) readLen
                        andData: (nonnull uint8_t*) data
                       andError: (NSError *_Nullable*_Nullable) aError;


//--------------------------------------------------------------
//--------------------------------------------------------------
// Configure the SPI
//--------------------------------------------------------------
//--------------------------------------------------------------
//args:
//  mode:
//    CarbonSPI_Mode_Slave
//    CarbonSPI_Mode_Master
//  direction:   SPI unidirectional or bidirectional data mode.
//    CarbonSPI_Direction_2Lines_FullDuplex,
//    CarbonSPI_Direction_2Lines_RxOnly,
//    CarbonSPI_Direction_1Line_Rx,
//    CarbonSPI_Direction_1Line_Tx,
//  dataSize:
//    CarbonSPI_DataSize_8b
//    CarbonSPI_DataSize_10b
//  cpol:   Specifies the serial clock steady state.
//    CarbonSPI_CPOL_Low  // Clock Idle is Low
//    CarbonSPI_CPOL_High  // Clock Idle is High
//  cpha: Specifies the clock active edge for the bit capture
//    CarbonSPI_CPHA_1Edge    //Leading Edge Falling edge
//    CarbonSPI_CPHA_2Edge    //Trailing Edge  Rising Edge
//  removed ss:
//  baudRate:
//      CarbonSPI_BaudRatePrescaler_21MHz
//      CarbonSPI_BaudRatePrescaler_10_5MHz,
//      CarbonSPI_BaudRatePrescaler_5_25MHz,
//      CarbonSPI_BaudRatePrescaler_2_63MHz,
//      CarbonSPI_BaudRatePrescaler_1_31MHz,
//      CarbonSPI_BaudRatePrescaler_656kHz,
//      CarbonSPI_BaudRatePrescaler_328kHz,
//      CarbonSPI_BaudRatePrescaler_164kHz,
//  firstBit:  data transfers start from MSB or LSB bit.
//    CarbonSPI_FirstBit_MSB
//    CarbonSPI_FirstBit_LSB
//  crcPolynomial: Specifies the polynomial used for the CRC calculation
//          e.g. 7

-(BOOL) configureSPIwithMode:(ATCarbonSpiMode) mode
        andDirection: (ATCarbonSpiDirection) direction
         andDataSize: (ATCarbonSpiDataSize)dataSize
             andCPOL: (ATCarbonSpiCPOL) cpol
             andCPHA: (ATCarbonSpiCPHA) cpha
         andBaudRate: (ATCarbonSpiBaudRate) baudRate
         andFirstBit: (ATCarbonSpiFirstBit) firstBit
    andCRCPolynomial: (int) crcPolynomial
            andError: (NSError *_Nullable*_Nullable) aError;


// Carbon SPI transfer. it uses European connector to address the pin instead of STM32's Port and pin
// parameters

//      isWriteAndReadMode: YES = Write and Read Mode or NO = Write then Read mode
//      writeLen: write dnumber of data in byte
//      readLen: Read number of data in byte
//      data:  Write and Read both share this array. Size of this array must be bigger than writeLen and readLen. Max size is 255.
// return value
- (BOOL) spiTransferWithWriteAndRead: (BOOL) isWriteAndReadMode // isWriteAndReadMode = Write One byte and then Read one byte
                         andWriteLen: (uint8_t) writeLen
                          andReadLen: (uint8_t) readLen
                             andData: (nonnull uint8_t*) data
                            andError: (NSError *_Nullable*_Nullable) aError;


- (BOOL) configureCANBus    : (BOOL) captureTimestamps
       andAutoRecoverFromOff: (BOOL) autoRecoverFromBusOff
               andAutoWakeUp: (BOOL) autoWakeUp
        andKeepTryTilSuccess: (BOOL) keepTryTilSuccess
   andDiscardMessageWhenFull: (BOOL) discardMessageWhenFull
 andTxMessageInPriorityOrder: (BOOL) txMessageInPriorityOrder
                  andCanMode: (ATDeviceCanBusMode) canBusMode
        andMaxNumberOfQuanta: (uint8_t) maxNumberOfQuanta
    andNumberOfQuantaBitSeq1: (uint8_t) numberOfQuantaBitSeq1
    andNumberOfQuantaBitSeq2: (uint8_t) numberOfQuantaBitSeq2
                andPrescaler: (uint16_t) prescaler
                    andError: (NSError *_Nullable*_Nullable) aError;

- (BOOL) sendCANMessageToCANBus: (uint32_t) messageId
                 andMessageType: (ATDeviceCanBusMessageType) messageType
                 andWriteLength: (uint8_t) writeLength
                        andData: (uint8_t *_Nullable) data
                       andError: (NSError *_Nullable*_Nullable) aError;

- (BOOL) receiveCANMessageWithMessageId: (uint32_t *_Nullable) messageId
                   andMessageLeftInFifo: (uint16_t *_Nullable) messageLeftInFifo
                   andIsRemoteTxRequest: (BOOL *_Nullable) isRTR
                        andIsExtendedId: (BOOL *_Nullable) isExtendedId
                    andActualDataLength: (uint8_t *_Nullable) actualDataLength
                                andData: (uint8_t *_Nullable) data
                               andError: (NSError *_Nullable*_Nullable) aError;

- (uint16_t) pendingCANMessage: (NSError *_Nullable*_Nullable) aError;

//--------------------------------------------------------------
//--------------------------------------------------------------
//  Configure UART
//--------------------------------------------------------------
//--------------------------------------------------------------
// Oxygen use UART ID 6
// wordLen:
//      CarbonUartWordLength_8B
//      CarbonUartWordLength_9B,
// stopBits:
//      CarbonUART_StopBits_1,
//      CarbonUART_StopBits_0_5,
//      CarbonUART_StopBits_2,
//      CarbonUART_StopBits_1_5,
//  parity:
//      CarbonUART_Parity_None,
//      CarbonUART_Parity_Even,
//      CarbonUART_Parity_Odd,
//  flowControl:
//      CarbonUART_HW_FlowControl_None,
//      CarbonUART_HW_FlowControl_RTS,
//      CarbonUART_HW_FlowControl_CTS,
//      CarbonUART_HW_FlowControl_RTS_CTS,
//  baudRate:
//      e.g. 12500000
-(BOOL) configureUartWithWordLength: (ATCarbonUARTwordLength) wordLen
                        andStopBits: (ATCarbonUARTStopBitType) stopBits
                          andParity: (ATCarbonUARTParityType) parity
                   andHWFlowControl: (ATCarbonUARTFlowControl) flowControl
                        andBaudRate: (uint32_t) baudRate
                           andError: (NSError *_Nullable*_Nullable) aError;


// UART transfer
// Oxygen use UART ID 6
// parameters
//      writeLen: write dnumber of data in byte
//      readLen: Read number of data in byte
//      data:  Write and Read both share this array. Size of this array must be bigger than writeLen and readLen. Max size is 255.
//      uartReadTimeOutInMiliSeconds:  timeout in Miliseconds when read the UART bus . Only vaild if readLen is non zero.
- (BOOL) uartTransferWithWriteLen: (uint8_t) writeLen
                       andReadLen: (uint8_t) readLen
                          andData: (uint8_t *_Nullable) data
               andUartReadTimeOut: (uint16_t) uartReadTimeOutInMiliSeconds
                         andError: (NSError *_Nullable*_Nullable) aError;


//--------------------------------------------------------------
//--------------------------------------------------------------
//  setup UART to stream data to TCP/IP port 4500 (FIFO-0)
//--------------------------------------------------------------
//--------------------------------------------------------------
// Oxygen use UART ID 6
// wordLen:
//      CarbonUartWordLength_8B
//      CarbonUartWordLength_9B,
// stopBits:
//      CarbonUART_StopBits_1,
//      CarbonUART_StopBits_0_5,
//      CarbonUART_StopBits_2,
//      CarbonUART_StopBits_1_5,
//  parity:
//      CarbonUART_Parity_None,
//      CarbonUART_Parity_Even,
//      CarbonUART_Parity_Odd,
//  flowControl:
//      CarbonUART_HW_FlowControl_None,
//      CarbonUART_HW_FlowControl_RTS,
//      CarbonUART_HW_FlowControl_CTS,
//      CarbonUART_HW_FlowControl_RTS_CTS,
//  baudRate:
//      e.g. 12500000
//
//      FIFO0 will be streaming to TCP port 4500.
//

-(BOOL) uartStartStreamingWithWordLength: (ATCarbonUARTwordLength) wordLen
                             andStopBits: (ATCarbonUARTStopBitType) stopBits
                               andParity: (ATCarbonUARTParityType) parity
                        andHWFlowControl: (ATCarbonUARTFlowControl) flowControl
                             andBaudRate: (uint32_t) baudRate
                                andError: (NSError *_Nullable*_Nullable) aError;

//--------------------------------------------------------------
//--------------------------------------------------------------
//  Stop UART to stream data to TCP/IP port 4500
//--------------------------------------------------------------
//--------------------------------------------------------------
// Oxygen use UART ID 6

-(BOOL) uartStopStreaming: (NSError *_Nullable*_Nullable) aError;

@end
