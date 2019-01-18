class cProtocal:
    def __init__(self,strMsg):
        self.bStatu,self.dictMsg = self.PraseMessage(strMsg)

    def CreateMessage(self,strCmd,strGrounp,strItem,strFormat=None):
        return str({"cmd":strCmd,"grounp":strGrounp,"item":strItem})
    def PraseMessage(self,strMsg):
        bRet =True
        dictMsg = {}
        try:
            dictMsg = eval(strMsg)
        except Exception as e:
            strRet="Exception {}".format(strMsg)
        return bRet,dictMsg
    def GetCmd(self):
        xRet = None
        if self.bStatu:
            xRet = self.dictMsg.get("cmd")
        return xRet

    def GetLockGrounp(self):
        xRet = None
        if self.bStatu:
            xRet = self.dictMsg.get("grounp")
        return xRet
    def GetLockItem(self):
        xRet = None
        if self.bStatu:
            xRet = self.dictMsg.get("item")
        return xRet


