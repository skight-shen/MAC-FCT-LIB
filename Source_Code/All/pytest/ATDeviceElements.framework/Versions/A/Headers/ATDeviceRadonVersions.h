//
//  ATDeviceRadonVersions.h
//  ATDeviceElements
//
//  Created by Sai  on 4/21/17.
//  Copyright © 2017 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <ATDeviceElements/ATDeviceVersions.h>


#define kATDRadonInfoSize 62

@interface ATDeviceRadonVersions : ATDeviceVersions

@property (nonatomic) uint32_t stmFwVersion;
@property (nonatomic) uint32_t fpgaFwVersion;
@property (nonatomic) uint64_t athena1FwVersion;
@property (nonatomic) uint64_t athena2FwVersion;
@property (nonatomic) uint64_t vega1FwVersion;
@property (nonatomic) uint64_t vega2FwVersion;
@property (nonatomic) uint32_t athena1EdidFwVersion;
@property (nonatomic) uint32_t athena2EdidFwVersion;
@property (nonatomic) uint32_t ace1TBTPortAFwVersion;
@property (nonatomic) uint32_t ace2RedrivenDPFwVersion;
@property (nonatomic) uint32_t ace3NativeDPInFwVersion;
@property (nonatomic) uint32_t ace4NativeDPOutFwVersion;
@property (nonatomic) uint32_t alpinRidgeFwVersion;
@property (nonatomic) uint32_t sil9777FwVersion;
@property (nonatomic) uint32_t hdmiEdidFwVersion;
@property (nonatomic) uint32_t dviEdidFwVersion;
@property (nonatomic) uint32_t hwVersion;

-(id) initWithData:(NSData*) data;

@end
