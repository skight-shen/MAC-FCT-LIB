#from Common.BBase import *
#from Log.LogClient import LogClient
from ingenuity import zmqports

from libDylib import *

#from libDylib import LibNanohippo, LibSocketDev
import time, os
from ingenuity.testEngine.functions.potassium import *




class cSocketDev(object):
    """docstring for ClassName"""
 #   m_objBTime = cBruceTime()

    def __init__(self, nSlotId):
        super(cSocketDev, self).__init__()
        self.nSlotId = nSlotId

        self.bConnectFlag = False

        # Add strPubUrl/strRepUrl Auto Get


        self.objSocketDev = LibSocketDev()

        strRepUrl = "tcp://127.0.0.1:" + str(int(zmqports.UART2_PORT) + self.nSlotId)
        strPubUrl = "tcp://127.0.0.1:" + str(int(zmqports.UART2_PUB) + self.nSlotId)

        self.objSocketDev.CreateIPC(strRepUrl, strPubUrl)
        self.strZynqAddr = "169.254.1.{}".format(32 + self.nSlotId)
        self.strPchport = 7603

        self.Connect_b()
      #  self.m_objBLog = LogClient(self.nSlotId, "pch_log_prm_efi.log")  # cBruceLogs("/vault/pch_log_prm_efi.log")

    def Connect_b(self):
        if self.bConnectFlag:
            self.objSocketDev.Close()
            self.bConnectFlag = False

        # print("< ".. tostring(CONFIG.ID).." NanoHippo PORT : "..potassium_id .."> ")
        if self.objSocketDev.Open(self.strZynqAddr, self.strPchport) < 0:
            self.objSocketDev.Close()
            self.bConnectFlag = False

        else:
            self.bConnectFlag = True
        return self.bConnectFlag

    def Clr_spam_buff(self):
        pass

    def DutSendCmd_n_str(self, strCmd, nTimeout):
        nRet = -1
        strRet = ""
        # self.m_objBTime.Delay(500)
        if self.bConnectFlag:
            # t1 = self.m_objBTime.Current()
            for i in strCmd:
                self.objSocketDev.WriteString(i, 1)
                self.m_objBTime.Delay(50)
            self.objSocketDev.WriteString("\r\n", 1)
            self.m_objBTime.Delay(20)
            nRet = self.objSocketDev.WaitDetect(nTimeout)
        else:
            print "Socket Dut Didn't Connected !! "
        return nRet, strRet

    def DutSendString_n(self, strData):
        # t1 = self.m_objBTime.Current()
        nRet = -1
        strRet = ""
        # self.m_objBTime.Delay(500)
        if self.bConnectFlag:
            for i in strData:
                self.objSocketDev.WriteString(i, 1)
                self.m_objBTime.Delay(50)
            self.objSocketDev.WriteString("\r\n", 1)
            self.m_objBTime.Delay(20)
        # print "Efi send:-->> {}".format(strData)
        # self.m_objBLog.Trace(strRet)

        else:
            print "Socket Dut Didn't Connected !! "
        return 0

    def DutReadString_str(self):
        strRet = ""
        if self.bConnectFlag:
            strRet = self.objSocketDev.ReadString()
            if strRet != "":
                # print "Efi read:-->> {}".format(strRet)
                self.m_objBLog.Trace(strRet)
        else:
            print "Socket Dut Didn't Connected !!DutReadString_str "
        return strRet

    def DutReadString2_str(self):
        strRet = ""
        if self.bConnectFlag:
            self.m_objBTime.Delay(50)
            strRet = self.objSocketDev.ReadString()
            if strRet != "":
                print "Efi Read:-->> {}".format(strRet)
                self.m_objBLog.Trace(strRet)


        else:
            print "Socket Dut Didn't Connected !!DutReadString_str "
        return strRet

    def DutSetDetectString(self, strData):
        if self.bConnectFlag:
            self.objSocketDev.SetDetectString(strData)
        else:
            print  "Socket Dut Didn't Connected !!DutSetDetectString "

    def DutWaitForString_n(self, nTimeout):
        nRet = -1

        if self.bConnectFlag:
            nRet = self.objSocketDev.WaitDetect(nTimeout)
        else:
            print  "Socket Dut Didn't Connected !!DutWaitForString_n_str "
        return nRet

    def Close(self):
        if self.bConnectFlag:
            self.objSocketDev.Close()
        else:
            print  "Socket Dut Didn't Connected !!Close "


