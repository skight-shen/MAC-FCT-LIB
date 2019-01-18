//
//  ATDeviceBusInterfaceBase.h

//
//  Created by Sai  on 6/29/16.
//  Copyright © 2016 Apple Inc. All rights reserved.
//

#import <Foundation/Foundation.h>



@interface ATDeviceBusInterface : NSObject


-(BOOL) readRegisterAtAddress:(NSUInteger)address
                   withLength:(NSUInteger)length
                         data:(uint8_t *)data
                        error:(NSError **)error;

-(NSArray *) readRegistersAtAddresses:(NSArray *)addresses
                                error:(NSError **)error;

-(BOOL) writeRegisterAtAddress:(NSUInteger)address
                        length:(NSUInteger)length
                          data:(uint8_t *)data
                         error:(NSError **)error;

-(BOOL) execute4ccCommand:(NSString*)command4cc
                 withArgs:(uint32_t)args
                 withData:(uint8_t*)data
              writeLength:(NSUInteger)writeLength
               readLength:(NSUInteger)readLength
      timeoutMilliseconds:(NSUInteger)timeoutMilliseconds
                    error:(NSError **) error;

-(uint16_t) crc16: (uint16_t) crc andData:(uint8_t) data;


// Child classes must implment these 4 functions
- (int) readCTDIRegisterWithAddress: (uint8_t) address
                          andLength: (uint8_t) length
                           andValue: (uint8_t*) value
                              error: (NSError **)error;

- (int) writeCTDIRegisterWithAddress: (uint8_t) address
                           andLength: (uint8_t) length
                            andValue: (uint8_t*) value
                               error: (NSError **)error;

-(BOOL) close;

// Open or Reopen the Interface.
-(BOOL) openWithError:(NSError **) error;
@end
