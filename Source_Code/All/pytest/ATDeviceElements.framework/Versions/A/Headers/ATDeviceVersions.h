//
//  ATDeviceVersions.h
//  ATDeviceElements
//
//  Created by Sai  on 4/19/17.
//  Copyright © 2017 htwe. All rights reserved.
//

#import <Foundation/Foundation.h>

typedef NS_ENUM(int8_t, ATDVersionResult) {
    ATDVersionResultSame = 0,
    ATDVersionResultGreaterThanOrEqual = 1,
};

@interface ATDeviceVersions : NSObject

- (id) initWithData:(NSData*) data;

- (BOOL) isMatchedWithRetrievedData: (NSData*) retrievedData
                            andError: (NSError**) aError;

- (BOOL) isMatchedWithRetrievedVerions: (ATDeviceVersions*) retrievedVersions
                               andError: (NSError**) aError;

- (BOOL) compareSTMVersionWithExpected: (uint32_t) expected
                          andRetreived: (uint32_t) retrieved
                     andExpectedResult: (ATDVersionResult) expectedResult
                              andError: (NSError**) aError;


- (BOOL) compareBcdVersionWithExpected: (uint32_t) expected
                          andRetreived: (uint32_t) retrieved
                     andExpectedResult: (ATDVersionResult) expectedResult
                              andError: (NSError**) aError;

- (BOOL) compare64bitsVersionWithExpected: (uint64_t) expected
                             andRetreived: (uint64_t) retrieved
                        andExpectedResult: (ATDVersionResult) expectedResult
                                 andError: (NSError**) aError;



@end
