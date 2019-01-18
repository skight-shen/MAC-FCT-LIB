//
//  ATDeviceUSBC.h
//  ATDeviceElements
//
//  Created by Sai  on 3/23/17.
//  Copyright © 2017 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <ATDeviceElements/ATDeviceElement.h>

typedef NS_ENUM(uint8_t, ATDeviceGPIOPortName) {
    ATD_GPIO_A = 0,
    ATD_GPIO_B,
    ATD_GPIO_C,
    ATD_GPIO_D,
    ATD_GPIO_E,
    ATD_GPIO_F,
    ATD_GPIO_G,
    ATD_GPIO_H,
    ATD_GPIO_I,
};

typedef NS_ENUM(uint8_t, ATDeviceOrientation) {
    ATDOrientationCC1 = 0,
    ATDOrientationCC2,
    ATDOrientationNeither,
    ATDOrientationBoth,
};

typedef NS_ENUM(uint8_t, ATDeviceCCConfigType) {
    ATD_CCType_NoAction = 0,
    ATD_CCType_NoConnection,
    ATD_CCType_MakeConnection,
    ATD_CCType_Reserved,
};



@interface ATDeviceGPIOPort: NSObject

//values
//Example: 0x2544 = 0b0010010101000100
//Pins 3,6,8,10,and 13 are at a logic level High
//The rest of the pins are at a logic level LOW
@property (nonatomic) uint16_t values;
//directions
//Example: 0x4083 = 0b0100000010000011
//Pins 0,1,7, and 14 are outputs.
//• The rest of the pins are inputs.
@property (nonatomic) uint16_t directions;

@end



@interface ATDeviceUSBC : ATDeviceElement

//
// measureVConnPowerOnPort
// param
//      portIndex   port index to measure. 1 base.
//      miliVolt    measurement  voltage result  in mili voltage.
//      miliAmp     measurement  Amp result  in mili amp.
//      isSource    TRUE means port is sourcing current. NO means port is sinking current
//      aError      when there is an error, this will be set
// return value
//      BOOL:	YES = successed with no Error.
//              NO  = Error occured;

-(BOOL) measureVConnPowerOnPort: (NSUInteger)     portIndex
              andMiliVoltResult: (uint32_t*)      miliVolt
               andMiliAmpResult: (uint32_t*)      miliAmp
                    andIsSource: (BOOL*)          isSource
                       andError: (NSError **)     aError;

//
// measureVBusPowerOnPort
// param
//      portIndex   port index to measure. 1 base.
//      miliVolt    measurement  voltage result  in mili voltage.
//      miliAmp     measurement  Amp result  in mili amp.
//      isSource    TRUE means port is sourcing current. NO means port is sinking current
//      aError      when there is an error, this will be set
// return value
//      BOOL:	YES = successed with no Error.
//              NO  = Error occured;

-(BOOL) measureVBusPowerOnPort: (NSUInteger)    portIndex
             andMiliVoltResult: (uint32_t*)     miliVolt
              andMiliAmpResult: (uint32_t*)     miliAmp
                   andIsSource: (BOOL*)         isSource
                      andError: (NSError **)    aError;

// gpioStatus
// get all the GPIO Pin values
// NSArray[0] or NSArray[ATD_GPIO_A]= PORTA
// NSArray[1] or NSArray[ATD_GPIO_B]= PORTB
// NSArray[2] or NSArray[ATD_GPIO_C]= PORTC
// NSArray[3] or NSArray[ATD_GPIO_D]= PORTD
- (NSArray < ATDeviceGPIOPort*>*) gpioStatus: (NSError **) aError;





// configureDeviceAsVBusSinkOnPort
// This function will make sure device has a Galluim connected and configure it to sink current at requested voltage and currrent.
// param
//      portIndex    Port ID to apply the change, Xenon 2 ports: 1 or 2. Palladium 4 ports: 1,2,3,and 4.
//      milliVolt    Target Milli Voltage
//      milliAmp     Target Milli Current
//      aError      when there is an error, this will be set
// return value
//      BOOL:	YES = successed with no Error.
//              NO  = Error occured;
-(BOOL) configureDeviceAsVBusSinkOnPort: (NSUInteger) portIndex
                           andMilliVolt: (NSUInteger) milliVolt
                            andMilliAmp: (NSUInteger) milliAmp
                               andError: (NSError **) aError;
