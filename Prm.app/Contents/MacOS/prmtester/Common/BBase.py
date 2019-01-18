import time
import re
import subprocess
import logging
import threading
from abc import ABCMeta, abstractmethod
import zmq
import socket
import json
import serial
import os
import signal
from subprocess import Popen


from multiprocessing import Lock,Process

class cBaseProcessLock(object):
    """docstring for cBaseLock"""
    objLock  = Lock()
    def __init__(self):
        pass

    def Lock(self,bFlag):
        self.objLock.acquire() if bFlag else self.objLock.release()



class cBaseProcess(object):
    """docstring for cBaseProcessManager"""
    def __init__(self,*Arsg):
        self.bStatu=False
        self.process = None
        self.objLock = cBaseProcessLock()
        self.listCmd =["python"]
        for i in Arsg:
            self.listCmd.append(i)
        print "cmd : {}".format(self.listCmd)
    def GetStatu(self):
        return self.bStatu
    def StartProcess_n(self):

        self.process = Popen(self.listCmd)
        self.bStatu = True
    def StopProcess(self):
        self.bStatu=False
        os.kill(self.process.pid,signal.SIGKILL)

class cBaseThreadLock(object):
    """docstring for cBaseLock"""
    objLock  = threading.Lock()
    def __init__(self):
        pass

    def Lock(self,bFlag):
        self.objLock.acquire() if bFlag else self.objLock.release()
class cBaseThread(threading.Thread):
    """docstring for cBaseProcessManager"""
    objLock = cBaseThreadLock()
    dictThread = {}
    __metaclass__ = ABCMeta

    def __init__(self,dictArgs =None):
        self.dictArgs= dictArgs
        self.objTimer = cBruceTime()

        self.bRun = True
    def Lock(self,bFlag):
        self.objLock.Lock(bFlag)

    def Stop(self):
        self.bRun = False
        self.StopDo()

    @abstractmethod
    def StopDo(self):
        pass

    def run(self):
        self.bRun = True
        while self.bRun:
            #nEndtime = self.objTimer.Current() + self.nTimeOut
            self.ThreadDo()

    @abstractmethod
    def ThreadDo(self):
        pass





class cBruceConfig(object):
    """docstring for cBruceLog"""
    def __init__(self,strPath,strType="json"):
        self.Type = strType
        self.Path=strPath
        self.Config={}
        self.Statu=False
        self.Load()
    def Load(self):
        bRet=True
        try:
            if self.Type.lower()=="json":
                #add path check here
                f = open(self.Path, 'rU')
                self.Config = json.load(f)
                f.close()
        except Exception as e:
            #print "cBruceConfig Get Exception {}".format(str(e))
            bRet=False
        self.Statu=bRet
        return bRet
    def GetDict(self):
        return self.Config
    def GetConfig(self,strKey):
        strRet=""
        if self.Statu:
            strRet = self.Config.get(strKey)
        else:
            pass
            #print "cBruceConfig Get {} from {}".format(strKey, self.Config)
        return  strRet




class cBruceBuf:
    def __init__(self,buffer):
        self.SetBuf(buffer)
    def Char2Int(self,nInput):
        bRet =True
        hexRet=""
        try:
            hexRet = ord(nInput)
        except:
            bRet=False
        return bRet,hexRet

    def SetBuf(self,buffer):
        self.Buffer = buffer
        self.nMax = len(self.Buffer)
        self.nStartIndex = 0
        self.nEndIndex = 0
        self.bEndFlag = False
    def Read(self,nSize):
        strRet = ""
        bRet = True
        if not self.bEndFlag:
            if self.nStartIndex <self.nMax:
                self.nEndIndex = self.nStartIndex + nSize
                if self.nEndIndex >self.nMax:
                    self.nEndIndex = -1
                    self.bEndFlag = True
                if self.bEndFlag:
                    strRet = self.Buffer[self.nStartIndex:]
                else:
                    strRet = self.Buffer[self.nStartIndex:self.nEndIndex]
                self.nStartIndex = self.nEndIndex
            else:
                self.bEndFlag = True
        else:
            bRet = False
        return bRet,strRet