class cNanoHippoPy:
    """docstring for ClassName"""
    nPubPort = 31337

    def __init__(self, nSlotId, objLock, strPotassiumUrl):

        self.nSlotId = nSlotId

        self.g_Lock = objLock

        self.PotassiumUrl = strPotassiumUrl
        self.bConnectFlag = False

        strRepUrl = "tcp://127.0.0.1:" + str(int(zmqports.UART_PORT) + self.nSlotId)
        strPubUrl = "tcp://127.0.0.1:" + str(int(zmqports.UART_PUB) + self.nSlotId)
        # Add strPubUrl/strRepUrl Auto Get

        self.objNanoHippoDev = LibNanohippo()

        self.objNanoHippoDev.CreatePub(strPubUrl, 31337)  # self.nPubPort)
        self.objNanoHippoDev.CreateRep(strRepUrl)

        self.objNanoHippoDev.SetFilterColorCode(1)
        self.objNanoHippoDev.SetFilterUnreadable(1)

        #self.m_objBLog = LogClient(self.nSlotId, "dut.log")

        self.PotassiumIdFinder = PotassiumIdFinder()
        self.PotassiumUrl = self.PotassiumIdFinder.GetPotassiumUrl(self.nSlotId)

        print "{0} Auto Potassium Id :{1}".format(self.nSlotId, self.PotassiumUrl)

    def Connect_b(self):
        strPotassiumId = self.PotassiumUrl

        print "Potassium Open {0} Start".format(strPotassiumId)
        nRet = self.objNanoHippoDev.openSerial(strPotassiumId)
        time.sleep(1)
        print "Potassium Open {0} End, {1}".format(strPotassiumId, nRet)
        if nRet < 0:
            print "Potassium Open Error {0}".format(strPotassiumId)
            self.bConnectFlag = False
        else:
            self.bConnectFlag = True

        return nRet

    def SetLogPaths(self, listNPort, listStrPath):
        if len(listNPort) != len(listStrPath):
            print "SetLog File Len different !!!! {} VS {}".format(str(listNPort), str(listStrPath))
        else:
            for i in range(0, len(listNPort)):
                nRet = self.objNanoHippoDev.SetLogFile(listNPort[i], listStrPath[i])
                self.m_objBLog.Trace("Set Log File {}:{} Ret:{}".format(listNPort[i], listStrPath[i], nRet))

    def SetLogfile(self, strDefaultLogAddr):
        self.objNanoHippoDev.SetLogFile(-1, strDefaultLogAddr)

    def SetSmcLogfile(self, nPort, strDefaultLogAddr):
        self.objNanoHippoDev.SetLogFile(nPort, strDefaultLogAddr)

    def DutSendString_n(self, strData, nPort=31337):
        nRet = -1
        if self.bConnectFlag:
            time.sleep(0.1)
            strWriteData = "\n"
            if nPort == None or nPort == "":
                nPort = 31337
            if strData.upper().find("ENTER") < 0:
                strWriteData = "{}\n".format(strData)

            nRet = self.objNanoHippoDev.WriteString(nPort, strWriteData)

        else:
            print "DutSendString_n Potassium Didn't Connect !!"
        return nRet

    def ClearBuffer(self, nPort=31337):
        nRet = -1
        if self.bConnectFlag:
            if nPort == None or nPort == "":
                nPort = 31337

            self.objNanoHippoDev.ClearBuffer(nPort)

        else:
            print "ClearBuffer Potassium Didn't Connect !!"
        return nRet

    def DutSetDetectString(self, strData):
        if isinstance(basestring, strData) and strData != "":
            self.objNanoHippoDev.SetDetectString(strData)

    def DutWaitForString_n_str(self, nTimeout, nPort=31337):
        nRet = -1
        strRet = ""
        if self.bConnectFlag:
            nRet = self.objNanoHippoDev.WaitDetect(nPort, nTimeout)
            if nRet == -1:
                strRet = "connection disconnect"
            elif nRet == -2:
                strRet = "Timeout"
            elif nRet != 0:
                strRet = "Unknow Error occur EFI_MODULEWait_For_String_"
        else:
            print "DutWaitForString_n_str Potassium Didn't Connect !!"
        return nRet, strRet

    def DutSendCmd_n_str(self, strCmd, nTimeout, nPort=31337):
        nRet = -1
        strRet = ""
        if self.bConnectFlag:
            self.DutSendString_n(strCmd, nPort)
            print "dut send cmd {0}".format(strCmd)
            nRet, strRet = self.DutWaitForString_n_str(nTimeout, nPort)
            print "dut waitforstring: {0}".format(strCmd)
        else:
            print "DutSendCmd_n_str Potassium Didn't Connect !!"
        return nRet, strRet

    def DutReadString_str(self, nPort=31337):

        strRet = ""
        if self.bConnectFlag:
            time.sleep(0.03)
            strRet = self.objNanoHippoDev.ReadString(nPort)
            if strRet != "":
                self.ClearBuffer(nPort)
                bRet, strRet = self.m_objBRe.SubStr_b_str(strRet, "\+", "")
        else:
            print "DutReadString_str Potassium Didn't Connect !!"

        print "dut read {0}".format(strRet)
        return strRet

    def WriteCB(self, nSd, strCmd, nPort=31337):
        nRet = -1
        if self.bConnectFlag:
            nRet = self.objNanoHippoDev.WritePassControlBit(nPort, nSd, strCmd)
        else:
            print "WriteCB Potassium Didn't Connect !!"
        return nRet

    def Close(self):
        if self.bConnectFlag:
            nRet = self.objNanoHippoDev.closeAll()
        else:
            print "Close Potassium Didn't Connect !!"

        return nRet

    def CheckAlive_n(self, nCount, strData):
        nRet = -1
        if self.bConnectFlag:
            if len(strData)==0:
                strData = ":-)"

            self.DutSetDetectString(strData)
            for i in range(0, nCount):  # (1) do
                nRet = self.DutSendCmd_n("", 1000)
                if nRet == 0:
                    break
        else:
            print "CheckAlive_n Potassium Didn't Connect !!"
        return nRet

    def LoopTryConnection(self, nCount, nPort=31337):
        strDutRespond = ""

        bRet = True
        if self.bConnectFlag:
            if type(nCount) == int and type(nPort) == int:
                self.DutSetDetectString(":-)")

                nRet = -1
                for i in range(0, nCount):  # (1) do
                    nRet = self.DutSendCmd_n("version", 9000)
                    if nRet != 0:
                        bRet = False
                        break
                    time.sleep(1)
                    strDutRespond = self.objNanoHippoDev.ReadString(nPort)

                    if strDutRespond == None:
                        bRet = False
                        break
                    time.sleep(0.001)
        return bRet


