//
//  CNanohippo.cpp
//  pytest
//
//  Created by prmeasure on 2018/5/14.
//  Copyright © 2018 mental. All rights reserved.
//

#include "CNanohippo.hpp"


cNanoHippoDev::cNanoHippoDev(){
    m_NanoHippoDev = new NanoHippoDev();
}
cNanoHippoDev::~cNanoHippoDev(){
    delete  m_NanoHippoDev ;
}
int cNanoHippoDev::CreatePub(std::string strUrl,int nPort){
    return m_NanoHippoDev->CreatePub(strUrl.c_str(), nPort ) ;
}
int cNanoHippoDev::CreateRep(std::string strUrl){
     return m_NanoHippoDev->CreateRep(strUrl.c_str());
}
int cNanoHippoDev::Open(std::string strSerial){
     return m_NanoHippoDev->Open(strSerial.c_str()) ;
}
int cNanoHippoDev::Close(){
     return 0 ;
}
int cNanoHippoDev::CloseZMQ(){
     return 0 ;
}
int cNanoHippoDev::SetPubOpt(int nNeedPub){
     return 0 ;
}
    
    
    //set write wait micro sec per byte
int cNanoHippoDev::SetWriteTimeInterval(unsigned int usleeps){
     return 0 ;
}
int cNanoHippoDev::WriteString(int nPort,std::string strBuf){
     return 0 ;
}
int cNanoHippoDev::WriteBytes(int nPort,std::string strData, int nLen){
     return 0 ;
}
int cNanoHippoDev::WriteStringBytes(int nPort,std::string strData){
     return 0 ;
}
    
std::string cNanoHippoDev::ReadString(int nPort){
     return "" ;
}
std::string cNanoHippoDev::ReadBytes(int nPort){
    return "" ;
}
std::string cNanoHippoDev::ReadStringBytes(int ponPortrt){
    return "" ;
}
std::string cNanoHippoDev::ReadChannels(){
    return "" ;
}
std::string cNanoHippoDev::GetDetectString(){
    return "" ;
}
void cNanoHippoDev::ClearBuffer(int nPort){
    
}
int cNanoHippoDev::SetDetectString(std::string strDet){
    return 0 ;
}
int cNanoHippoDev::WaitDetect(int nPort, int nTimeOut){
    return 0 ;
} //msec
int cNanoHippoDev::IsDataReady(int nPort){
    return 0 ;
}
    
    //port=-1 for default log file
int cNanoHippoDev::SetLogFile(int nPort,std::string strPath){
    return 0 ;
}
    
void cNanoHippoDev::SetAppendBufTimeStamp(bool bFlag){
    
}
void cNanoHippoDev::SetFilterColorCode(bool fbFlaglag){
    
}
void cNanoHippoDev::SetFilterUnreadable(bool bFlag){
    
}
int  cNanoHippoDev::WritePassControlBit(int nPort, int stationid,std::string strCmd){
    return 0 ;
}
void cNanoHippoDev::Log_file_timestamp(int nPort,std::string strTime){
    
}





//#include "pytest/NanohippoBridge.cpp"
