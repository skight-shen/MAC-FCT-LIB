//
//  ATDeviceCarbon.h
//  ATDeviceElements
//
//  Created by Sai  on 9/19/16.
//  Copyright © 2016 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <ATDeviceElements/ATDeviceElement.h>
#import <ATDeviceElements/ATDeviceParameters.h>
#import <ATDeviceElements/ATDeviceCarbonConnectorChecker.h>
#import <ATDeviceElements/ATDeviceMCUCommon.h>

#define kCarbonUSBProductType @"Carbon"

//---------------------------------
//---------------------------------
// Carbon Error code is defined in ATDeviceCarbonErrors.h
//---------------------------------
//---------------------------------

#define kUART_STREAMING_TCP 4500




typedef NS_ENUM(uint8_t, ATCarbonDacTriangleAmplitude) {
    
    CarbonDAC_TriangleAmplitude_3v3 = 0,
    CarbonDAC_TriangleAmplitude_1v65,
    NumOfCarbonDAC_TriangleAmplitude,
    
};

@interface ATDeviceCarbon : ATDeviceElement
//--------------------------------------------------------------
//4cc command: "GIOs"   GPIO single write
//args
//      type write 1, Write 0 or toggle
//      andConnectorRow can be A,B,or C.
//      pin from 1 to 32;
//
- (BOOL)  writeGPIO:(ATCarbonWriteGPIOType) type
                andConnectorRow: (ATCarbonEuropeanConnectorRow) row
                andPin:(uint8_t) pin
                andError: (NSError**) aError;
//--------------------------------------------------------------
//4cc command: "GIOs"   GPIO single read
//args
//      value: GPIO readback = 0 or 1.  0 = Low and 1 = High. *Not the same as ATCarbonWriteGPIOType
//      andConnectorRow can be A,B,or C.
//      pin from 1 to 32;
//
- (BOOL)  readGPIO: (uint8_t*) value
                andConnectorRow: (ATCarbonEuropeanConnectorRow) row
                andPin:(uint8_t) pin
                andError: (NSError**) aError;
//--------------------------------------------------------------
// 4cc command: "ADCr"   ADC read
//args
//      ADCId can be 1, 2, or 3
//      channel ranges from 0 to 15
//      samples 1 to max of uint16_t;
//      reading_inV: between 0 to 3.3V.
//      rawReading:  0 to 4096 if for resolution_12b.
//      timeoutMilliseconds  1000 = 1 second.
- (BOOL) readADC: (uint8_t) ADCId
      andChannel: (uint8_t) whichChannel
   andResolution: (ATCarbonADCResolutions) resolution
       andSample: (uint16_t) numOfSample
      andReading_inV: (double*) reading_inV
   andRawReading: (uint32_t*) rawReading
 timeoutMilliseconds:(NSUInteger)timeoutMilliseconds
        andError: (NSError**) aError;

//--------------------------------------------------------------
// 4cc command: "ADCc"   ADC configure
//args
//      ADCId can be 1, 2, or 3
//      resolution from 0 to 3 definded in ATCarbonADCResolutions
//      CarbonADC_Resolution_12b
//      CarbonADC_Resolution_10b,
//      CarbonADC_Resolution_8b,
//      CarbonADC_Resolution_6b,
- (BOOL) configureADC: (uint8_t) ADCId
        andResolution: (ATCarbonADCResolutions) resolution
             andError: (NSError**) aError;

