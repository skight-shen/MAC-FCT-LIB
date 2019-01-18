from ingenuity.tinyrpc.dispatch import public
from ingenuity.driver.LibCallPy import cNanoHippoPy
from ingenuity.testEngine.functions.potassium import *
from ingenuity.driver.dataDriver import *
from ingenuity.driver.nanohippo import Nanohippo
import logging, re

class Dut():
    def __init__(self, slotID, objSDev, cfg):
        #super(Dut, self).__init__(cfg)
        self.nanohippo = Nanohippo(cfg, slotID)
        #self.potassium = Potassium(nanohippo=self.nanohippo)
        self.slotID = slotID
        self.pch_uart = objSDev
        self.nanohippo.connect()
        self._last_diags_response = ''
        self._last_diags_command = ''
        self.fDutRtc = -9999

    @public
    def enteriboot(self, *args, **kwargs):
        nTimeout = kwargs['timeout']
        endTime = startTime = time.time()
        isRecoveryMode = False
        try:
            while endTime - startTime <= nTimeout:
                self.nanohippo.DutSendString('\r\n')
                strRet = self.nanohippo.DutReadString()
                if "SYNTAX" in strRet:
                    isRecoveryMode = True
                    break
                elif ']' in strRet:
                    self.nanohippo.DutSendString('checkbootstatus')
                    time.sleep(0.5)
                elif 'root#' in strRet:
                    self.nanohippo.DutSendString('reboot')
                    time.sleep(6)
                    self.nanohippo.DutSendString('\r\n')
                    time.sleep(3)
                    self.nanohippo.DutSendString('\r\n')
                    time.sleep(1.5)
                    self.nanohippo.DutSendString('\r\n')
                elif 'Password' in strRet:
                    self.nanohippo.DutSendString('alpine')
                    time.sleep(0.1)
                elif 'login' in strRet:
                    self.nanohippo.DutSendString('root')
                    time.sleep(0.1)
                    
                endTime = time.time()
            return '--PASS--' if isRecoveryMode else '--FAIL--'
        except Exception as e:
            return "--FAIL--, Exception: %s" %e.message

    #send diags cmd and detect sequence.paramter2
    @public
    def diags(self, *args, **kwargs):
        diags_timeout = 2500

        diags_cmd = args[0]
        if len(diags_cmd) == 0:
            return "ERRORCODE[-6] Diags command shall not be empty!"

        if len(args) > 1:
            diags_det = args[1]
        else:
            diags_det = ":-)"
        self.nanohippo.DutSetDetectString(diags_det)

        if diags_cmd.find('usbfs -e') != -1:
            diags_cmd = 'usbfs -e -n ' + str(self.slotID+1)
        elif diags_cmd.find('usbfs -d') != -1:
            diags_cmd = 'usbfs -d -n ' + str(self.slotID+1)
        elif diags_cmd.find('--mount') != -1:
            diags_cmd = 'usbfs -m -n ' + str(self.slotID + 1)

        self._last_diags_command = diags_cmd
        self.nanohippo.DutReadString()

        logging.info("send diags command: {0}".format(diags_cmd))
        ret, errmsg = self.nanohippo.DutSendCmd(diags_cmd, diags_timeout)
        if(ret != 0):
            logging.info("no response >> Reset potassium!!!")
            self._last_diags_response = self.nanohippo.DutReadString()
            self.nanohippo.reset()
            ret, errmsg = self.nanohippo.DutSendCmd(diags_cmd, diags_timeout)
            if(ret != 0):
                logging.info("ERROR:%s"%errmsg)
                self.nanohippo.DutSendString("consolerouter -t")
                time.sleep(10)
                self.nanohippo.DutReadString("smc dump")
                time.sleep(5)
        self._last_diags_response = self.nanohippo.DutReadString()


        if not ret:
            return "--PASS--"
        else:
            return "--FAIL--, ERROR: %s"%errmsg

    @public
    def getsnfromiboot(self,*args,**kwargs):
        serialNumber = ''
        try:
            strParam1 = args[0]
            self.nanohippo.DutSendString(strParam1)
            time.sleep(1)
            strRet = self.nanohippo.DutReadString()


        except Exception as e:
            return "--FAIL--, EXCEPTION: %s"% e.message
        return serialNumber
    #send diags cmd only and no detection
    @public
    def iefisend(self, *args, **kwargs):
        diags_cmd = args[0]
        if len(diags_cmd) == 0:
            return "ERRORCODE[-6] Diags command shall not be empty!"

        self.nanohippo.DutReadString()
        logging.info("send diags command: {0}".format(diags_cmd))
        ret = self.nanohippo.DutSendString(diags_cmd)

        if not ret:
            return "--PASS--"
        else:
            return "--FAIL--"

    #send efi cmd and detect sequence.paramater2
    @public
    def efidiags(self, *args, **kwargs):
        timeOut = kwargs['timeout']

        if len(args) == 0:
            return "ERRORCODE[-6] EFI command shall not be empty!"

        if len(args[0]) != 0:
            strCmd = args[0]

        if len(args[1]) != 0:
            strDetection = args[1]
        else:
            strDetection = '\\>'

        try:
            self.pch_uart.DutSetDetectString(strDetection)
            self.pch_uart.DutReadString_str()

            ret, msg = self.pch_uart.DutSendCmd_n_str(strCmd, timeOut)
            retString = self.pch_uart.DutReadString_str()
        except Exception as e:
            ret = -1
            erromsg = e.message

        if not ret:
            return "--PASS--"
        else:
            return "--FAIL--"+erromsg

    #send efi cmd and no detection
    @public
    def efisend(self, *args, **kwargs):
        return

    def connect(self, *args, **kwargs):
        status = self.nanohippo.connect()
        return status

    def disconnect(self,*args, **kwargs):
        return self.nanohippo.close()

    @public
    def parse(self, *args, **kwargs):
        return "--PASS--"

    @public
    def rtc(self, *args, **kwargs):
        str_cmd = args[0]
        nTimeout = kwargs['timeout']
        try:
            if 'get' in str_cmd:
                nRet, strRet = self.nanohippo.DutSendCmd('rtc --get')
                if not nRet:
                    sreRet = self.nanohippo.DutReadString()
                    strRex = "RTC_Time: (\d+?)\.(\d+?)\.(\d+?)\.(\d+?)\.(\d+?)\.(\d+?)"
                    listRet = re.findall(strRex, strRet)
                    strRet = "{}-{}-{} {}:{}:{}". \
                        format(listRet[0][0],listRet[0][1],listRet[0][2],listRet[0][3],listRet[0][4],listRet[0][5])
                    fRtc = time.mktime(time.strptime(strRet,'%Y-%m-%d %H:%M:%S'))
                    fCurrentTime = time.time()

                    if fCurrentTime-fRtc >1800:
                        self.fDutRtc = fCurrentTime
                    else:
                        self.fDutRtc = 1
                else:
                    return "--FAIL--fail to get rtc"

            elif 'set' in str_cmd:
                if self.fDutRtc == -9999:
                    return "--FAIL--fail to get time"
                elif self.fDutRtc == 1:
                    return "--PASS--Do not set time"
                else:
                    strTemp = time.strftime('%Y%m%d%H%M%S',time.localtime())
                    nRet,strRet = self.nanohippo.DutSendCmd('rtc --set {}'.format(strTemp), nTimeout)
                    if not nRet:
                        strRet = self.nanohippo.DutReadString()
                        if len(re.findall('\d+', strRet)):
                            return "--FAIL--fail to set rtc"
                        else:
                            return "--PASS--"
                    else:
                        return "--FAIL--fail to set rtc"
                pass
            else:
                return "--FAIL-- Unknown RTC command"

        except Exception as e:
            return "--FAIL--, EXCEPTION: %s"%e.message

    @public
    def checklistedcb(self, *args, **kwargs):
        pass

    @public
    def checkfailcount(self, *args, **kwargs):
        try:
            param1 = args[0]
            strRet = re.sub(' ', '', param1)
            for i in strRet[0:40]:
                if i:
                    return "--FAIL--, Found non zero"
            return "--PASS--"
        except Exception as e:
            return "--FAIL--, EXCEPTION:%s"%e.message
        