// clearVBusSinkOnPort
// this fucntion will turn off the VBus Sink (Load)
// param
//      portIndex    Port ID to apply the change,Xenon 2 ports: 1 or 2. Palladium 4 ports: 1,2,3,and 4.
//      aError      when there is an error, this will be set
// return value
//      BOOL:	YES = successed with no Error.
//              NO  = Error occured;
-(BOOL) clearVBusSinkOnPort: (NSUInteger) portIndex
                     andError: (NSError **) aError;


// configureDeviceAsVBusSourceOnPort
// This function will make sure device has a Galluim connected and configure it to source current at requested voltage and currrent.
// param
//      portIndex    Port ID to apply the change, Xenon 2 ports: 1 or 2. Palladium 4 ports: 1,2,3,and 4.
//      milliVolt    Target Milli Voltage
//      milliAmp     Target Milli Current
//      aError      when there is an error, this will be set
// return value
//      BOOL:	YES = successed with no Error.
//              NO  = Error occured;
-(BOOL) configureDeviceAsVBusSourceOnPort: (NSUInteger) portIndex
                             andMilliVolt: (NSUInteger) milliVolt
                              andMilliAmp: (NSUInteger) milliAmp
                                 andError: (NSError **) aError;


// configureDeviceAsVConnSinkOnPort
// This function will make sure device has a Galluim connected and configure it to sink current at requested currrent.
// param
//      portIndex    Port ID to apply the change, Xenon 2 ports: 1 or 2. Palladium 4 ports: 1,2,3,and 4.
//      milliAmp     Target Milli Current
//      aError      when there is an error, this will be set
// return value
//      BOOL:	YES = successed with no Error.
//              NO  = Error occured;
-(BOOL) configureDeviceAsVConnSinkOnPort: (NSUInteger) portIndex
                             andMilliAmp: (NSUInteger) milliAmp
                                andError: (NSError **) aError;


// clearVConnSinkOnPort
// this fucntion will turn off the VConn Sink (Load)
// param
//      portIndex    Port ID to apply the change,Xenon 2 ports: 1 or 2. Palladium 4 ports: 1,2,3,and 4.
//      aError      when there is an error, this will be set
// return value
//      BOOL:	YES = successed with no Error.
//              NO  = Error occured;
-(BOOL) clearVConnSinkOnPort: (NSUInteger) portIndex
                      andError: (NSError **) aError;


// isGalliumConnected
// this fucntion will check if Gallium is connected or not.
// param
//      aError      when there is an error, this will be set
// return value
//      BOOL:	YES = connected.
//              NO  = not connnected or Error occured
-(BOOL) isGalliumConnected: (NSError **) aError;

//  portStatusOnPort
//  param
//       portIndex    Port ID to apply the change, Xenon 2 ports: 1 or 2. Palladium 4 ports: 1,2,3,and 4.
//       ccConnected            CC Connection State 0 - Disconnected, 1 - Connected
//       andIsSource            0 - Sink. Port is presenting Rd, 1 - Source. Port is presenting Rp
//       andIsDownFacingPort    Port Data Role.  Only valid if Bit 0 is 1.   0 - UFP 1 - DFP
//       andIsCC2Up             Orientation.  Only valid if Bit 0 is 1.  0 - CC1 (top-up),  1 - CC2 (bottom-up)
//       numOfPorts             Number of Ports of the device
//       dataProtocolUsed        Current data protocol.
//                              0 - USB
//                              1 - DisplayPort
//                              2 - Thunderbolt
//                              3 - Reserved
-(BOOL)     portStatusOnPort: (NSUInteger) portIndex
              andCCConnected: (BOOL*) ccConnected
                 andIsSource: (BOOL*) isSource
         andIsDownFacingPort: (BOOL*) isDownFacingPort
                  andIsCC2Up: (BOOL*) isCC2Up
         andDataProtocolUsed: (uint8_t*) dataProtocolUsed
               andNumOfPorts: (NSUInteger*) numOfPorts
                    andError: (NSError **) aError;
//  swapPowerRoleToSourceOnPort
//  param
//      portIndex    Port ID to apply the change, Xenon 2 ports: 1 or 2. Palladium 4 ports: 1,2,3,and 4.
- (BOOL) swapPowerRoleToSourceOnPort: (NSUInteger) portIndex
                            andError: (NSError **) aError;
//  swapPowerRoleToSinkOnPort
//  param
//      portIndex    Port ID to apply the change, Xenon 2 ports: 1 or 2. Palladium 4 ports: 1,2,3,and 4.
- (BOOL) swapPowerRoleToSinkOnPort: (NSUInteger) portIndex
                          andError: (NSError **) aError;

