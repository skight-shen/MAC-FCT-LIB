//
//  ATDeviceUSBInterface.h
//  ATDeviceElements
//
//  Created by Sai  on 11/8/16.
//  Copyright © 2016 htwe. All rights reserved.
//

#import <ATDeviceElements/ATDeviceElements.h>
#import "ATDeviceBusInterfaceBase.h"

typedef NS_ENUM(int, ATDeviceInterfaceStatus)
{
    kADBoxUSBDeviceError            = -5,
    kADBoxUSBRequestError           = -4,
    kADBoxUSBNotOpen                = -3,
    kADBoxUSBInvalidResponse        = -2,
    kADBoxUSBTimeOut                = -1,
    kADBoxUSBStatusGood             = 0,
};

@interface ATDeviceUSBInterface : ATDeviceBusInterface

// Users can init with the USB Location ID
- (id)initWithUSBLocationId:(uint32) locationId;

// Or Users can use USB VendorID, ProductID and BCDevice.
- (id)initWithVendorId: (uint16_t) aVid
          andProductId: (uint16_t) aPid
           andBCDevice: (uint16_t) aBCDevice;
@end
