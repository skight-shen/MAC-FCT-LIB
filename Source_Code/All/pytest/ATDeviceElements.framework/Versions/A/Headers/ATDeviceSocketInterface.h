//
//  ATDeviceSocketInterface.h
//
//  Created by Sai  on 6/24/16.
//  Copyright © 2016 Apple Inc . All rights reserved.
//

#import <Foundation/Foundation.h>
#import "ATDeviceBusInterfaceBase.h"

@interface ATDeviceSocketInterface : ATDeviceBusInterface


- (id)initWithIPAddress:(NSString*)aIP;

@property (copy) NSString * IPaddress;

@end
