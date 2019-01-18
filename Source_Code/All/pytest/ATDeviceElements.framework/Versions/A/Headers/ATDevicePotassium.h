//
//  ATDevicePotassium.h
//  ATDeviceElements
//
//  Created by Sai  on 11/9/16.
//  Copyright © 2016 htwe. All rights reserved.
//

#import <ATDeviceElements/ATDeviceElements.h>


#define kATDPotassiumProductID 0x1636
#define kATDPotassiumBCDeviceID 0x0001


@interface ATDevicePotassium : ATDeviceElement

- (BOOL) turnLED_ONapplyToRed: (BOOL) applyToRed
              andApplyToGreen: (BOOL) applyToGreen
             andApplyToYellow: (BOOL) applyToYellow
                     andError: (NSError**) aError;

- (BOOL) turnLED_OFFapplyToRed: (BOOL) applyToRed
               andApplyToGreen: (BOOL) applyToGreen
              andApplyToYellow: (BOOL) applyToYellow
                      andError: (NSError**) aError;

- (BOOL) blinkLEDapplyToRed: (BOOL) applyToRed
            andApplyToGreen: (BOOL) applyToGreen
           andApplyToYellow: (BOOL) applyToYellow
               andBlinkRate: (uint16_t) blinkRate
                   andError: (NSError**) aError;

- (BOOL) readTargetVBus: (double*) targetVBus
          andChargeVBus: (double*) chargeVBus
             andSamples: (uint32_t) samples
               andError: (NSError**) aError;

- (BOOL) setDebugLevel: (uint8_t) level
              andError: (NSError**) aError;

- (BOOL) startHeartbeatWithTimeout: (uint32_t) timeout
                          andError: (NSError**) aError;

- (BOOL) sendHeartbeatWithError: (NSError**) aError;

- (BOOL) cancelHeartbeatWithError: (NSError**) aError;

- (BOOL) saveEnvironmentWithError: (NSError**) aError;

- (BOOL) sendForceDFUWithError: (NSError**) aError;

- (BOOL) setSWDPollingPeriod: (uint32_t) period
             andActualPeriod: (uint32_t*) currentPeriod
                    andError: (NSError**) aError;

- (BOOL) emulateDisconnectOnPort: (uint8_t) port
                     forDuration: (uint16_t) duration
                       withError: (NSError**) aError;

- (BOOL) sendRequestForVoltage: (uint16_t) voltage
                    andCurrent: (uint16_t) current
                     withError: (NSError**) aError;

- (BOOL) powerRoleSwapToSourceWithError: (NSError**) aError;

- (BOOL) powerRoleSwapToSinkWithError: (NSError**) aError;

- (BOOL) startAppleDebugModeWithError: (NSError**) aError;

- (BOOL) startAppleUSBModeWithError: (NSError**) aError;

- (BOOL) useBananaCircuit: (BOOL) enable
       withStartupTimeout: (uint16_t) timeout
                withError: (NSError**) aError;

- (BOOL) getBananaSerialNumber: (uint8_t*) serialNumber
                     withError: (NSError**) aError;

- (BOOL) getBananaVersion: (uint32_t*) version
                withError: (NSError**) aError;

- (BOOL) getBananaUSBState: (ATDeviceBananaUSBState*) state
                 withError: (NSError**) aError;

- (BOOL) bananaTypeKeys: (uint8_t*) keycodes
       withModifierKeys: (uint8_t) modifiers
        withSpecialKeys: (uint8_t) specials
            forDuration: (uint16_t) duration
              withError: (NSError**) aError;

- (BOOL) bananaReleaseAllKeysWithError: (NSError**) aError;

@end
