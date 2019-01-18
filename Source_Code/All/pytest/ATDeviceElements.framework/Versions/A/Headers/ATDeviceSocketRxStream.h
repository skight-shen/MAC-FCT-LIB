//
//  ATDeviceSocketRxStream.h
//  TestNSStream
//
//  Created by Sai  on 11/1/16.
//  Copyright © 2016 Sai . All rights reserved.
//

#import <Foundation/Foundation.h>

typedef void (^ATDeviceSocketRx_block_t)(NSString* str); // decode as  NSASCIIStringEncoding

typedef void (^ATDeviceSocketRx_NSData_block_t)(NSData* data); // decode as NSData

typedef void (^ATDeviceSocketRxError_block_t)(NSError* anError);

@interface ATDeviceSocketRxStream : NSObject <NSStreamDelegate>

// decode as  NSASCIIStringEncoding
- (BOOL)socketStreamRxStartWithHost:(NSString *)host
                            andPort:(int)port
                           andDataAvailable:(ATDeviceSocketRx_block_t) dataAvailable
                      andErrorOccur:(ATDeviceSocketRxError_block_t)errorOccur
                            andError:(NSError**) aError;

// decode as  NSData
- (BOOL)socketStreamRxStartWithHost:(NSString *)host
                            andPort:(int)port
                 andNSDataAvailable:(ATDeviceSocketRx_NSData_block_t) dataAvailable
                      andErrorOccur:(ATDeviceSocketRxError_block_t)errorOccur
                           andError:(NSError**) aError;

- (void)close;
@end