import mmap
class cBaseMmap:
    def __init__(self, strFilePath,nStep):
        self.nIndex = 0
        self.nStep = nStep
        file = open(strFilePath, "r+")
        filefid = file.fileno()
        self.map = mmap.mmap(filefid, 0)
    def flush(self):
        self.map.flush()
    def reset(self):
        self.nIndex = 0
    def rawwrite(self, rawdata):
        try:
            self.map.seek(self.nIndex*self.nStep)
            self.map.write(rawdata)
            self.nIndex+=1
        except:
            print "Raw Write Error"
    def rawread(self):
        xRet=None
        try:
            self.map.seek(self.nIndex*self.nStep)
            xRet = self.map.read(self.nStep)
            self.nIndex=self.nIndex+1
        except Exception as e:
            xRet=None
        return xRet
class cShell:
    def __init__(self):
        pass
    def RunShell_n(self, strCmd):
        nRet = -1
        try:
            nRet = os.system(str(strCmd))
        except:
            #print "RunShell {} Except".format(str(strCmd))
            nRet = -1
        return nRet
    def RunShell(self, *args):
        bRet = True
        try:
            listcommand = []
            strCommand = ""
            for i in args:
                if strCommand == "":
                    strCommand = "{}".format(i)
                else:
                    strCommand = "{} {}".format(strCommand, i)
            listcommand.append(strCommand)
            pipeHandle = subprocess.Popen(listcommand, shell=True, stdout=subprocess.PIPE)

        except:
            #print "RunShell {} Except".format(str(args))
            bRet = False
        return bRet
    def RunShell_b_str(self,*args):

        bRet =True
        strRet = ""
        try:
            listcommand = []
            strCommand=""
            for i in args:
                if strCommand=="":
                    strCommand="{}".format(i)
                else:
                    strCommand = "{} {}".format(strCommand,i)
            listcommand.append(strCommand)

            pipeHandle = subprocess.Popen(listcommand,shell=True,stdout=subprocess.PIPE)
            #print "{}".format(str(listcommand))
            strRet = pipeHandle.stdout.read()
        except:
            strRet = "RunShell_b_str {} Except".format(str(args))
            bRet = False
        return bRet,strRet


        

class cBaseFolder():
    def __init__(self):
        pass
    def CreateFodler(self,strPath):
        if os.path.exists(strPath) == False:
            os.makedirs(strPath)
    def CheckExist(self,strPath):
        return os.path.exists(strPath)

class cBruceTime(object):
    """docstring for cBruceTime"""
    def __init__(self):
        super(cBruceTime, self).__init__()
        self.nStartTimeTemp = 0
    def Start(self):
        self.nStartTimeTemp = time.time()
    def Stop_n(self):
        return  float(round((time.time()-self.nStartTimeTemp)*1000))
    #Functions
    def Delay(self,nRelayMSecTime):
        time.sleep(float(nRelayMSecTime)/1000)
    def Current(self):
        return time.time()*1000
    def CurrentStr(self,strFormat="%Y-%m-%d-%H-%M-%S"):
        return self.TempToStr(time.time(),strFormat)
    def StrToTemp(self,strTime,strFormat):
        return time.mktime(time.strptime(strTime,strFormat))
    def TempToStr(self,nTimeTemp,strFormat):
        return time.strftime(strFormat,time.localtime(nTimeTemp))
class cLocalLogs(object):
    objTime = cBruceTime()
    def __init__(self,strPath,strMode="w+"):
        self.file=open(strPath,strMode)
    def Flush(self):
        self.file.flush()
    def Trace(self,strInfo):
        self.file.write("{}{}\n".format(self.objTime.CurrentStr(),strInfo))
        self.file.flush()
    def Close(self):
        self.file.close()

