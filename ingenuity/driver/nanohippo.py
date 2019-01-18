from ingenuity.loggers import ZmqPublisher
from ingenuity import zmqports
import zmq

import time,os, sys
from ingenuity.driver.dataDriver import SerialDriver

class Nanohippo(SerialDriver):
    def __init__(self, cfg, site):
        super(Nanohippo, self).__init__(cfg, site)

    def DutReadString(self):
        strRet =''
        strRet = self.recvMsg()
        return strRet

    def DutSendString(self, strData):
        strData += '\n'
        self.sendMsg(strData)

    def DutSendCmd(self, strData, nTimeout):
        self.DutSendString(strData)
        nRet, strRet = self.DutWaitForString(nTimeout)
        return nRet, strRet

    def DutWaitForString(self, nTimeout):
        nRet = self.WaitDetect(nTimeout)
        if nRet == -1:
            strRet = "No such a key word"
        elif nRet == -2:
            strRet = "Timeout"
        elif nRet != 0:
            strRet = "Unknow Error occur EFI_MODULEWait_For_String_"
        elif nRet == 0:
            strRet = "Find key word: %s"%self.detection

        return nRet, strRet

    def DutSetDetectString(self, strData):
        self.detection = strData

    def WriteCB(self,nSd, strCmd):
        pass

    def reset(self):
        self.close()
        time.sleep(1)
        self.connect()