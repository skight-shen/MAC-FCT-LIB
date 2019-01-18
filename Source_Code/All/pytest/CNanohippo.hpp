//
//  CNanohippo.hpp
//  pytest
//
//  Created by prmeasure on 2018/5/14.
//  Copyright © 2018 mental. All rights reserved.
//

#ifndef CNanohippo_HH
#define CNanohippo_HH

#include <stdio.h>
#include <string>


//#include <boost/python.hpp>
class NanoHippoDev ;
class cNanoHippoDev
{
    
public:
    cNanoHippoDev();
    ~cNanoHippoDev();
    
public:
    //port=-1 for serial others for hippo;
    int CreatePub(std::string strUrl,int nPort);
    int CreateRep(std::string strUrl);
    int Open(std::string strSerial);
    int Close();
    int CloseZMQ();
    int SetPubOpt(int nNeedPub);
    
    
    //set write wait micro sec per byte
    int SetWriteTimeInterval(unsigned int usleeps);
    int WriteString(int nPort,std::string strBuf);
    int WriteBytes(int nPort,std::string strData, int nLen);
    int WriteStringBytes(int nPort,std::string strData);
    
    std::string ReadString(int nPort);
    std::string ReadBytes(int nPort);
    std::string ReadStringBytes(int ponPortrt);
    std::string ReadChannels();
    std::string GetDetectString();
    void ClearBuffer(int nPort);
    int SetDetectString(std::string strDet);
    int WaitDetect(int nPort, int nTimeOut);  //msec
    int IsDataReady(int nPort);
    
    //port=-1 for default log file
    int SetLogFile(int nPort,std::string strPath);
    
    void SetAppendBufTimeStamp(bool bFlag);
    void SetFilterColorCode(bool fbFlaglag);
    void SetFilterUnreadable(bool bFlag);
    int  WritePassControlBit(int nPort, int stationid,std::string strCmd);
    void Log_file_timestamp(int nPort,std::string strTime);
    
    
    //    NSData *GetDataBuff(int port);
    //    NSString * ConvertDataToStr(NSData * data);
    //    NSString * LocalTimeStampStr();
    //    void _log_file_timestamp(int port,NSString *str);
    //    void _log_smc_file(int port, NSString *string);
    
private:
    NanoHippoDev *  m_NanoHippoDev;
};
/*
BOOST_PYTHON_MODULE(NanoHippoDev)
{
    class_<cNanoHippoDev>("cNanoHippoDev")
    .def("CreatePub", &cNanoHippoDev::CreatePub)
    .def("CreateRep", &cNanoHippoDev::CreateRep)
    ;
}

*/


#endif /* CNanohippo_hpp */
