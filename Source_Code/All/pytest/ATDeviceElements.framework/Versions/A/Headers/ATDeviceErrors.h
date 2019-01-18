//
//  ATDeviceErrors.h
//  ATDeviceElements
//
//  Created by Sai  on 9/22/16.
//  Copyright © 2016 htwe. All rights reserved.
//

#ifndef ATDeviceErrors_h
#define ATDeviceErrors_h



typedef NS_ENUM(int, ATDErrorCode) {
    
    ATDeviceRegisterReadError       = -11,
    ATDeviceVersionFailed           = -10,
    ATDeviceNotSupportFunction      = -9,
    ATDeviceUSBCPowerContractError  = -8,
    ATDeviceTimedOut                = -7,
    ATDeviceUSBMUxNotSetRight       = -6,
    ATDDeviceNotOpened              = -5,
    ATDTBTDeviceError               = -4,
    ATDUSBDeviceError               = -3,
    ATDUserError                    = -2,
    ATDSystemError                  = -1,
    ATDeviceSuccess                 =  0,
   
};

#endif /* ATDeviceErrors_h */
