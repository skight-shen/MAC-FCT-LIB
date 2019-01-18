from ingenuity.tinyrpc.dispatch import public
from ingenuity.driver.LibCallPy import *
import time,re,os,sys
from ingenuity.driver.dataDriver import TcpClient
import json

class Zynq(TcpClient):
    def __init__(self, addr, dut):
        super(Zynq, self).__init__(addr)
        self.io_table = self.load_io_table()
        self.relayTable = self.io_table.get('RelayTable')
        self.measureTable = self.io_table.get('MeasureTable')
        self.DMMSwitchGNDTable = self.io_table.get('DMMSwitchGNDTable')
        self.AISwtichTable = self.io_table.get('AISwtichTable')
        self.THDNFrequencyTable = self.io_table.get('THDNFrequencyTable')
        self.eloadTable = self.io_table.get("ELOAD")
        self.channelTable = self.io_table.get("CHANNEL")
        self.datalogTable = self.io_table.get("DataLog")
        self.objPwrSeq = cPowerSequence(1, self.channelTable, zmqports.PWR_SEQUENCER_PUB)
        self.objDut = dut
        self.powersequence_data_table = {}
        #below tables are used for USB module
        self.type_reset_table = [["07","68"],["07","68"],["07","68"],["10","68"], \
                                 ["0C","6c"],["0D","68"],["00","6c"],["01","6c"], \
                                 ["02","6c"],["03","6c"],["06","6c"],["08","6c"], \
                                 ["0E","6c"],["0F","6c"],["11","6c"]]
        self.type_eload_table = [["XAXB", "TOP", "ch1ch2", "08,6c", "00,68", "0D,6c", "07,6c"], \
                                 ["XAXB", "BOT", "ch1ch2", "08,68", "00,68", "0D,6c", "07,6c"], \
                                 ["TATB", "TOP", "ch3ch4", "08,6c", "00,68", "0D,6c", "07,6c"], \
                                 ["TATB", "BOT", "ch3ch4", "08,68", "00,68", "0D,6c",  "07,6c"]]
        self.type_swtich_table = [["2.0", "TOP", "0C,68", "0E,68", "08,6c", "01,68", "10,68", "0F,68", "0C,6c", "00,6c", "07,6c"], \
                                  ["2.0", "BOT", "0C,68", "0E,68", "08,68", "02,68", "10,6c", "0F,6c", "0E,6c", "00,6c", "07,6c"], \
                                  ["3.0", "TOP", "0C,68", "0E,68", "08,6c", "03,68", "10,6c", "0F,68", "00,6c", "07,6c"], \
                                  ["3.0", "BOT", "0C,68", "0E,68", "08,68", "06,68", "10,6c", "0F,68", "00,6c", "07,6c"]]

        if self.connect():
            print 'Zynq connected successfully.'
        else:
            print 'Zynq failed to connected'
        return

    def load_io_table(self):
        with open(u'./functions/zynq_io.json', 'rU') as f:
            table = json.load(f)
        return table

    @public
    def fixtureid(self, *args,**kwargs):
        strId = ''
        try:
            cmd = "[]eeprom string read(translation,cat08,20,17)"
            ret = self.req_recv(cmd) #[]ACK("PRM_P1_0002_SLOT1";DONE;101424,731,101424,766,35)
            strId = re.split(r'\"', ret)[1]
        except Exception as e:
            return "--FAIL--, EXCEPTION: %s" % e.message
        return strId

    @public
    def vendor_id(self, *args, **kwargs):
        return u'0x01:PRM'

    @public
    def getxavier_fw(self, *args, **kwargs):
        cmd = "[]version(0)"
        ret = self.req_recv(cmd)
        """
                    []ACK($
            MCU Software name:ARM Board D3-J213_FCT_PRM$
            ,MCU Software version:5.00.01$
            ,Hardware name:ARM Board D3$
            ,Hardware version:D3.0$
            ,Compile time:2018-10-26 15:15:37$
            ,FileSystem version: v3.3
            $
            ,FPGA version:V01.01$
            ,Author:SmartGiant$
            ,FSBL version:v2017.4_1.0$
            ,Kernel version:4.9.0-xilinx
            $
            ,devicetree version:v1.0.0$
            ,uboot version:2017.4$
            ;DONE;101621,787,101621,789,2)
        """
        str_fw = re.findall('\:(.+?)\$', ret)[1]
        return str_fw

    @public
    def disconnect(self,*args, **kwargs):
        if len(args) == 0:
            return 'missing parameters'
        else:
            param1 = args[0]
            try:
                if self.io_table.has_key(param1):
                    signalTable = self.io_table.get(param1)
                else:
                    signalTable = self.relayTable.get(param1)
                cmd = '[]' + signalTable.get('DISCONNECT')[0]
                ret = self.req_recv(cmd)
                if 'DONE' in ret:
                    return "--PASS--"
            except Exception as e:
                return e.message
        return '--FAIL--'

    @public
    def relay(self, *args, **kwargs):
        strParam1 = args[0]
        if len(args) == 2:
            strParam2 = args[1]
        else:
            strParam2 = "CONNECT"

        try:
            dictSignal = self.relayTable.get(strParam1)
            strCmd = '[]' + dictSignal.get(strParam2)[0]
            strRet = self.req_recv(strCmd)
            if strRet.find('DONE') < 0:
                return "--FAIL--"
            else:
                return "--PASS--"
        except Exception as e:
            return "--FAIL--, %s" % e.message

    @public
    def dmm(self, *args, **kwargs):
        GAIN = 1.0
        OFFSET = 0

        if len(args) == 0:
            return 'missing parameters'
        else:
            param1 = args[0]
        strUnit = kwargs['unit']

        listInfo = self.measureTable.get(param1)
        strCmd = '[]' + listInfo[0]
        strChannel = listInfo[1]
        strGnd = listInfo[2]
        strGain = listInfo[3]
        self.req_recv(strCmd)

        strCmd = '[]' + self.DMMSwitchGNDTable.get(strGnd)[0]
        self.req_recv(strCmd)

        strCmd = '[]' + self.AISwtichTable.get(strChannel)[0]
        self.req_recv(strCmd)

        if len(strGain) != 0:
            GAIN = float(strGain)

        strCmd = "[]dmm measure(volt)"
        strRet = self.req_recv(strCmd)

        if 'DONE' in strRet:
            strVoltage = re.findall("ACK\s*\((.+?)mv;",strRet)[0]
            strVoltage = round(float(strVoltage), 3)*GAIN + OFFSET

        if strUnit.upper() == 'V':
            strVoltage = round(strVoltage/1000, 3)

        return strVoltage

    @public
    def usbctrl(self, *args, **kwargs):
        i2cBus = ["usbc_i2c_1", "usbc_i2c_2"]
        deviceAddr = ["0x38", "0x39"]

        if len(args) == 0:
            return 'missing parameters'
        elif len(args) == 1:
            param1 = args[0]
        else:
            param1 = args[0]
            param2 = args[1]

        try:
            if param1.upper() == 'RESET':
                for i in range( len(self.type_reset_table) ):
                    cmd1 = "[]i2c write(usbc_i2c_1,0x38,3,09,01,{})".format(str(self.type_reset_table[i][0]))
                    ret1 = self.req_recv(cmd1)

                    cmd2 = "[]i2c write(usbc_i2c_1,0x39,6,08,04,47,50,73,{})".format(str(self.type_reset_table[i][1]))
                    ret2 = self.req_recv(cmd2)
                    if ret1.find("DONE") < 0 or ret2.find("DONE") < 0:
                        return "--FAIL--"

        except Exception as e:
            return "--FAIL--," + e.message

        return "--PASS--"

    @public
    def powersequencemonitor(self, *args, **kwargs):
        all_channel_command = ["1,all", "40,ch1,ch2,ch3,ch4,ch5,ch6,ch7,ch8,ch9,ch10,ch11,ch12,ch13,ch14,ch15,ch16,ch17,ch18,ch19,ch20,ch21,ch22,ch23,ch24,ch25,ch26,ch27,ch28,ch29,ch30,ch31,ch32,ch33,ch34,ch35,ch36,ch37,ch38,ch39,ch40"]
        strParam1 = args[0]
        assert len(strParam1) != 0
        try:
            if 'STOP' in strParam1.upper():
                self.objPwrSeq.StopDataLog(1)
                #self.sendMsg("[]power sequence monitoring stop()")
            elif 'START' in strParam1.upper():
                self.sendMsg("[]power sequence monitoring stop()")
                self.sendMsg("[]power sequence trigger time start(10000)")
                powersequence_cmd_str = "[]power sequence monitoring start(1000,{})".format(all_channel_command[0])
                strRet = self.req_recv(powersequence_cmd_str)
                if 'DONE' not in strRet:
                    return "--FAIL--"
            return "--PASS--"
        except Exception as e:
            return "--FAIL--, %s" %e.message

    @public
    def detectvoltageraise(self, *args,**kwargs):
        try:
            bFlag = False
            strParam1 = args[0].split(';')
            strParam2 = args[1].split(';')
            nTimeout =  kwargs['timeout']
            startTime = time.time()
            while time.time()-startTime <= nTimeout:
                if len(strParam1) == len(strParam2):
                    volt_list = [self.dmm(i, unit='V', timeout=10000) for i in range(len(strParam1)-1)]
                    for i in range(len(strParam1)-1):
                        if volt_list[i] < strParam2[i]:
                            bFlag = False
                            break
                        else:
                            bFlag = True
                else:
                    bFlag = False
                    break
            return "--PASS--" if bFlag else '--FAIL--'

        except Exception as e:
            return "--FAIL--, EXCEPTION: %s"%e.message

    @public
    def detectvoltagefall(self,*args, **kwargs):
        try:
            bFlag = False
            strParam1 = args[0].split(';')
            strParam2 = args[1].split(';')
            nTimeout = kwargs['timeout']
            startTime = time.time()
            while time.time()-startTime <= nTimeout:
                if len(strParam1) == len(strParam2):
                    volt_list = [self.dmm(i, unit='V', timeout=10000) for i in range(len(strParam1)-1)]
                    for i in range(len(strParam1)-1):
                        if volt_list[i] > strParam2[i]:
                            bFlag = False
                            break
                        else:
                            bFlag = True
                else:
                    bFlag = False
                    break
            return "--PASS--" if bFlag else '--FAIL--'

        except Exception as e:
            return "--FAIL--, EXCEPTION: %s"%e.message

    @public('powersequencedelta')
    def powersequencedelta(self, *args, **kwargs):
        try:
            content = args[0]
            if r',' in args[1]:
                trigger_mode = args[1].split(',')[0]
                reference_channel = args[1].split(',')[1]
            else:
                trigger_mode = args[1]

            if 'all' in content.lower():  # Calculate pwr sequence timing for all channels
                content = '1,all'
            else:  # Calculate pwr sequence timing for specific channels
                if r',' not in content:
                    content = '1,' + content
                else:
                    signal_count = len(content.split(r','))
                    content = str(signal_count) + content

            if self.powersequence_parse_data(trigger_mode, content, reference_channel, kwargs):
                return "--PASS--"
            else:
                return "--FAIL--"
        except Exception as e:
            return "--FAIL--, EXCEPTION: %s" % e.message

    def powersequence_parse_data(self, mode, content, reference_channel, **kwargs):
        timeOut = kwargs['timeout']
        unit = kwargs['unit']
        try:
            for i in range(1,81):
                if self.channelTable['CH{}'.format(i)][0] == reference_channel:
                    reference_channel_id = i
                    break
                else:
                    reference_channel_id = 1

            str_cmd = 'power sequence trigger time read({},{})'.format(mode, content)
            strRet = self.req_recv(str_cmd)
            reference_tim_step = re.findall("ch{}=(.+),".format(reference_channel_id), strRet)[0]
            listRet = re.findall("ch\d+=\d+", strRet)
            for item in listRet:
                listRetIn = re.findall("ch(.+)=(.+)", item)
                channel_id = listRetIn[0]
                tim_step = float(listRetIn[1]) - float(reference_tim_step)
                if 'ms' in unit.lower():
                    tim_step = "%.3f" % (tim_step/1000000)
                self.powersequence_data_table[channel_id] = tim_step
            return 1
        except Exception as e:
            return 0

    def reset(self):
        try:
            self.req_recv("[]uart config(SOC,9600,8,1,none,ON)")
            self.req_recv("[]uart config(SMC,9600,8,1,none,ON)")
            self.req_recv("[]uart config(PCH,115200,8,1,none,ON)")
            self.req_recv("[]pdm disable(ch1)")
            self.req_recv("[]pdm disable(ch2)")
            self.req_recv("[]io chip set(cp21=0x7FB9)")
            self.req_recv("[]eload dac ref(4,ch1=0,ch2=0,ch3=0,ch4=0)")
            self.usbctrl("reset")
            fValue = self.dmm("PM_PCH_SYS_PWROK", timeout=5000, unit="V")
            fActiveValue = 0.0
            if float(fValue) > 1:
                if self.objDut:
                    self.objDut.efidiags("reset -s", timeout=30000)
                    strRet = self.detectvoltagefall("PM_PCH_SYS_PWROK;SMC_SYSRST_L_TO;PP3V3_S5;", "1;1;1;", timeout=10000,
                                                    unit="V")
            fActiveValue = self.dmm("PMU_ACTIVE_READY", timeout=10000, unit="V")
            if float(fActiveValue) > 1.5:
                self.objDut.connect()
                strMode = self.objDut.GetCurrentMode()
                if "iefi" in strMode:
                    self.objDut.iefisend("reset", timeout=600000)
                    self.objDut.enteriboot(timeout=100000)
                    strMode = self.objDut.GetCurrentMode()
                self.objDut.disconnect()
                self.disconnect("MeasureTable")
                self.disconnect("DMMSwitchGNDTable")
                self.disconnect("AISwtichTable")
                self.disconnect("EloadTable")
                self.disconnect("THDNFrequencyTable")

                self.disconnect("XA_CC_TO_TARGET",timeout=5000)
                self.disconnect("CHARGE_TO_XA_VBUS",timeout=5000)
                self.disconnect("USBC_XA_CHIMP_VBUS",timeout=5000)
                self.disconnect("USBC_SIGNAL_CTRL",timeout=5000)
                self.disconnect("XB_CC_TO_CHARGE",timeout=5000)
                self.disconnect("CHARGE_TO_XB_VBUS",timeout=5000)
                self.disconnect("USBC_XB_CHIMP_VBUS",timeout=5000)

                self.relay("DISCHARGE_CTRL","PPDCIN_G3H",timeout=5000)
                self.relay("DISCHARGE_CTRL","PP20V_USBC_XA_VBUS",timeout=5000)

                #4 finger rest
                if float(fActiveValue) > 1.5:
                    self.relay("DUT_CTRL", "PMU_RSLOC_RST_R_L", timeout=5000)
                    time.sleep(4.5)
                    self.relay("DUT_CTRL", "PMU_ONOFF_R_L", timeout=5000)
                    time.sleep(4.5)
                    strRet = self.detectvoltagefall("PP2V7_NAND;PP1V8_SSD;PP0V9_SSD;PP3V3_G3H_RTC;SYS_DETECT_TO;","0.1;0.1;0.1;0.1;0.1;", timeout=10000, unit="V")
                time.sleep(1)

                #self.disconnect('RelayTable')
                self.relay("DISCHARGE_CTRL","PPVBAT_G3H_CONN",timeout=5000)
                self.relay("DISCHARGE_CTRL","PPBUS_G3H",timeout=5000)
                self.relay("DISCHARGE_CTRL","PP3V3_S0SW_LCD",timeout=5000)
                #self.relay("TP_SMC_DEV_SUPPLY_L", "LOW", timeout=5000)

                time.sleep(1)
                self.disconnect("PPVBAT_EN", timeout=5000)
                self.disconnect("SYS_DETECT",timeout=5000)
                self.disconnect("SPKR_ID0",timeout=5000)
                self.disconnect("DUT_CTRL",timeout=5000)
                self.disconnect("SMC_LID_LEFT",timeout=5000)
                self.disconnect("SMC_LID_RIGHT",timeout=5000)
                self.disconnect("TP_SMC_DEV_SUPPLY_L",timeout=5000)
                self.disconnect("SWD_CTRL",timeout=5000)
                self.disconnect("VCCP_5V_DCI",timeout=5000)
                self.disconnect("SPKR_RESISTOR",timeout=5000)
                self.disconnect("USB_SOC_CTRL",timeout=5000)
                self.disconnect("USB_ELOAD_CTRL",timeout=5000)
                self.disconnect("FRE_CTRL",timeout=5000)
                self.disconnect("SOC_UART_CTRL",timeout=5000)
                self.disconnect("PCH_UART_CTRL",timeout=5000)
                self.disconnect("I2C_MONITOR_CTRL",timeout=5000)

                self.relay("TP_SMC_DEV_SUPPLY_L", "LOW", timeout=5000)

                self.disconnect("PPDCIN_EN",timeout=5000)
                self.disconnect("SYS_DETECT_FIXTURE",timeout =5000)
                self.disconnect("FAN_DMIC_CTRL",timeout =5000)
                self.disconnect("SMC_UART_CTRL",timeout =5000)
                self.disconnect("PCH_UART_CTRL",timeout =5000)
                self.disconnect("RESET_TCA6416A",timeout =5000)
                self.disconnect("SOC_FORCE_DFU_CTRL",timeout =5000)
                self.disconnect("SOC_USB_VBUS_CTRL",timeout =5000)
                self.disconnect("SMBUS_I2C_CTRL",timeout =5000)

                time.time(1)
                self.disconnect('POWER_DISCHARGE',timeout=5000)
                strRet = self.detectvoltagefall("PPBUS_G3H;PPVBAT_G3H_CONN_DIV;PPVOUT_S0_LCDBKLT_DIV;", "0.2;0.2;0.2;",timeout=7500, unit="V")

            return "--PASS--"
        except Exception as e:
            return '--FAIL--, %s' % e.message
