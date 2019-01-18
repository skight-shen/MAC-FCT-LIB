import time
import zmq
import sys
import os
import sched

sys.path.append(os.getcwd())
sys.path.append("./Core")

if not __package__:
    path = os.path.join(os.path.dirname(__file__), os.pardir)
    sys.path.insert(0, path)
import CoreAPI

from threading import Thread
from Common.tinyrpc.transports.zmq import ZmqServerTransport
from Common.publisher import ZmqPublisher
from Common import zmqports

from Common.BBase import *
from Log.LogBase import *



class cLogsManager(object):
    objbaseHand= logging.basicConfig(level=logging.INFO)
    objTimer= cBruceTime()
    objFolder = cBaseFolder()
    def __init__(self,strLogName,strConfigPath="./Config/logset.json",strFormat= "%(asctime)s %(message)s",strDataformat="[%Y-%m-%d-%H:%M:%S]"):
        self.objLock           = cBaseThreadLock()
        self.objOfflineConfig  = cBruceConfig(strConfigPath)
        self.objOnlineConfig   = cBruceConfig(self.objOfflineConfig.GetConfig("OnlineConfig"))
        self.strLogName        = strLogName
        self.objLog            = logging.getLogger(strLogName)
        self.strRootPath       = self.objOfflineConfig.GetConfig("RootBasePath")
        self.nChangrFodlerTime = self.objOfflineConfig.GetConfig("ChangeFodlerTime")
        self.nCleanFrequence     = self.objOfflineConfig.GetConfig("CleanFrequence")
        self.nZipKeepTime      = self.objOfflineConfig.GetConfig("ZipKeep")
        self.bStreamHandler    = self.objOfflineConfig.GetConfig("StreamHandler")
        self.bFileHandler      = self.objOfflineConfig.GetConfig("FileHandler")
        self.SeverLogFolder    = "SeverLogFolder"
        self.OpenSWFolder      = ""
        self.StartTestFolder   = "Ready"
        self.strFormat         = strFormat
        self.dictClientLogs    = {}
        self.InitSeverLog()
        self.OnMessage(ChangeType.CLEAN)
        self.OnMessage(ChangeType.OPENSOFTWARE)

        self.StartZipLastOpenLog()


    def ReSetAllClientLog(self):
        self.objLock.Lock(True)
        for log in  self.dictClientLogs.values():
            for handler in log.handlers:
                handler.close()
                log.removeHandler(handler)
        self.dictClientLogs={}
        self.objLock.Lock(False)
        self.SeverTrace("Sever ReSetAllClientLog")
    def InitSeverLog(self):
        if self.bStreamHandler:
            self.AddStreamHandler(self.objLog)
        if self.bFileHandler:
            self.AddSeverFileHandler(self.objLog,self.strLogName)
        self.dictClientLogs = {}
        self.SeverTrace("Sever InitSeverLog")

    def CreateSeverFileHandler(self, strLogName):
        strNewPath= "{}/{}".format(self.strRootPath, self.SeverLogFolder)
        self.objFolder.CreateFodler(strNewPath)
        hfLog = logging.FileHandler("{}/{}".format(strNewPath,strLogName))
        hfLog.setLevel(logging.INFO)
        hfLog.setFormatter(logging.Formatter(self.strFormat))
        return hfLog
    def GetCurrentFolder(self):
        return "{}/{}/{}".format(self.strRootPath,self.OpenSWFolder,self.StartTestFolder)
    def GetOnlineFolder(self):
        strOnlinePath = self.objOnlineConfig.GetConfig("defaults").get("log_file_path")
        self.SeverTrace("Sever GetOnlineFolder {}".format(strOnlinePath))
        return strOnlinePath
    def GetOnlineProjectName(self):
        strOnlineProjectName = self.objOnlineConfig.GetConfig("project")
        self.SeverTrace("Sever GetOnlineProjectName {}".format(strOnlineProjectName))
        return strOnlineProjectName

    def CreateClientFileHandler(self,strLogName,strFormat=None):
        strNewPath = "{}/{}/{}".format(self.strRootPath,self.OpenSWFolder,self.StartTestFolder)
        self.objFolder.CreateFodler(strNewPath)
        hfLog = logging.FileHandler("{}/{}".format(strNewPath,strLogName))
        hfLog.setLevel(logging.INFO)
        if strFormat:
            hfLog.setFormatter(logging.Formatter(strFormat))
        else:
            hfLog.setFormatter(logging.Formatter(self.strFormat))
        return hfLog
    def AddSeverFileHandler(self,objLog,strLogName):
        objLog.addHandler(self.CreateSeverFileHandler(strLogName))
    def AddClientFileHandler(self,objLog,strLogName,strFormat=None):
        objLog.addHandler(self.CreateClientFileHandler(strLogName,strFormat=strFormat))
    def AddStreamHandler(self,objLog):
        hcLog = logging.StreamHandler()
        hcLog.setLevel(logging.INFO)
        hcLog.setFormatter(logging.Formatter(self.strFormat))
        objLog.addHandler(hcLog)

    def StartCleanLog(self):
        objScheduler = threading.Timer(self.nCleanFrequence,self.OnMessage, (ChangeType.CLEAN,))
        objScheduler.start()
        self.SeverTrace("Sever StartFolderCheanSche")
    def StartZipLastOpenLog(self):
        objScheduler = threading.Timer(0,self.OnMessage, (ChangeType.CLEANLASTOPEN,))
        objScheduler.start()
        self.SeverTrace("Sever StartFolderCheanSche")

    def CleanLog(self):
        self.SeverTrace("Sever Clean Zip Start")
        try:
            CoreAPI.CleanFolderFiles(self.strRootPath,"zip",self.nZipKeepTime)
            CoreAPI.CleanFolderFiles("{}/Log".format(self.GetOnlineFolder()), "zip", self.nZipKeepTime)
        except:
            pass
        self.SeverTrace("Sever Clean Zip End")


    def StartZipLog(self,strFolderPath):
        objScheduler = threading.Timer(2, self.ZipLog, (strFolderPath,))
        objScheduler.start()
    def ZipLog(self,strFolderPath):
        self.SeverTrace("Sever  Zip Start")
        try:
            CoreAPI.ZipFolder(strFolderPath)
            CoreAPI.ZipFolder("{}/Ready".format(CoreAPI.GetFolderRoot(self.GetCurrentFolder())))
        except:
            pass
        self.SeverTrace("Sever  Zip End")
    def ZipLastOpenLog(self):
        listExclude = []
        try:
            listExclude.append(CoreAPI.GetFolderRoot(self.GetCurrentFolder()))
            CoreAPI.ZipFolders(self.strRootPath,listExclude=listExclude)
        except:
            pass


    def OnMessage(self,enumType):
        if enumType==ChangeType.CLEAN:
            self.CleanLog()
            self.StartCleanLog()
        else:
            if enumType == ChangeType.STARTTEST:
                self.StartTestFolder = "StartTest_{}".format(self.objTimer.CurrentStr())
                self.ReSetAllClientLog()
            if enumType == ChangeType.STOPTEST:
                self.StartZipLog(self.GetCurrentFolder())
            elif enumType == ChangeType.CLEANLASTOPEN:
                self.ZipLastOpenLog()
            elif enumType == ChangeType.OPENSOFTWARE:
                self.OpenSWFolder = "OpenTester_{}".format(self.objTimer.CurrentStr())
                self.ReSetAllClientLog()
        self.SeverTrace("Sever OnMessage {}".format(enumType))


    def SeverTrace(self,strInfo):
        self.objLog.info(strInfo)

    def ClientTrace(self,strLogName,strInfo,strFormat=None):
        self.objLock.Lock(True)
        if strLogName not in self.dictClientLogs.keys():
            self.dictClientLogs[strLogName]=logging.getLogger(strLogName)
            self.AddClientFileHandler(self.dictClientLogs[strLogName],strLogName,strFormat=strFormat)
        self.dictClientLogs[strLogName].info(strInfo)
        self.objLock.Lock(False)






