//
//  ATDeviceExtensionBoard.h
//  ATDeviceElements
//
//  Created by Sai  on 4/3/17.
//  Copyright © 2017 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "ATDeviceCarbon.h"



@interface ATDeviceExtensionBoard : NSObject



-(nullable id) initWithFixtureController: (nonnull ATDeviceCarbon* ) aFixtureController;


// Master board such Oxygen should override the attachExtensionBoard function
// attachExtensionBoard will call configure: to configure all the extension boards.
- (BOOL) attachExtensionBoard: (nonnull ATDeviceExtensionBoard*) board andError:(NSError *_Nullable*_Nullable) aError;

// addresses Dictionary's Keys are defined in ATDeviceExtBoardCommon.h
// concrete class must implement this updateBoardAddress function.
- (void)        updateBoardAddress: (NSUInteger) newBoardAddress
                 andOtherAddresses: (nullable NSDictionary*) addresses;

// configure anything required by the board. e.g. i2c stuff.
- (BOOL) configure: (NSError *_Nullable*_Nullable) aError;


//--------------------------------------------------------------
//Read Digital IN
//args:
//  indexOfDIN = DIN
- (uint8) readDIO: (uint8) indexOfDIN
         andError: (NSError *_Nullable*_Nullable) aError;

// Default isDigitalOutputOKAtBank just let the nextBoard to handle
// Concrete class must implement readDIO if it can handle it
- (BOOL) isDigitalOutputOKAtBank:(uint8)bankIndex
                        andError:(NSError *_Nullable*_Nullable) aError;


//--------------------------------------------------------------
//Write Digital OUT
//args:
//  indexOfDOUT = DOUT 
//  highOrLow YES = High or NO = Low
//
- (BOOL) writeDIO: (uint8)indexOfDOUT
        withValue: (BOOL)high
         andError: (NSError *_Nullable*_Nullable) aError;

@property (nonatomic, strong)  ATDeviceCarbon* _Nullable fixtureController;
@property (nonatomic, strong)  ATDeviceExtensionBoard* _Nullable nextBoard;
// General boardAddress
@property (nonatomic) NSUInteger boardAddress; //set with the switch on the board.





@end
