//
//  ATDevicePalladiumVersions.h
//  ATDeviceElements
//
//  Created by Sai  on 4/20/17.
//  Copyright © 2017 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <ATDeviceElements/ATDeviceVersions.h>

#define kATDPalladiumInfoSize 40

@interface ATDevicePalladiumVersions : ATDeviceVersions

@property (nonatomic) uint32_t stmFwVersion;
@property (nonatomic) uint32_t fpgaFwVersion;
@property (nonatomic) uint32_t cedarFwVersion;
@property (nonatomic) uint64_t vegaFwVersion; //Not checked for now.
@property (nonatomic) uint32_t edidFwVersion;
@property (nonatomic) uint32_t ace1TBTPortAFwVersion;
@property (nonatomic) uint32_t ace2RedrivenDPFwVersion;
@property (nonatomic) uint32_t ace3NativeDPFwVersion;
@property (nonatomic) uint32_t ace4TBTPortBFwVersion;
@property (nonatomic) uint32_t alpinRidgeFwVersion;
@property (nonatomic) uint32_t hwVersion;

-(id) initWithData:(NSData*) data;


@end