//--------------------------------------------------------------
//--------------------------------------------------------------
// Configure all the Ports. GPIO, UART, SPI, I2C, CAN
//--------------------------------------------------------------
//--------------------------------------------------------------
// 4cc command: "PTSc"   Configure all the ports
// Code for using ATDCarbonEuropeanConnector class
// NSError * error = nil;
// ATDCarbonEuropeanConnector * connector = [ [ATDCarbonEuropeanConnector alloc] init];
// BOOL success = [connector addPinWithRow:'A' andPin:10 andType:GPIO_Mode_IN_25MHz_PP_PullDown_Init0 andError:&error]:
//      success = [connector addPinWithRow:'B' andPin:11 andType:GPIO_Mode_IN_25MHz_PP_PullDown_Init0 andError:&error]:
//      success = [connector addPinWithRow:'C' andPin:11 andType:GPIO_Mode_AF_PP_NoPull_GPIO_AF_SPI2 andError:&error]:
// Now you can pass it to this function
- (BOOL) configureEuropeanConnector: (ATDCarbonEuropeanConnector*) connector andError: (NSError**) aError;
//--------------------------------------------------------------
//--------------------------------------------------------------
// Same as configureEuropeanConnector and also save the configuration to the EEPROM
// Next reboot the configuration will be loaded automatically
//--------------------------------------------------------------
//--------------------------------------------------------------
- (BOOL) configureEuropeanConnectorAndSaveToEEPROM: (ATDCarbonEuropeanConnector*) connector andError: (NSError**) aError;

//--------------------------------------------------------------
//--------------------------------------------------------------
//  Return the configureEuropeanConnector setting from EEPROM which previous set using configureEuropeanConnectorAndSaveToEEPROM
//--------------------------------------------------------------
//--------------------------------------------------------------
- (ATDCarbonEuropeanConnector *) europeanConnectorSettingfromEEPROMwithError: (NSError**) aError;

//--------------------------------------------------------------
//--------------------------------------------------------------
//  Configure I2C
//--------------------------------------------------------------
//--------------------------------------------------------------
// 4cc command: "I2Cc"
//args:
// i2cId:
//      i2c 1 or 2.
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

-(BOOL) configureI2C: (int) i2cId
             andMode: (ATCarbonI2CMode) mode
          andI2cAddr: (uint16_t) i2cAddress
       andClockSpeed: (uint32_t) clockSpeed
        andEnableAck: (BOOL) enableAck
       andAckAddress: (ATCarbonI2CAckAddressMode)ackAddressMode
            andError: (NSError**) aError;


//--------------------------------------------------------------
//--------------------------------------------------------------
//  Configure UART
//--------------------------------------------------------------
//--------------------------------------------------------------
// 4cc command: "URTc"
//args:
//  uartId:
//  1 (USART1),2 (USART2), 3 (USART3), 4 (UART4), 5 (UART5), 6 (USART6).
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
-(BOOL) configureUart: (int) uartId
        andWordLength: (ATCarbonUARTwordLength) wordLen
          andStopBits: (ATCarbonUARTStopBitType) stopBits
            andParity: (ATCarbonUARTParityType) parity
     andHWFlowControl: (ATCarbonUARTFlowControl) flowControl
          andBaudRate: (uint32_t) baudRate
             andError: (NSError**) aError;

//--------------------------------------------------------------
//--------------------------------------------------------------
// Configure the SPI
//--------------------------------------------------------------
//--------------------------------------------------------------
// 4cc command: "SPIc"
//args:
//  spiId:
//  SPI2 or SPI3. SPI1 is reserved.
//  direction:   SPI unidirectional or bidirectional data mode.
//    CarbonSPI_Direction_2Lines_FullDuplex,
//    CarbonSPI_Direction_2Lines_RxOnly,
//    CarbonSPI_Direction_1Line_Rx,
//    CarbonSPI_Direction_1Line_Tx,
//  mode:
//    CarbonSPI_Mode_Slave
//    CarbonSPI_Mode_Master
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

-(BOOL) configureSPI: (int) spiId
        andDirection: (ATCarbonSpiDirection) direction
          andSPiMode: (ATCarbonSpiMode) mode
         andDataSize: (ATCarbonSpiDataSize)dataSize
             andCPOL: (ATCarbonSpiCPOL) cpol
             andCPHA: (ATCarbonSpiCPHA) cpha
         andBaudRate: (ATCarbonSpiBaudRate) baudRate
         andFirstBit: (ATCarbonSpiFirstBit) firstBit
    andCRCPolynomial: (int) crcPolynomial
            andError: (NSError**) aError;