class LogServer(Thread):
    def __init__(self,strConfigPath="../Config/logset.json"):
        super(LogServer, self).__init__()
        ctx = zmq.Context()

        listen_addr = "tcp://*:" + str(zmqports.PRM_LOG_PORT)
        pub_addr    = "tcp://*:" + str(zmqports.PRM_LOG_PUB)

        self.frontend = ctx.socket(zmq.ROUTER)
        self.frontend.bind(listen_addr)

        self.publisher = ZmqPublisher(ctx, pub_addr, "PRMLOG")
        self.transport = ZmqServerTransport(self.frontend)

        self.transport.publisher = self.publisher
        self.ThreadLock = cBaseThreadLock()

        self.objLog  = cLogsManager("PrmLogSever.log",strConfigPath=strConfigPath)
        self.serving = True
    def StopSever(self):
        self.serving = False
    def run(self):
        self.objLog.SeverTrace("Start Prm Log Sever Success!!")
        while self.serving:
            context, message = self.transport.receive_message()
            if message:
                objProtocal = cProtocal(message)
                strCmd= objProtocal.GetCmd()
                strInfo = objProtocal.GetInfo()
                strLogName = objProtocal.GetLogName()
                strLogFormat = objProtocal.GetLogFormat()
                if strCmd and strInfo and strLogName and  strCmd=="prmlog" :
                    self.objLog.ClientTrace(strLogName,strInfo,strFormat=strLogFormat)
                    self.transport.send_reply(context, str("log ok"))
                elif strCmd  and  strCmd=="starttest":
                    self.objLog.OnMessage(ChangeType.STARTTEST)
                    self.transport.send_reply(context, str("start ok"))
                elif strCmd  and  strCmd=="stoptest":
                    self.objLog.OnMessage(ChangeType.STOPTEST)
                    self.transport.send_reply(context, str("stop ok"))
                elif strCmd  and  strCmd=="currentpath":
                    strRet = self.objLog.GetCurrentFolder()
                    self.transport.send_reply(context, strRet)
                elif strCmd  and  strCmd=="onlinepath":
                    strRet = self.objLog.GetOnlineFolder()
                    self.transport.send_reply(context,str(strRet))
                elif strCmd  and  strCmd=="onlineproject":
                    strRet = self.objLog.GetOnlineProjectName()
                    self.transport.send_reply(context,str(strRet))
                    
                else:
                    self.objLog.SeverTrace("Sever Get Message Error : {}".format(message))
                del objProtocal

        print("LogServer Stoped")
        self.transport.shutdown()

if __name__=="__main__":

    objlogSeverThread = LogServer(strConfigPath="./Config/logset.json")
    objlogSeverThread.start()

