/*
 *  IPSFCPost_API.h
 *  IPSFCPost
 *
 *  Created on 9/11/10.
 *  Copyright 2010 Apple Inc. All rights reserved.
 *
 */
#ifndef IPSFCPost__API__HH__
#define IPSFCPost__API__HH__

struct QRStruct {
	char * Qkey;
	char * Qval;
};


#ifdef WIN32
	#define EXPORT __declspec(dllexport)
#else
	#define EXPORT __attribute__((visibility("default")))
#endif     //WIN32

#ifdef __OBJC__

	#import <Foundation/Foundation.h>
	/* returns version string */
	EXPORT const char * SFCLibVersion(void);
	EXPORT const char * SFCServerVersion(const char * acpURL,int aiTimeOut);
	EXPORT const char * SFCQueryHistory(const char * acpSerialNumber, const char * acpURL,int aiTimeOut);
	EXPORT const char * SFCQueryRecordByStationName(const char * acpSerialNumber,const char * acpStationName,const char* acpParams, const char * acpURL,int aiTimeOut);
	EXPORT const char * SFCQueryRecordUnitCheck(const char * acpSerialNumber,const char * acpStationID, const char * acpURL,int aiTimeOut);
	EXPORT const char * SFCAddRecord(char** cppParams);
	EXPORT int SFCQueryRecord(const char * acpSerialNumber, struct QRStruct *apQRStruct[],int aiSize);

	EXPORT	void FreeSFCBuffer(const char * cpBuffer);

#else /* __OBJC__ */



#ifdef __cplusplus
	extern "C" {
#endif

		
	/* returns version string */
	EXPORT const char * SFCLibVersion(void);
	EXPORT const char * SFCServerVersion(const char * acpURL,int aiTimeOut);
	EXPORT const char * SFCQueryHistory(const char * acpSerialNumber, const char * acpURL,int aiTimeOut);
	EXPORT const char * SFCQueryRecordByStationName(const char * acpSerialNumber,const char * acpStationName,const char* acpParams, const char * acpURL,int aiTimeOut);
	EXPORT const char * SFCQueryRecordUnitCheck(const char * acpSerialNumber,const char * acpStationID, const char * acpURL,int aiTimeOut);
	EXPORT const char * SFCAddRecord(char** cppParams);
	EXPORT int SFCQueryRecord(const char * acpSerialNumber, struct QRStruct *apQRStruct[],int aiSize);
	
	EXPORT	void FreeSFCBuffer(const char * cpBuffer);
	

#ifdef __cplusplus
	}
#endif


#endif /* __OBJ__ */
#endif /* IPSFCPost__API__HH__ */