#pragma mark ADC
//--------------------------------------------------------------
//--------------------------------------------------------------
// Configure the ADC trigger.
// ADC FIFO's 1024 and each sample is 2 Byte.
//--------------------------------------------------------------
//--------------------------------------------------------------
// 4cc command: "ADCt"   ADC trigger
//args
//   ADCId:
//      can be 1, 2, or 3
//   whichChannel:
//      ranges from 0 to 15
//  sampleRateInKHz:
//      e.g. 100 = 100Khz
//  resolution:
//      CarbonADC_Resolution_12b
//      CarbonADC_Resolution_10b,
//      CarbonADC_Resolution_8b,
//      CarbonADC_Resolution_6b,
//  triggerVolt:
//       0.0 to 3.3V  .  Reference Voltage is 3.3V
//  triggerifOverTriggerVolt:
//      YES:  will trigger if the sample is higher than the triggerVolt
//      NO:   will trigger if the sample is lower than the triggerVolt
//   postTriggerNumberOfCapture:
//      The FIFO is 1024 circuler FIFO. User select number of sample after it's triggered.
//      e.g. 100, capture 100 samples after triggered.

- (BOOL) adcSetupTrigger: (uint8_t) ADCId
              andChannel: (uint8_t) whichChannel
      andSampleRateInKHz: (uint16_t) sampleRateInKHz
           andResolution: (ATCarbonADCResolutions) resolution
             andTrigVolt: (double) triggerVolt
andTrigifOverTriggerVolt: (BOOL) triggerifOverTriggerVolt
             andPostTrig: (uint16_t)postTriggerNumberOfCapture
        andError: (NSError**) aError;

//--------------------------------------------------------------
//--------------------------------------------------------------
// force ADC to trigger and read back status
//  Use with setupTriggerADC.
//--------------------------------------------------------------
//--------------------------------------------------------------
// 4cc command: "ADCf"
//args
//   ADCId:
//      can be 1, 2, or 3
//  forceTrig:
//     YES: Force Trigger, so users can read back the FIFO data
//  adcStopped:
//      Status of the ADC.  Stopped or not? Stopped means triggered and post trigger capture all done
//  adcTriggered:
//      Status of the ADC. Triggered or not?
//  numOfCaptureInFifo:
//      Numbe of Capture in the FIFO.

- (BOOL) adcForceTrigger: (uint8_t) ADCId
          andADCiStopped: (BOOL*) adcStopped
         andADCTriggered: (BOOL*) adcTriggered
   andNumOfCaptureinFifo: (uint16_t*)numOfCaptureInFifo
                andError: (NSError**) aError;
//--------------------------------------------------------------
//--------------------------------------------------------------
// read back ADC trigger status
//  Use with setupTriggerADC.
//--------------------------------------------------------------
//--------------------------------------------------------------
// 4cc command: "ADCf"
//args
//   ADCId:
//      can be 1, 2, or 3
//  forceTrig:
//     NO: status only
//  adcStopped:
//      Status of the ADC.  Stopped or not? Stopped means triggered and post trigger capture all done.
//  adcTriggered:
//      Status of the ADC. Triggered or not?
//  numOfCaptureInFifo:
//      Numbe of Capture in the FIFO.

- (BOOL) adcTriggerStatus: (uint8_t) ADCId
           andADCiStopped: (BOOL*) adcStopped
          andADCTriggered: (BOOL*) adcTriggered
    andNumOfCaptureinFifo: (uint16_t*)numOfCaptureInFifo
                 andError: (NSError**) aError;

