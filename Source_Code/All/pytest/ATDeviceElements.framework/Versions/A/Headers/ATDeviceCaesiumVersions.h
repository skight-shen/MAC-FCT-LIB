//
//  ATDeviceCaesiumVersions.h
//  ATDeviceElements
//
//  Created by Sai  on 4/19/17.
//  Copyright © 2017 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <ATDeviceElements/ATDeviceVersions.h>

#define kATDCaesiumInfoSize 17

@interface ATDeviceCaesiumVersions : ATDeviceVersions

@property (nonatomic) uint32_t stmFwVersion;
@property (nonatomic) uint32_t fx3FwVersion;
@property (nonatomic) uint32_t aceFwVersion;
@property (nonatomic) uint32_t lowSpeedControllerFwVersion;
@property (nonatomic) uint32_t hwVersion;

-(id) initWithData:(NSData*) data;

@end
