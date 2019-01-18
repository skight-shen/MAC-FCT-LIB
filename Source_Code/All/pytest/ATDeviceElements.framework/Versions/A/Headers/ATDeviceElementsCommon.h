//
//  ATDeviceElementsCommon.h
//  ATDeviceElements
//
//  Created by Sai  on 3/15/17.
//  Copyright © 2017 htwe. All rights reserved.
//

#ifndef ATDeviceElementsCommon_h
#define ATDeviceElementsCommon_h

typedef NS_ENUM(uint32_t, ATDeviceElementsID) {
    ATDevice_INVALID_ID      = 0,
    ATDevice_PALLADIUM_ID    = 0xD0010001,
    ATDevice_SPADE_ID        = 0xD0020001,
    ATDevice_XENON_ID        = 0xD0020002,
    ATDevice_POTASSIUM_ID    = 0xD0020003,
    ATDevice_GALLIUM_ID      = 0xD0030001,
    ATDevice_RADON_ID        = 0xD0040001,
    ATDevice_DUST_ID         = 0xD0070001,
    ATDevice_CARBON_ID       = 0xD0080001,
};
#endif /* ATDeviceElementsCommon_h */