//--------------------------------------------------------------
//--------------------------------------------------------------
//  Read the ADC FIFO
//  Use with setupTriggerADC.
//--------------------------------------------------------------
//--------------------------------------------------------------
// 4cc command used: "ADCd"
// args:
//   ADCId:
//      can be 1, 2, or 3
// return:
//  An NSArray of NSNumber of rawReading which contains the FIFO captures.
//      Resolution_12b adc_range = 4096;
//      Resolution_10b adc_range = 1024;
//      Resolution_8b adc_range = 256;
//      Resolution_6b adc_range = 64;
//    To get the final reading in Voltage;
//    The formula result in Voltage = (3.3/adc_range) * rawReading;
- (NSArray*) adcFifoRawRead: (uint8_t) ADCId
                andError: (NSError**) aError;

// Same as adcFifoRawRead but convert the raw data to double
- (NSArray*) adcFifoRead: (uint8_t) ADCId
                andError: (NSError**) aError;

#pragma mark UART STREAMING
//--------------------------------------------------------------
//--------------------------------------------------------------
//  setup UART to stream data to TCP/IP port 4500 (FIFO-0) or 4501 (FIFO-1)
//  Streaming only support up to 2 UART.
//--------------------------------------------------------------
//--------------------------------------------------------------
// 4cc command: "URTs"
//  1 (USART1),2 (USART2), 3 (USART3), 4 (UART4), 5 (UART5), 6 (USART6).
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
// andStreamFIFOIndex:
//      Select the Streaming FIFO 0 or 1.
//      FIFO0 will be streaming to TCP port 4500.
//      FIFO1 will be streaming to TCP port 4501.
//      If not set FIFO index, FIFO-0 will be used.

-(BOOL) uartStartStreaming: (int) uartId
        andWordLength: (ATCarbonUARTwordLength) wordLen
          andStopBits: (ATCarbonUARTStopBitType) stopBits
            andParity: (ATCarbonUARTParityType) parity
     andHWFlowControl: (ATCarbonUARTFlowControl) flowControl
          andBaudRate: (uint32_t) baudRate
             andError: (NSError**) aError;

-(BOOL) uartStartStreaming: (int) uartId
             andWordLength: (ATCarbonUARTwordLength) wordLen
               andStopBits: (ATCarbonUARTStopBitType) stopBits
                 andParity: (ATCarbonUARTParityType) parity
          andHWFlowControl: (ATCarbonUARTFlowControl) flowControl
               andBaudRate: (uint32_t) baudRate
        andStreamFIFOIndex: (uint8_t)  fifoIndex
                  andError: (NSError**) aError;

//--------------------------------------------------------------
//--------------------------------------------------------------
//  Stop UART to stream data to TCP/IP port 4500  or 4501
//--------------------------------------------------------------
//--------------------------------------------------------------
// 4cc command: "URTs"
//  uartId:
//  1 (USART1),2 (USART2), 3 (USART3), 4 (UART4), 5 (UART5), 6 (USART6).

-(BOOL) uartStopStreaming: (int) uartId
                  andError: (NSError**) aError;

#pragma mark SPI

// Command = "SPIt"
// Carbon SPI transfer. it uses European connector to address the pin instead of STM32's Port and pin
// parameters
//      spiID: SPI Bus ID, 2 or 3. 1 is reserved
//      slaveSelectRow:
//          EuropeanPortRowA
//          EuropeanPortRowB
//          EuropeanPortRowC
//      slaveSelectPin:  The pin for European from 1 to 32
//      isWriteAndReadMode: YES = Write and Read Mode or NO = Write then Read mode
//      writeLen: write dnumber of data in byte
//      readLen: Read number of data in byte
//      data:  Write and Read both share this array. Size of this array must be bigger than writeLen and readLen. Max size is 255.
// return value
- (BOOL) spiCarbonTransferWithSPIid: (uint8_t) spiID
           andSlaveSelectEuropeanRow: (ATCarbonEuropeanConnectorRow) slaveSelectRow
            andSlaveSelectPin: (uint8_t) slaveSelectPin
          andWriteAndReadMode: (BOOL) isWriteAndReadMode // isWriteAndReadMode = Write One byte and then Read one byte
                  andWriteLen: (uint8_t) writeLen
                   andReadLen: (uint8_t) readLen
                      andData: (uint8_t*) data
                     andError: (NSError**) aError;

