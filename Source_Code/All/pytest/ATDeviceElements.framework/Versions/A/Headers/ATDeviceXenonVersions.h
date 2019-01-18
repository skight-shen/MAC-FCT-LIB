//
//  ATDeviceXenonVersions.h
//  ATDeviceElements
//
//  Created by Sai  on 4/19/17.
//  Copyright © 2017 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <ATDeviceElements/ATDeviceVersions.h>

#define kATDXenonInfoSize 25

@interface ATDeviceXenonVersions : ATDeviceVersions

@property (nonatomic) uint32_t stmFwVersion;
@property (nonatomic) uint32_t fx3FwVersion;
@property (nonatomic) uint32_t legacyAceFwVersion;
@property (nonatomic) uint32_t superSpeedAceFwVersion;
@property (nonatomic) uint32_t tbtControllerFwVersion; // not checked currently
@property (nonatomic) uint32_t hwVersion;
@property (nonatomic) uint32_t lowSpeedControllerFwVersion;

-(id) initWithData:(NSData*) data;

@end
