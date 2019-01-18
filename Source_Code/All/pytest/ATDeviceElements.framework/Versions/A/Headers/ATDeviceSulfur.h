//
//  ATDeviceSulfur.h
//  ATDeviceElements
//
//  Created by Sai  on 4/3/17.
//  Copyright © 2017 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "ATDeviceExtensionBoard.h"

@interface ATDeviceSulfur : ATDeviceExtensionBoard

// Base class ATDeviceExtensionBoard has this initWithFixtureController function
-(nullable id) initWithFixtureController: (nonnull ATDeviceCarbon* ) aFixtureController;


+ (nullable id) create: (NSInteger) numberOfSulfur
        SulfurWithFixtureController: (nonnull ATDeviceCarbon* ) aFixtureController;

- (void) updateAllBoardToI2cBusId: (NSUInteger) aI2CBusId;

@property (nonatomic) NSUInteger i2cBusId; // for users not use the default I2c bus, they can directly change this property.
@property (nonatomic) NSUInteger startDINIndex;
@property (nonatomic) NSUInteger startDOUTIndex;
@property (nonatomic) NSUInteger startBankIndex;

@end