// spiTransferWithSPIid same as spiCarbonTransferWithSPIid.
// Just removed the Name Carbon to make it generic
- (BOOL) spiTransferWithSPIid: (uint8_t) spiID
          andSlaveSelectEuropeanRow: (ATCarbonEuropeanConnectorRow) slaveSelectRow
                  andSlaveSelectPin: (uint8_t) slaveSelectPin
                andWriteAndReadMode: (BOOL) isWriteAndReadMode // isWriteAndReadMode = Write One byte and then Read one byte
                        andWriteLen: (uint8_t) writeLen
                         andReadLen: (uint8_t) readLen
                            andData: (uint8_t*) data
                           andError: (NSError**) aError;
//--------------------------------------------------------------
//--------------------------------------------------------------
//  DAC
//--------------------------------------------------------------
//--------------------------------------------------------------
#pragma mark DAC

// Command = "DACc"
//   Configure the DAC to generate White Noise
// Parameters:
//  enableOutBuffer = Enable the DAC's Output Buffer or not
//  enableCh1 = enable channel 1
//  enableCh2 = enable channel 2
//
-(BOOL) dacGenerateWhiteNoiseWithBufferEnable: (BOOL) enableOutBuffer
                           andEnableChannel_1: (BOOL) enableCh1
                           andEnableChannel_2: (BOOL) enableCh2
                                     andError: (NSError**) aError;

// Command = "DACc"
//   Configure the DAC to generate Triangle Waveform
// Parameters:
//  enableOutBuffer = Enable the DAC's Output Buffer or not
//  enableCh1 = enable channel 1
//  enableCh2 = enable channel 2
//  amplitude = CarbonDAC_TriangleAmplitude_3v3 or CarbonDAC_TriangleAmplitude_1v65
//  frequencyInHz = for CarbonDAC_TriangleAmplitude_3v3 Max = 2500Hz
//                  for CarbonDAC_TriangleAmplitude_1v65 Max = 5000Hz
//
-(BOOL) dacGenerateTriangleWaveFormWithBufferEnable: (BOOL) enableOutBuffer
                                 andEnableChannel_1: (BOOL) enableCh1
                                 andEnableChannel_2: (BOOL) enableCh2
                                        andAmplitude: (ATCarbonDacTriangleAmplitude) amplitude
                                       andFrequencyInHz: (uint16_t) frequencyInHz
                                           andError: (NSError**) aError;
// Command = "DACc"
//   Configure the DAC to generate a fixed voltage
// Parameters:
//  enableOutBuffer = Enable the DAC's Output Buffer or not
//  enableCh1 = enable channel 1
//  ch1Volt = channel voltage 0.0 to 3.3v
//  enableCh2 = enable channel 2
//  ch2Volt = channel voltage 0.0 to 3.3v
-(BOOL) dacGenerateFixedVoltageWithBufferEnable: (BOOL) enableOutBuffer
                             andEnableChannel_1: (BOOL) enableCh1
                               andChannel_1Volt: (double) ch1Volt
                             andEnableChannel_2: (BOOL) enableCh2
                               andChannel_2Volt: (double) ch2Volt
                                       andError: (NSError**) aError;

#pragma mark "CAN Bus"

