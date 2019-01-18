//
//  ATDHippoCommon.h
//
//  Created by Sai  on 11/16/16.
//  Copyright © 2016 htwe. All rights reserved.
//

#ifndef ATDHippoCommon_h
#define ATDHippoCommon_h

//  parameter = data
typedef void (^SerialDataCallBack)( NSData *_Nonnull);
//  parameter = src UDP Port number (dock channel) and data
typedef void (^HippoChannelCallBack)( NSNumber *_Nonnull, NSData *_Nonnull);
//  parameter = src UPD Port number (dock channel)
typedef void (^NewHippoChannelAddedCallBack)( NSNumber *_Nonnull);

typedef NS_ENUM(int, ATDHippoError) {
    
    ATDHippoSystemError = -2,
    ATDHippoUserError = -1,
};


#endif /* ATDHippoCommon_h */
