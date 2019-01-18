//
//  ATDeviceTBTInterface.h
//  ATDeviceElements
//
//  Created by Sai  on 1/26/17.
//  Copyright © 2017 htwe. All rights reserved.
//

#import "ATDeviceBusInterfaceBase.h"



@interface ATDeviceTBTInterface : ATDeviceBusInterface

// initWithRid
// rid = ridge ID.
// route = route string
// You can find them in ioreg or IORegistryExplorer
- (id)initWithRid:(uint8_t)rid andRoute: (uint64_t) route;


- (uint32_t) deviceID: (NSError**) error;
@end