/** configureCANBus
 * brief Configure the CAN Bus
 *
 * param canBusId:                     CAN ID  1 or 2
 * param captureTimestamps:            Capture Timestamps of CAN packets
 * param autoRecoverFromBusOff:        Automatically recover from Bus-Off state
 * param autoWakeUp:                   Automatically wake up upon receiving a CAN message
 * param keepTryTilSuccess:            Keep trying to transmit until successful
 * param discardMessageWhenFull:       When RX FIFO is full, discard received messages
 * param txMessageInPriorityOrder:     Transmit messages in order of priority, rather than chronologically
 * param canBusMode:                   Defined in ATDeviceCanBusMode
 * param maxNumberOfQuanta:            specifies the maximum number of time quanta the CAN hardware is allowed to lengthen or shorten a bit to perform resynchronization
 *                                      1 = 1 time quantum
 *                                      2 = 2 time quantum
 *                                      3 = 3 time quantum
 *                                      4 = 4 time quantum   // 4 time quantum is max
 * param numberOfQuantaBitSeq1         Specifies the number of time quanta in Bit Segment 1.
 *                                      1 = 1 time quantum
 *                                      2 = 2 time quantum
 *                                      ...
 *                                      16 = 16 time quantum  // 16 time quantum is max
 * param numberOfQuantaBitSeq2         Specifies the number of time quanta in Bit Segment 2.
 *                                      1 = 1 time quantum
 *                                      2 = 2 time quantum
 *                                      ...
 *                                      8 = 8 time quantum  // 8 time quantum is max
 * param[in] prescaler                     It ranges from 1 to 1024
 * param[out] aError: nil = NO error, or error set. Error code is defined in <ATDeviceElements/ATDeviceCarbonErrors.h>
 * retval BOOL: YES = sucess NO = Error;
 *
 *
 */

- (BOOL) configureCANBus    : (uint8_t) canBusId
                andCaptureTS: (BOOL) captureTimestamps
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
                    andError: (NSError**) aError;

/** sendCANMessageToCANBus
 * brief send message the CAN Bus
 *
 * param[in] canBusId:             CAN ID  1 or 2
 * param[in] messageId:            Message/Frame ID
 * param[in] messageType:          Defined in ATDeviceCanBusMessageType. 11Bit Standard or 29bit extended.
 * param[in] writeLength:          Number of Byte to send. Max is 8.
 * param[out] data:                 The Data to send
 * param[out] aError: nil = NO error, or error set. Error code is defined in <ATDeviceElements/ATDeviceCarbonErrors.h>
 * retval BOOL: YES = sucess NO = Error;
 *
 *
 */

- (BOOL) sendCANMessageToCANBus: (uint8_t) canBusId
                   andMessageId: (uint32_t) messageId
                 andMessageType: (ATDeviceCanBusMessageType) messageType
                 andWriteLength: (uint8_t) writeLength
                        andData: (uint8_t*) data
                       andError: (NSError**) aError;
/** receiveCANMessageFromCANBus
 * brief receive Message from the CAN Bus Software FIFO which can contains up to 1260 messages
 *
 * param[out] messageId:            Message/Frame ID
 * param[out] messageLeftInFifo:
 * param[out] isRTR:                Remote transmission request (RTR)
 * param[out] isExtendedId:         dentifier extension bit (IDE)
 * param[out] actualReadLength:     Actual Number of data Bytes read.
 * param[out] data:                 The Data to read. Must be at least 8 bytes.
 * param[out] aError: nil = NO error, or error set. Error code is defined in <ATDeviceElements/ATDeviceCarbonErrors.h>
 * retval BOOL: YES = sucess NO = Error;
 *
 *
 */
- (BOOL) receiveCANMessageWithMessageId: (uint32_t*) messageId
                   andMessageLeftInFifo: (uint16_t*) messageLeftInFifo
                   andIsRemoteTxRequest: (BOOL*) isRTR
                        andIsExtendedId: (BOOL*) isExtendedId
                    andActualDataLength: (uint8_t*) actualDataLength
                                andData: (uint8_t*) data
                               andError: (NSError**) aError;

/** receiveCANMessageFromCANBus
 * brief receive number of pendding Message inside the CAN Bus Software FIFO which can contains up to 1260 messages
 *
 * param[out] aError: nil = NO error, or error set. Error code is defined in <ATDeviceElements/ATDeviceCarbonErrors.h>
 * retval uint16_t:     number of message in FIFO
 *
 *
 */

- (uint16_t) pendingCANMessage: (NSError**) aError;



@end
