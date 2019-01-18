//
//  ATDeviceCaesium.h
//  ATDeviceElements
//
//  Created by Sai  on 12/16/16.
//  Copyright © 2016 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <ATDeviceElements/ATDeviceUSBC.h>
#import <ATDeviceElements/ATDeviceParameters.h>

// Measure VConn or VBus fucntions are declared in the base class ATDeviceUSBC

@interface ATDeviceCaesium : ATDeviceUSBC

// configureCaesiumForConnectionAtSpeed
// Change USB Port Speed (SPDc)
// parameters
//      targetSpeed = ATDeviceCaesiumSpeed
//      disconnectTime =  disconnect time (emulate a USB data disconnect) in MiliSeconds before reconnecting in new speed
//      disconnectCCLInes = if Caesium should emulate a type-C disconnect or just a USB disconnect
//      actualSpeed = the speed after the speed changed.
// return value
//      BOOL:	YES = successed with no Error.
//              NO  = Error occured;
-(BOOL) configureCaesiumForConnectionAtSpeed: (ATDeviceCaesiumSpeed) targetSpeed
                    disconnectTimeInMilliSec: (uint16_t) disconnectTime
                           disconnectCCLines: (BOOL) disconnectCC
                              andActualSpeed: (ATDeviceCaesiumSpeed*)actualSpeed
                                   withError: (NSError**) aError;

//
//  USB Port Error Counts (ERRC)
//  This command checks the FX3 counters for Physical Layer, Link Layer, and Recovery Mode values.  After reading these values, all three counters are reset to 0.
//  Note: These values are only valid when connected at Super Speed.
//
// parameters
//      phyLayerError       = Physical Layer Error Counts
//      linkLayerError      = Link Layer Error Counts
//      numOfRecoverState   = Number of ENtrances To USB 3.0 Recovery State.
// return value
//      BOOL:	YES = successed with no Error.
//              NO  = Error occured;
- (BOOL) errorCountsWithPhyLayerError: (uint16_t*) phyLayerError
                       linkLayerError: (uint16_t*) linkLayerError
    numOfEntrancesToUSB3RecoveryState: (uint16_t*) numOfRecoverState
                            withError: (NSError**) aError;
//
//  reset a selected IC on Caesium.
//      ATDeviceCaesiumFX3      (Note: this will force the FX3 back to SS operation, so reissuing a SPDc or HTPG is highly recommended if running this command)
//      ATDeviceCaesiumASMedia
//      ATDeviceCaesiumLSController
//      ATDeviceCaesiumAce
//      ATDeviceCaesiumW5500
//      ATDeviceCaesiumSATA

// return value
//      BOOL:	YES = successed with no Error.
//              NO  = Error occured;

- (BOOL) resetSelectedIC: (ATDeviceCaesiumSelectedIC) selectedIC  withError:(NSError**) aError;




@end