class cBruceRe(object):
    """docstring for cBruceRe"""
    def __init__(self):
        pass
    def MatchStr_b(self,strMessage,strRex):
        bRet = True
        try:
            listRet = re.findall(strRex,strMessage)
            if len(listRet)<=0:
                bRet = False
            elif listRet[0]=="":
                bRet=False
        except Exception as e:
            bRet = False
        return bRet
    def MatchStr_b_list(self,strMessage,strRex):
        bRet = True
        listRet=[]
        try:
            listRet = re.findall(strRex,strMessage)
            if len(listRet)<=0:
                bRet = False
            elif listRet[0]=="":
                bRet=False
        except Exception as e:
            bRet = False
        return bRet,listRet
    def MatchOrInList_b(self,listStrMessage,strRex):
        bRet = False
        try:
            for strMes in listStrMessage:

                listRet = re.findall(strMes,strRex)
                if len(listRet) >0:
                    bRet = True
                    break
                else:
                    bRet = False
        except Exception as e:
            bRet = False
        return bRet


    def SplitStr_b_list(self,strMessage,strRex):
        bRet = True
        listRet=[]
        try:
            listRet = re.split(strRex,strMessage)
            if len(listRet)<=0:
                bRet = False
        except Exception as e:
            bRet = False
        return bRet,listRet

    def SubStr_b_str(self,strMessage,strRex,strReplace):
        bRet = True
        try:
            strRet = re.sub(strRex,strReplace,strMessage)

        except Exception as e:
            bRet = False
        return bRet,strRet

    def SubStrSpeci_b_str(self,strMessage):
        bRet=True
        try:
            liststrReplaceChart = ["\(", "\)", "\.","\*","\[","\]"]
            for strReplaceChart in liststrReplaceChart:
                strMessage = re.sub(strReplaceChart, strReplaceChart, strMessage)
        except:
            bRet=False
        return bRet,strMessage


    
    
    





class cTcpSeverForConneter(cBaseThread):
    def __init__(self,dicArgs=None):
        super(cTcpSeverForConneter, self).__init__(dicArgs)
        self.bInitArgs = False

    def StopDo(self):
        del self.obj[self.strConnecterAddress]
    def ThreadDo(self):
        if not self.bInitArgs:
            def Disconnect(objConnecter):
                objConnecter.shutdown(socket.SHUT_RDWR)
                objConnecter.close()

            def Send(objConnecter, strCommand):
                objConnecter.send(strCommand)

            def Recv(objConnecter, nTimeOut=1000, nSizeRecive=1024, strLastWord="\n"):
                strRet = ""
                bRet = True

                nEndTime = self.objTimer.Current() + nTimeOut
                while True:
                    strRet += objConnecter.recv(nSizeRecive)
                    if strRet[-1] == strLastWord:
                        break
                    elif self.objTimer.Current() > nEndTime:
                        bRet = False
                        strRet = "Recv TimeOut {}".format(nTimeOut)
                        break

                return bRet, strRet
            def Clear(objConnecter):
                Recv(objConnecter)
            self.Connecter = self.dictArgs["connecter"]
            self.strConnecterAddress = self.dictArgs["address"]
            self.obj = self.dictArgs["obj"]

import binascii

class cUart:
    def __init__(self,dictArgs=None ):
        self.__session = serial.Serial()
        self.dictArgs =  dictArgs

        self.__session.timeout = self.dictArgs['timeout']
        self.__session.baudrate = self.dictArgs['baud_rate']
        self.__session.port = self.dictArgs['port']
        self.__session.stopbits = self.dictArgs['stop_bits']
        self.__session.bytesize = self.dictArgs['byte_size']
        self.__session.parity = self.dictArgs['parity']
        self.__session.xonxoff = 0

    def sendMsg(self, strCommand):
        if self.status:
            try:
                self.__session.write(strCommand)
                time.sleep(0.3)
            except Exception as e:
                raise e

    def recvMsg(self):
        bRet = True
        strRet = ""
        if self.__session.isOpen() and self.__session.inWaiting():
            try:
                strRet = self.__session.read(self.__session.inWaiting())
            except:
                strRet ="Exceptn Error"
                bRet = False
        self.status = bRet
        return bRet,strRet

    def send_recv(self, command):
        result = None
        if self.status:
            self.sendMsg(command)
            time.sleep(0.05)
            # result = self.__session.readlines(2)
            while True:
                if self.__session.inWaiting():
                    result = self.recvMsg()
                    break
                time.sleep(0.05)
        return result