// updateSinkCapabilitiesOnPort
// param
//      portIndex    Port ID to apply the change, Xenon 2 ports: 1 or 2. Palladium 4 ports: 1,2,3,and 4.
//      milliVolt    Target Milli Voltage
//      milliAmp     Target Milli Current
//      aError      when there is an error, this will be set
// return value
//      BOOL:	YES = successed with no Error.
//              NO  = Error occured;
-(BOOL) updateSinkCapabilitiesOnPort: (NSUInteger) portIndex
                        andMilliVolt: (NSUInteger) milliVolt
                         andMilliAmp: (NSUInteger) milliAmp
                            andError: (NSError **) aError;

// updateSourceCapabilitiesOnPort
// param
//      portIndex    Port ID to apply the change, Xenon 2 ports: 1 or 2. Palladium 4 ports: 1,2,3,and 4.
//      milliVolt    Target Milli Voltage
//      milliAmp     Target Milli Current
//      aError      when there is an error, this will be set
// return value
//      BOOL:	YES = successed with no Error.
//              NO  = Error occured;
-(BOOL) updateSourceCapabilitiesOnPort: (NSUInteger) portIndex
                          andMilliVolt: (NSUInteger) milliVolt
                           andMilliAmp: (NSUInteger) milliAmp
                              andError: (NSError **) aError;
// negotiatePowerContractOnPort
// param
//      portIndex    Port ID to apply the change, Xenon 2 ports: 1 or 2. Palladium 4 ports: 1,2,3,and 4.
//      milliVolt    Target Milli Voltage
//      milliAmp     Target Milli Current
//      aError      when there is an error, this will be set
// return value
//      BOOL:	YES = successed with no Error.
//              NO  = Error occured;
- (BOOL) negotiatePowerContractOnPort: (NSUInteger) portIndex
                         andMilliVolt: (NSUInteger) milliVolt
                          andMilliAmp: (NSUInteger) milliAmp
                            andAsSink: (BOOL)       asSink
                             andError: (NSError **) aError;

// negotiatedContractOnPort
// get the current negotiated power contract on port
//      portIndex    Port ID to apply the change, Xenon 2 ports: 1 or 2. Palladium 4 ports: 1,2,3,and 4.
//      milliVolt    negotiated Milli Voltage
//      milliAmp     negotiated Milli Current
//      aError      when there is an error, this will be set
// return value
//      BOOL:	YES = successed with no Error.
//              NO  = Error occured;
- (BOOL)    negotiatedContractOnPort: (NSUInteger) portIndex
              andNegotiatedMilliVolt: (NSUInteger*) milliVolt
               andNegotiatedMilliAmp: (NSUInteger*) milliAmp
                            andError: (NSError **) aError;

// setCCOrientationOnPort
// param
//      portIndex       port index to change orientation. Xenon 2 ports: 1 or 2. Palladium 4 ports: 1,2,3,and 4.
//      orientation     The Orientation to:
//                      ATDOrientationCC1
//                      ATDOrientationCC2,
//                      ATDOrientationNeither, Both disconnected
//                      ATDOrientationBoth,    Both connected
//      presentRa       When it's not connected, connect the pin to Ra Pull Down resistor?
//      aError      when there is an error, this will be set
// return value
//      BOOL:	YES = successed with no Error.
//              NO  = Error occured;

-(BOOL) setCCOrientationOnPort: (NSUInteger) portIndex
                andOrientation: (ATDeviceOrientation) orientation
                  andPresentRa: (BOOL) presentRa
                      andError: (NSError **)  aError;
// flipOrientationOnPort
//   Flip the current Orientation to another. If CC1 is active, CC2 will be active and CC1 will be off
//   If both CC1 and CC2 are active, error will return.
//   If neither CC1 and CC2 are active, error will return.
//    Ra will be preserved during fliping.
// param
//      portIndex       port index to change orientation. Xenon 2 ports: 1 or 2. Palladium 4 ports: 1,2,3,and 4.
//      aError      when there is an error, this will be set
// return value
//      BOOL:	YES = successed with no Error.
//              NO  = Error occured;

-(BOOL) flipOrientationOnPort: (NSUInteger) portIndex
                      andError: (NSError **)  aError;

//ccConfigOnPort
// Read the CDTI register CCConfiguratino at 0x48
//param
//      portIndex       port index to change orientation. Xenon 2 ports: 1 or 2. Palladium 4 ports: 1,2,3,and 4.
//      aError      when there is an error, this will be set
// return value
//      uint8_t:	the value of the register

-(uint8_t) ccConfigOnPort: (NSUInteger) portIndex
                          andError: (NSError **)  aError;



@property (nonatomic) NSUInteger numberOfPorts;

@end
