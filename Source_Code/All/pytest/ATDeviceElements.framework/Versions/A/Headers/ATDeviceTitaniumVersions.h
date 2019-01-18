//
//  ATDeviceTitaniumVersions.h
//  ATDeviceElements
//
//  Created by Sai  on 8/14/17.
//  Copyright © 2017 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <ATDeviceElements/ATDeviceVersions.h>

#define kATDTitaniumInfoSize 40

@interface ATDeviceTitaniumVersions : ATDeviceVersions

@property (nonatomic) uint32_t stmFwVersion;
@property (nonatomic) uint64_t fpgaFwVersion;
@property (nonatomic) uint32_t tbtAFwVersion;
@property (nonatomic) uint32_t tbtBFwVersion;
@property (nonatomic) uint32_t dpTx1FwVersion;
@property (nonatomic) uint32_t dpRx1FwVersion;
@property (nonatomic) uint32_t dpTx0FwVersion;
@property (nonatomic) uint32_t alpinRidgeFwVersion;
@property (nonatomic) uint32_t hwVersion;

-(id) initWithData:(NSData*) data;

@end