class cTcpSever(object):
    def __init__(self,strIp,nPort,nTimeOut =0.2,nMaxClientSize=10):
        self.objTimer = cBruceTime()
        self.nMaxClientSize = 10
        self.strIp = strIp
        self.nPort = nPort
        self.nTimeOut = 0.2
        self.bBind = False
        self.__Session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__Session.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.__Session.settimeout(self.timeout)
        self.dictConnectThreads = {}

    def Lisen(self):
        if not self.bBind:
            self.Bind()
        if self.bBind:
            while True:
                if len(self.dictConnectThreads)<self.nMaxClientSize:
                    Connecter,Address = self.__Session.listen(self.nMaxClientSize)
                    self.dictConnectThreads[str(Address)]=cBaseThread({"connecter":Connecter,"address":str(Address),"obj":self})
                    self.dictConnectThreads[str(Address)].start()
        return self.bBind
    def Bind(self):
        strRet = ""
        if not self.bBind:
            try:
                nConnectInfo = self.__Session.bind((self.strIp,self.nPort))
                if nConnectInfo==0:
                    self.bBind = True
            except:
                strRet = "Bind Fail {} {}".format(self.strIp,self.nPort)
        return self.bBind,strRet

class cTcpClient(object):
    def __init__(self,strIp,nPort,nTimeOut =0.2):
        self.objTimer = cBruceTime()
        self.strIp = strIp
        self.nPort = nPort
        self.nTimeOut = 0.2
        self.bConnect = False
        self.__Session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__Session.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.__Session.settimeout(self.timeout)
    def Connect(self):
        if not self.bConnect:
            nConnectInfo = self.__Session.connect_ex((self.strIp,self.nPort))
            if nConnectInfo==0:
                self.bConnect = True
        return self.bConnect
    def Disconnect(self):
        if self.bConnect:
            self.__Session.shutdown(socket.SHUT_RDWR)
            self.__Session.close()
            self.bConnect = False

    def Send(self,strCommand):
        bRet = True
        if not self.bConnect:
            self.Connect()
        if self.bConnect:
            if self._session.send(strCommand) <0:
                bRet = False
        return (bRet and self.bConnect)


    def Clear(self):
        self.Recv()
    def Recv(self,nTimeOut=1000,nSizeRecive=1024,strLastWord="\n"):
        strRet = ""
        bRet = True
        if self.bConnect:
            nEndTime = self.objTimer.Current() + nTimeOut
            while True:
                strRet+=self._session.recv(nSizeRecive)
                if strRet[-1]==strLastWord:
                    break
                elif self.objTimer.Current()>nEndTime:
                    bRet = False
                    strRet = "Recv TimeOut {}".format(nTimeOut)
                    break
        else:
            bRet = False
            strRet ="Didn't Connected !!"
        return bRet,strRet




class cPublisher:
    objContext =  zmq.Context()
    def __init__(self,strUrl,strName,strSubscribe):
        self.objSocket = self.objContext.socket(zmq.PUB)
        self.objSocket.setsockopt(zmq.IDENTITY, strName)
        self.strFlags = strSubscribe
    def start(self,strUrl = None):
        if strUrl:
            self.strUrl = strUrl
        self.bBind = True if self.objSocket.bind(self.strUrl) == 0 else False
        return self.bBind

    def publish(self,listMsg):
        if self.bBind and type(listMsg)==type([]):
            listMsg.insert(0,self.strFlags)
            self.objSocket.send_multipart(listMsg)
    def stop(self):
        if self.bBind and self.objSocket:
            self.publisher.setsockopt(zmq.LINGER, 0)
            self.publisher.close()



class cReplier:
    objContext = zmq.Context()

    def __init__(self, strUrl):
        self.objSocket = self.objContext.socket(zmq.REP)
        self.strUrl = strUrl
        self.bConnect = False

    def start(self, strUrl=None):
        if strUrl:
            self.strUrl = strUrl
        self.bConnect = True if self.objSocket.connect(self.strUrl) == 0 else False
        return self.bConnect

    def send(self, strMsg):
        if self.bConnect:
            self.objSocket.send_string(strMsg)

    def recv(self):
        strRet = ""
        bRet = True
        if self.bConnect:
            strRet = self.objSocket.recv_string()
        return bRet,strRet