class cCArmDLpy:
    def __init__(self, nUut, dictDataLog, nPubPort):
        self.dictDataLog = dictDataLog
        self.nUut = nUut
        self.strIp = "169.254.1.{}".format(32 + int(self.nUut))
        self.nPort = 7611
        self.libArm = LibArmDl()
        self.strMid = "cCArmDLpy_{}".format(self.nUut)
        self.strHeader = ""

        # self.strLogFileName="{}_log.csv".format(self.strMid)
        self.strUrl = "tcp://*:{}".format(nPubPort + self.nUut)
        self.Init()
        self.Connect()

    def Init(self):
        self.strHeader = ""
        for i in range(0, 4):
            self.strHeader = self.strHeader + "timestamp" + "{}".format(i + 1) + "," + \
                             self.dictDataLog["CH{}".format(i + 1)][4]
            if i < 3:
                self.strHeader = self.strHeader + ","
            else:
                self.strHeader = self.strHeader + "\r\n"

    def Connect(self):
        if self.libArm:
            self.libArm.CreateTCPClient(self.strMid, self.strIp, self.nPort)
            for i in range(0, 4):
                print float(eval(self.dictDataLog["CH{}".format(i + 1)][0])), \
                    float(eval(self.dictDataLog["CH{}".format(i + 1)][1])), \
                    float(eval(self.dictDataLog["CH{}".format(i + 1)][2])), \
                    float(eval(self.dictDataLog["CH{}".format(i + 1)][3]))
                self.libArm.updateConfig(i, float(eval(self.dictDataLog["CH{}".format(i + 1)][0])), \
                                         float(eval(self.dictDataLog["CH{}".format(i + 1)][1])), \
                                         float(eval(self.dictDataLog["CH{}".format(i + 1)][2])), \
                                         float(eval(self.dictDataLog["CH{}".format(i + 1)][3])), 1, 1000)
            self.libArm.CreatZmqPub(self.strUrl)

        else:
            print "Connect libArm Obj Didn't Create"

    def SetLogPath(self, strLogPath):
        if self.libArm:
            self.libArm.setLogPath(self.strHeader, "{}/{}".format(strLogPath, self.strMid))
        else:
            print "SetLogPath libArm Obj Didn't Create"

    def StartDataLog(self, strLogPath):
        self.SetLogPath(strLogPath)
        if self.libArm:
            self.libArm.startDataLogger()
        else:
            print "StartDataLog libArm Obj Didn't Create"

    def StopDataLog(self):
        if self.libArm:
            self.libArm.stopDataLogger()
        else:
            print "StopDataLog libArm Obj Didn't Create"


