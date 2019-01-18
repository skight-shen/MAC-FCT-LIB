class ChangeType:
    STARTTEST     = 0
    STOPTEST      = 1
    OPENSOFTWARE  = 2
    PERHOUR       = 3
    CLEAN         = 4
    CLEANLASTOPEN = 5

class cProtocal:
    def __init__(self,strMsg):
        self.bStatu,self.dictMsg = self.PraseMessage(strMsg)

    def CreateMessage(self,strCmd,strLogName,strInfo,strFormat=None):
        return str({"cmd":strCmd,"info":strInfo,"logname":strLogName,"format":strFormat})
    def PraseMessage(self,strMsg):
        bRet =True
        dictMsg = {}
        try:
            dictMsg = eval(strMsg)
        except Exception as e:
            strRet="Exception {}".format(strMsg)
        return bRet,dictMsg
    def GetInfo(self):
        xRet=None
        if self.bStatu:
            xRet= self.dictMsg.get("info")
        return xRet

    def GetCmd(self):
        xRet = None
        if self.bStatu:
            xRet = self.dictMsg.get("cmd")
        return xRet
    def GetLogName(self):
        xRet = None
        if self.bStatu:
            xRet = self.dictMsg.get("logname")
        return xRet
    def GetLogFormat(self):
        xRet = None
        if self.bStatu:
            xRet = self.dictMsg.get("format")
        return xRet


