import zmq
from Common.tinyrpc.transports.zmq import ZmqClientTransport
from Common import zmqports
from LogBase import *
from Common.BBase import *

class LogClientNet(object):
    objProctocal = cProtocal("")
    objThreadLock = cBaseThreadLock()
    def __init__(self,strFormat="%(asctime)s %(message)s"):
        ctx = zmq.Context()
        self.sub = ctx.socket(zmq.SUB)
        self.sub.connect("tcp://127.0.0.1:" + str(zmqports.PRM_LOG_PORT))
        self.sub.setsockopt(zmq.SUBSCRIBE, "")
        self.req = ZmqClientTransport.create(ctx, "tcp://127.0.0.1:" + str(zmqports.PRM_LOG_PORT))
    def GetCurrentFolderPath(self):
        return self.SendReply(self.objProctocal.CreateMessage("currentpath","",""))
    def GetOnlineProjectName(self):
        return self.SendReply(self.objProctocal.CreateMessage("onlineproject","",""))

    def GetOnlineFolderPath(self):
        return self.SendReply(self.objProctocal.CreateMessage("onlinepath","",""))

    def Trace(self,strLogName,strInfo,strLogFormat="%(asctime)s %(message)s"):
        return self.SendReply(self.objProctocal.CreateMessage("prmlog",strLogName,strInfo,strFormat=strLogFormat))
    def StartTest(self,strLogName):
        return self.SendReply(self.objProctocal.CreateMessage("starttest",strLogName,""))
    def StopTest(self,strLogName):
        return self.SendReply(self.objProctocal.CreateMessage("stoptest",strLogName,""))

    def SendReply(self,strMessage):
        strRet = ""
        try:
            self.objThreadLock.Lock(True)
            strRet =self.req.send_reply(strMessage)
            self.objThreadLock.Lock(False)
        except Exception as e:
            strRet = "SendReply Exception {}".format(e)
        return strRet



class LogClient:
    objLogClient = LogClientNet()
    def __init__(self, strBaseInfo, strLogFileName, strFormat="%(asctime)s %(message)s"):
        self.strLogName = "{}_{}".format(strBaseInfo, strLogFileName)
        self.strLogFormat = strFormat
    def GetCurrentFolderPath(self):
        return self.objLogClient.GetCurrentFolderPath()
    def GetOnlineProjectName(self):
        return self.objLogClient.GetOnlineProjectName()
    def GetOnlineFolderPath(self):
        return self.objLogClient.GetOnlineFolderPath()
    def Trace(self, strInfo):
        return self.objLogClient.Trace(self.strLogName,strInfo,strLogFormat=self.strLogFormat)

    def StartTest(self):
        return self.objLogClient.StartTest(self.strLogName)
    def StopTest(self):
        return self.objLogClient.StopTest(self.strLogName)

if __name__ == '__main__':
    log1 = LogClient("dut1", "Test1.csv",strFormat="%(message)s")
    log2 = LogClient(2, "Test2.txt")
    log3 = LogClient(3, "Test")
    log4 = LogClient(4, "Test4")
    log5 = LogClient(5, "Test5")