class cPowerSequence:
    def __init__(self, nUut, dictDataLog, nPubPort):
        self.dictDataLog = dictDataLog
        self.nUut = nUut
        self.strIp = "169.254.1.{}".format(32 + int(self.nUut))
        self.nPort = 7621
        self.libPs = LibPs()
        self.strMid = "cPowerSequence_{}".format(self.nUut)
        self.strHeader = ""

        # self.strLogFileName="{}_log.csv".format(self.strMid)
        self.strUrl = "tcp://*:{}".format(nPubPort + self.nUut)
        self.strChannelConfig = ""
        self.Init()

        self.bStartFlag = False

        self.Connect()

    def Init(self):
        self.strHeader = ""
        for i in range(0, 40):
            channel_temp = "CH{}".format(i + 1)
            self.strChannelConfig = self.strChannelConfig + ";" + self.dictDataLog[channel_temp][0] + "," + str(
                (5.002 * float(eval(self.dictDataLog[channel_temp][1])))) + "," + (
                                        self.dictDataLog[channel_temp][2]) + "," + (self.dictDataLog[channel_temp][3])
        self.strChannelConfig = self.strChannelConfig[1:]

    def Connect(self):
        if self.libPs:
            self.libPs.CreateTCPClient(self.strMid, self.strIp, self.nPort)
            self.libPs.updateConfig(self.strChannelConfig, 1, self.nUut)
            self.libPs.CreatZmqPub(self.strUrl)
        else:
            print "Connect libArm Obj Didn't Create"

    def StartDataLog(self, strLogPath, strType, nFlag=1):
        if self.libPs:
            if self.bStartFlag == False:
                self.libPs.startDataLogger("{}/{}_{}_PS.csv".format(strLogPath, self.strMid, strType), nFlag)
                self.bStartFlag = True
        else:
            print "StartDataLog libArm Obj Didn't Create"

    def StopDataLog(self, nFlag=1):
        if self.libPs:
            if self.bStartFlag == True:
                self.libPs.stopDataLogger(nFlag)
                self.bStartFlag = False
        else:
            print "StopDataLog libArm Obj Didn't Create"