class cRequester:
    objContext = zmq.Context()
    def __init__(self,strUrl):
        self.objSocket = self.objContext.socket(zmq.REQ)
        self.strUrl =  strUrl
        self.bConnect = False
    def start(self,strUrl=None):
        if strUrl:
            self.strUrl = strUrl
        self.bConnect = True if self.objSocket.connect(self.strUrl) == 0 else False
        return self.bConnect
    def send(self,strMsg):
        if self.bConnect:
            self.objSocket.send_string(strMsg)
    def recv(self):
        if self.bConnect:
            self.objSocket.recv_string()
class cSubscriber:
    def __init__(self):
        pass


import os

def FileOpen(Filepath,mode):
    strRet = ""
    nRet = 0
    fhFile = None
    try:
        fhFile = open(Filepath,mode)
    except Exception as e:
        strRet = str(e)
        nRet = -1
    return strRet,nRet,fhFile

def FileRead(fh):
    strRet = ""
    nRet = 0
    strFile = ""
    try:
        strFile = fh.read()
    except Exception as e:
        strRet = str(e)
        nRet = -1
    return strRet,nRet,strFile

def FileWrite(fh,strInput):
    strRet = ""
    nRet = 0
    try:
        fh.write(strInput)  
    except Exception as e:
        strRet = str(e)
        nRet = -1
    return strRet,nRet

def FileDelete(strFileName):
    strRet = ""
    nRet = 0
    try:
        os.remove(strFileName)
    except Exception as e:
        strRet = str(e)
        nRet = -1
    return strRet,nRet

def FileClose(fh):
    strRet = ""
    nRet = 0
    try:
        fh.close()
    except Exception as e:
        strRet = str(e)
        nRet = -1
    return strRet,nRet

def CheckArmFolderExist(Filepath):
    strRet = ""
    nRet = 0
    try:
        folder = os.path.exists(Filepath)
        if not folder:
            os.makedirs(Filepath)
            print "{} folder is created".format(Filepath)
        else:
            print "{} folder already exist".format(Filepath)
    except Exception as e:
        strRet = str(e)
        nRet = -1
    return strRet,nRet


class cAutoFoxArm:
    #def __init__():
    #   pass
    def __init__(self,strFolder,strResultFile,strCMDFile,strStatusFile,nSlotSize):
        self.strFolder = strFolder
        self.strResultFile = strResultFile
        self.strCMDFile = strCMDFile
        self.strStatusFile =  strStatusFile
        self.m_objShell = cShell()

        self.nSlotSize= nSlotSize
        CheckArmFolderExist(self.strFolder)
    def CheckCMDFileExist(self):
        nRet = -1
        try:
            bRet,strRet = self.m_objShell.RunShell_b_str("ls",self.strFolder)
            print "************ Check:{} Find:{}".format(strRet,self.strCMDFile)
            if self.strCMDFile in strRet:
                nRet = 0
            else:
                nRet = -1
        except:
            nRet = -1
        return nRet

    def ResultFile(self,listSN,listResult,RWmode="w"):
        Return = FileOpen(self.strFolder+"/"+self.strResultFile,RWmode)
        result = ''
        if Return[1]==0:
            for i in range(0,self.nSlotSize):
                if "READY" in listSN[i]:
                    listSN[i] = '00000000000000000'
                    listResult[i] = 'SKIP'
                result += "{}:{}:{}\n".format(i+1,listSN[i],listResult[i])
            FileWrite(Return[2],result)
            FileClose(Return[2])
        

    def StatusFile(self,FixStatus,RWmode="w"):
        Return = FileOpen(self.strFolder+"/"+self.strStatusFile,RWmode)
        if Return[1]==0:
            FileWrite(Return[2],FixStatus)
            FileClose(Return[2])

    def CMDFile(self,RWmode="r"):
        Return = FileOpen(self.strFolder+"/"+self.strCMDFile,RWmode)
        if Return[1]==0:
            strFileValue = FileRead(Return[2])
            strCMD = strFileValue[2]
            FileClose(Return[2])
        if Return[1]==-1:
            strCMD = Return[0]
        return strCMD
    
    def deleteCMDFile(self):
        FileDelete(self.strFolder+"/"+self.strCMDFile)



if __name__ == "__main__":
    pass#objRe.PraseForFile("../MessageFormat/Version.txt","{{revision}}","program Diag (branch)\nbuild_engine build build_version(diags_version) . Revision revision.\n\tBuilt at build_date_time")