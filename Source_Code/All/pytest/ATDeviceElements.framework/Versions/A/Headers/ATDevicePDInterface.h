//
//  ATDevicePDInterface.h
//  ATDeviceElements
//
//  Created by Sai  on 7/25/16.
//  Copyright © 2016 Apple Inc. All rights reserved.
//

#import "ATDeviceBusInterfaceBase.h"

@interface ATDevicePDInterface : ATDeviceBusInterface


- (id)initWithRid:(uint8_t)rid andRoute: (uint64_t) route
                 andPDControllerAddress: (uint32_t) address;


@end
