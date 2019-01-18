# encoding=utf-8
import os
import json
import re
import math
from TestEngine.Driver.TcpDriver import TcpDriver
from Common.tinyrpc.dispatch import public

from Common.publisher import ZmqPublisher

from Common.BBase import *

import time
from subprocess import Popen
import signal


from TestEngine.Driver.Functions.Callback import *
from Log.LogClient import LogClient
import struct
class ZYNQ_DUMMY(TcpDriver):
    def __init__(self, cfg, publisher=None,uut=None,psw=None):
        super(ZYNQ_DUMMY, self).__init__(cfg)

        self.cfg = cfg
        self.buf_dict = {}
        self.io_table = {}
        self.load_io_table()





        #self.pub = publisher
        self.pid = {}
        self.uut = uut
        self.reset()
        self.gain = 1
        self.offset = 0



        self.m_objBRe = cBruceRe()
        self.m_objBTime = cBruceTime()
        self.m_objBShell = cShell()


        self.eload_res_set = 0.55
        self.eload_res_read = 0.05
        self.eload_hw_gain = (1+(49.4/5.49))   

        self.eload_dac_amp = (1+1.21/1)
        self.factor = [1,0]

        self.subtrahendvalue=-1
        self.minuendvalue = -1

 ####
        #self.power = PsDataLogger(self.uut)
        self.power = psw
        self.psdata = ""
        self.finaltab = {}
        self.hwioresult = []
        self.all_channel_command = "1,all" 
        self.all_channel_command1 = "1,all" 
        self.all_channel_command0 = "40,ch1,ch2,ch3,ch4,ch5,ch6,ch7,ch8,ch9,ch10,ch11,ch12,ch13,ch14,ch15,ch16,ch17,ch18,ch19,ch20,ch21,ch22,ch23,ch24,ch25,ch26,ch27,ch28,ch29,ch30,ch31,ch32,ch33,ch34,ch35,ch36,ch37,ch38,ch39,ch40"
        #self.all_channel_command0 = "1,all1"
        self.timing_start_line_channel  = 37
        self.timing_start_line_channel_value = 0
        self.sampling_rarte = 1000
        self.sampling_rarte = 3
        self.group_flag = 0
        self.count = 40
        self.timing_start_line_channel_tmp = None
        self.waveform_type = "rise"
        self.powersequence_data_table = [-1 for i in range(0,40)]


        self.objPowerLog=None#LogClient(self.uut,"Power.log")#cBruceLogs("/vault/PRM_log/Dut{}_Power.txt".format(self.uut))
        self.objDebugIoLog =LogClient(self.uut, "DebugIo.log")
        self.objDummyLog = LogClient(self.uut, "Dummy.log")
        self.objCalLog = None#LogClient(self.uut, "Calibration.log")

        self.objPowerS =None #cPowerSequence(self.uut, self.io_table["CHANNEL"], zmqports.PWR_SEQUENCER_PUB)

        self.listRet=[-9999,-9999]
        self.listDebugIoCmds=[]

    # for publish msg to log
    def DebugIo(self):
        self.objDebugIoLog.Trace("Start Debug Io")
        for IoCmd in self.listDebugIoCmds:
            self.objDebugIoLog.Trace("IO CMD:{}".format(IoCmd))
            self.cmd_raw_send(IoCmd)
        self.objDebugIoLog.Trace("Finish Debug Io")
    def DummyCheck(self):
        bRet = True
        fV =self.dmmV("MeasureTable","GND_DETECT",10000)
        if fV>1000:
            bRet=False
        print "Dummy {} {} Check Result:{} {}".format(self.uut,self.cfg ,fV,bRet)
        return bRet
    def UpdateFac(self):
        #Calibration Measure Table
        dictMeasureCal = self.io_table.get("Calmeasure")
        for strkey in dictMeasureCal.keys():
            if strkey in self.io_table.get("MeasureTable").keys():
                bRet,listRet = self.ReadFactorFromARM_b_list("testbase",int(dictMeasureCal.get(strkey),16),strNetName = strkey)
                if bRet:
                    strGainNew = "{}".format(struct.unpack('!f', listRet[0].decode('hex'))[0])
                    strOffsetNew = "{}".format(struct.unpack('!f', listRet[1].decode('hex'))[0])
                    self.io_table["MeasureTable"][strkey][3]=strGainNew
                    self.io_table["MeasureTable"][strkey].append(strOffsetNew)
                    self.objCalLog.Trace("{} Cal Update Gain  :{}".format(strkey, strGainNew))
                    self.objCalLog.Trace("{} Cal Update Offset:{}".format(strkey, strOffsetNew))
        # Calibration Eload Table
        dictEloadCal = self.io_table.get("Caleload")
        if bRet:
            for strkey in dictMeasureCal.keys():
                if strkey in self.io_table.get("ELOAD").keys():
                    bRet,listRet = self.ReadFactorFromARM_b_list("testbase",int(dictMeasureCal.get(strkey),16))
                    if bRet:
                        strGainNew = "{}".format(struct.unpack('!f',listRet[0].decode('hex') )[0])
                        strOffsetNew = "{}".format(struct.unpack('!f',listRet[1].decode('hex') )[0])
                        self.io_table["ELOAD"][strkey]["gain"]  =strGainNew
                        self.io_table["ELOAD"][strkey]["offset"]=strOffsetNew
                        self.objCalLog.Trace("{} Cal Update Gain  :{}".format(strkey, strGainNew))
                        self.objCalLog.Trace("{} Cal Update Offset:{}".format(strkey, strOffsetNew))
        return bRet


    def ReadFactorFromARM_b_list(self,strBase,hexAddr,strNetName=""):
        nAddrOffset =0
        nLength=4
        listValue=["",""]
        #print strBase,hexAddr
        bRet,strValue= self.ReadEeprom_b_str(nAddrOffset,nLength,strBase,hexAddr,strNetName = strNetName)
        print "before test",bRet,strValue
        if bRet and "00000001" in strValue:
            for i in range(1,3):
                nAddrOffset+=i*4
                bRet,listValue[i-1]=self.ReadEeprom_b_str(nAddrOffset, nLength, strBase, hexAddr,strNetName = strNetName)
        else:
            bRet =False
        print "after test", bRet, listValue
        return bRet,listValue

    def ReadEeprom_b_str(self,nAddrOffset,nLength,strBase,hexAddr,strNetName =""):
        bRet = True
        flagnum = ""
        nlen = nAddrOffset
        legth = nLength
        #print strBase,hexAddr+len,legth

        recevicestr=""
        strGetCalCmd="eeprom read(%s,cat08,%X,%d)"%(strBase,hexAddr+nlen,legth)
        self.objCalLog.Trace("{} Cal Send :{}".format(strNetName,strGetCalCmd))
        recevicestr=self.cmd_auto_format(strGetCalCmd,timeout=10000)
        bRet,Recevicestr = self.m_objBRe.SubStr_b_str(recevicestr, "\s", "")
        self.objCalLog.Trace("{} Cal Reive:{}".format(strNetName,Recevicestr))

        bRet = ('ACK' in recevicestr) and ("ERR" not in recevicestr)
        if bRet:
            reg = "ACK\s*\((.+?);"
            print "ACK", bRet, recevicestr

            bRet, listRet = self.m_objBRe.MatchStr_b_list(recevicestr, reg)

            print "ack",bRet,listRet
            if bRet and (len(listRet)>=1):
                bRet,listRet= self.m_objBRe.SplitStr_b_list(listRet[0], ",")
                print "Split", bRet, listRet
            if bRet and (len(listRet)>=4):
                flagnum ="%02X%02X%02X%02X"%(int(listRet[3],16),int(listRet[2],16),int(listRet[1],16),int(listRet[0],16))
                print "Split after",flagnum
        self.objCalLog.Trace("{} Cal Value:{}".format(strNetName,flagnum))
        return bRet,flagnum





    def log(self, msg):
        pass
    def load_io_table(self):
        table_name = 'zynq_io.json'
        with open(os.path.dirname(__file__) + '/' + table_name) as f:
            self.io_table = json.load(f)
    def get_io_cmd(self, func, para):
        bRet=True
        strRet= ""
        try:
            get_cmd = self.io_table.get(func.upper())[para.upper()]
            if len(get_cmd) >= 3:
                self.gain = get_cmd[1]
                self.offset = get_cmd[2]
                strRet = get_cmd[0]
            else:
                self.gain = 1
                self.offset = 0
                strRet = get_cmd[0]
            # print('switch_io ' + str(switch_io))
        except Exception as e:
            bRet = False
            strRet = "get_io_cmd Except {} {}".format(func,para)
        return bRet,strRet

    def switch_io(self, command, **kwargs):
        func_name = kwargs['funcname']
        bRet,strRet = self.get_io_cmd(func_name, command)
        if bRet:
            bRet = self.connect()
            strRet = ""
            if bRet:
                if self.status:
                    strRet += self.endStr
                    self.log('send: %s' % strRet)
                    send = self._session.send(strRet)
                    if send > 0:
                        bRet,strRet = self.recv_result()
                        self.log('recv: %s' % strRet)
            else:
                strRet = 'ZYNQ did not connected'


        return bRet,strRet



    def send_cmd(self, command, **kwargs):
        bRet=True
        if not  self.status:
            bRet = self.connect()
        if self.status and bRet:
            command += self.endStr
            s = self._session.send("[{}{}]{}".format(self.uut,self.uut,command))
            if s <= 0:
                bRet = False
        return bRet

    def recv_result(self, tm=1000):

        bRet = True
        strRet = ""
        buf = ''
        size = 1024
        t = int(tm / (self.timeout * 1000))
        failtime = 0
        while True:
            try:
                rev = self._session.recv(size)
                buf += rev
                time.sleep(0.01)
                if buf[-1] == "\n" and buf != "":
                    strRet = buf
                    break
            except Exception as e:
                if failtime >= t:
                    self.disconnect()
                    strRet = "FailTime {}".format(t)
                    bRet = False
                    break
                else:
                    bRet = False
                    failtime += 1
                    continue
        #print "zynq rev :-->>> {}".format(strRet)
        return bRet,strRet
    def stop_ps_thread(self):
        self.cmd_auto_format("power sequence monitoring stop()",timeout=1000)
        if self.objPowerS:
            self.objPowerS.StopDataLog(1)

    def cmd_raw_send(self,strCommand,nTimeOut=500):
        strRet = self.send_recv(strCommand,nTimeOut)
        bRet = True
        if "ERR" in strRet:
            bRet = False
        return strRet
    def cmd_auto_format(self,strCommand,strParam1="",strParam2="",timeout=1000):

        if "adc read" in strCommand:
            strCommand = "adc read({},10)".format(strParam1)
        elif "io set" in strCommand:
            strCommand = strCommand
        elif "dac set" in strCommand:
            strCommand = "dac set(-c,{},{})".format(strParam1,strParam2) #%.01f - param2

        self.objDummyLog.Trace("DummyCheck Send  :{}".format(strCommand))
        strRet = self.send_recv(strCommand,timeout)
        self.objDummyLog.Trace("DummyCheck Recive:{}".format(strRet))
        if "ERR" in strRet:
            strRet=""
        return strRet



    def send_recv(self, command,ntimeout=500):
        self.send_cmd(command)
        self.m_objBTime.Delay(30)
        bRet,strRet= self.recv_result(ntimeout)
        return strRet

    def sync_time(self):
        utc = time.time()
        utc_s = str(int(utc))
        utc_ms = str(int(utc * 1000 % 1000))
        cmd = "synctime(-w,%s,%s)" % (utc_s, utc_ms)
        self.send_cmd(cmd)
        recv_data = self.recvMsg(1024)
        print(recv_data)

    @public('version')
    def version(self, *args, **kwargs):
        func_number = 0
        version_type = ''
        if len(args) > 0:
            version_type = args[0].upper()
            if version_type == 'MCU':
                func_number = 1
            elif version_type == 'PROJECT':
                func_number = 2
            elif version_type == 'HARDWARE':
                func_number = 3
            elif version_type == 'FPGA':
                func_number = 4
            elif version_type == 'FPGA BOM':
                func_number = 5
            else:
                func_number = 0
        else:
            version_type = 'all'
        try:
            bRet=True
            strRet = self.cmd_raw_send('version(%d)' % func_number)
            # result = 'ACK(SW=1.01.04)'
            if bRet:
                if func_number == 0:
                    bRet = False
                elif func_number in [1, 2, 4, 5]:
                    reg = '\(\w+=(.+);DONE;'
                    strRet = re.search(reg, strRet).group(1)
                elif func_number == 3:
                    reg = '\(.+=(.+),.+=(.+);DONE'
                    strRet = re.search(reg, strRet).group(2)
                self.buf_dict.setdefault('vesrion_' + version_type, strRet)

            else:
                bRet = False
                strRet = "version {} {}".format(args[0],args[1])
        except Exception as e:
            bRet = False
        return "--PASS-- {}".format(strRet) if bRet else "--FAIL-- {}".format(strRet)


    @public('sn')
    def sn(self, *args, **kwargs):
        bRet=True
        strRet = ""
        try:
            if len(args) > 0:
                bRet, strRet = self.send_recv('sn(%s)' % args[0])
                reg = '\((.+)\)'
                if bRet:
                    bRet, listRet = self.m_objBRe.MatchStr_b_list(reg,strRet)
                    if bRet:
                        strRet = self.m_objBRe.SubStr_b_str(listRet[0],'"',"")
        except:
            strRet = "Except sn {}".format(str(args))

        return "--PASS-- {}".format(strRet) if bRet else "--FAIL-- {}".format(strRet)

    @public('barcode')
    def barcode(self, *args, **kwargs):
        try:
            if len(args) > 0:
                bRet, strRet = self.send_recv('barcode(%s)' % args[0])
                reg = '\((.+)\)'
                if bRet:
                    bRet, listRet = self.m_objBRe.MatchStr_b_list(reg,strRet)
                    if bRet:
                        strRet = self.m_objBRe.SubStr_b_str(listRet[0],'"',"")
        except:
            strRet = "Except sn {}".format(str(args))

        return "--PASS-- {}".format(strRet) if bRet else "--FAIL-- {}".format(strRet)

    @public('synctime')
    def synctime(self, *args, **kwargs):
        try:
            if len(args) > 0:
                bRet, strRet = self.send_recv('synctime(%s)' % args[0])
                reg = '\((.+)\)'
                if bRet:
                    bRet, listRet = self.m_objBRe.MatchStr_b_list(reg,strRet)
                    if bRet:
                        strRet = self.m_objBRe.SubStr_b_str(listRet[0],'"',"")
        except:
            strRet = "Except sn {}".format(str(args))

        return "--PASS-- {}".format(strRet) if bRet else "--FAIL-- {}".format(strRet)


    def dmmV(self,strNetName,strKeyName,timeout):
        strRet = ""
        bRet = True
        try:

            GAIN = 1
            OFFSET = 0

            listInfo =  self.io_table.get(strNetName).get(strKeyName)
            self.relayFromDict({"CONNECT":listInfo})
            iocmd = listInfo[0]
            channel =listInfo[1]
            gnd =listInfo[2]
            hw_gain =listInfo[3]
            listGnd = self.io_table.get("DMMSwitchGNDTable").get(gnd)
            if gnd=="BKLT":
                self.m_objBTime.Delay(500)
            self.cmd_auto_format(listGnd[0])

            listchannel =self.io_table.get("AISwtichTable").get(channel)

            self.cmd_auto_format(listchannel[0])


            if hw_gain !="":
                GAIN=float(hw_gain)
            if len(listInfo)>=5:
                OFFSET =eval(listInfo[4])

            #self.m_objBTime.Delay(50)

            cmd = "dmm measure(volt)" #'voltage measure(-c, 6V, 1000)'

            strRet = self.cmd_auto_format(cmd)

            bRet = 'DONE' in strRet
            if bRet:
                reg = "ACK\s*\((.+?)mv;"
                bRet,listRet=self.m_objBRe.MatchStr_b_list(strRet,reg)
                if bRet:
                    strRet = round(float(listRet[0]),3)*GAIN  +OFFSET
        except Exception as e:
            print "DmmV Except({}) {} {}".format(e,strNetName,strKeyName)
        return strRet
    def dmmC(self,strNetName,strUnit):
        pass
        #
        # GAIN =1
        # OFFSET=0
        # if strUnit:
        #     strNetName = "{}_UA".format(strNetName)
        #     self.cmd_auto_format("dmm set(100 uA)")
        # else:
        #     strNetName = "{}_MA".format(strNetName)
        #     self.cmd_auto_format("dmm set(2 mA)")
        # self.cmd_auto_format(self.io_table.get("DMMCurrentTable").get(strNetName)[0])
        # self.m_objBTime.Delay(50)

    @public('dmm')
    def dmm(self, *args, **kwargs):
        bRet = True
        strRet = ""
        try:
            if len(args) > 0:

                strUnit = kwargs["unit"]
                nTimeOut=int(kwargs["timeout"])-2000

                if args[0]=="DISCONNECT":
                    self.cmd_auto_format(self.io_table.get("MeasureTable").get(str(args[0])))
                elif "V" in strUnit.upper():
                    strRet = self.dmmV("MeasureTable",args[0],nTimeOut)
                    if strUnit.upper() =="V":
                        strRet="%0.3f"%(strRet/1000)
        except:
            strRet = "Except sn {}".format(str(args))
            bRet = False
        return strRet if bRet else "--FAIL-- {}".format(strRet)

    @public('dmmresistance')
    def dmmresistance(self, *args, **kwargs):
        try:
            if len(args) > 0:
                bRet,strRet = self.switch_io(args[0], funcname='dmmresistance')
                if bRet:
                    time.sleep(0.1)
                    bRet ,strRet = self.send_recv('resistor measure(-r, 2, 100Kohm, 1000, 100)')
                    self.switch_io("DISCONNECT", funcname='dmmvoltage')
                    if bRet:
                        bRet =  'DONE' in strRet
                        if bRet:
                            reg = '([\d\.]+)\sohm'
                            bRet, strRet = self.m_objBRe.MatchStr_b_list(strRet, reg)
                            if bRet:
                                strRet = round(float(strRet),3)

        except:
            strRet = "Except sn {}".format(str(args))
        return "--PASS-- {}".format(strRet) if bRet else "--FAIL-- {}".format(strRet)


    @public('discharger')
    def discharger(self, *args, **kwargs):
        try:

            para = ''
            if len(args) > 0:
                para = args[0].strip().upper()
                discharger = self.io_table.get('DISCHARGER')
                # 判断参数是否为connectall, 如果是，则遍历所以io
                if para == 'CONNECTALL':
                    for io in discharger:
                        # if io is disconnect , by pass
                        if io.upper() == 'DISCONNECT':
                            continue
                        try:
                            # try switch io
                            bRet,strRet = self.switch_io(io, funcname='DISCHARGER')
                            # if reture pass, then continue next io
                            if 'DONE' in strRet:
                                continue
                            else:
                                return '--FAIL--'
                        except Exception as e:
                            #print(e)
                            return '--FAIL--'
                    return '--PASS--'
                elif para in discharger.keys():
                    try:
                        bRet,strRet = self.switch_io(para, funcname='DISCHARGER')
                        if 'DONE' in strRet:
                            return '--PASS--'
                        else:
                            return '--FAIL--'
                    except Exception as e:
                        #print(e)
                        return '--FAIL--'
        except:
            return "--FAIL-- Except"

    def fctmeasure(self,channel):
        strRet = self.cmd_auto_format("adc read",channel)
        nRet=-1
        bRet,listRet = self.m_objBRe.MatchStr_b_list(strRet,"\d+\.?\d*")
        nVal = 0
        if bRet:
            for i in listRet:
                nVal += float(i)
            nRet= nVal/len(listRet)

        return nRet

    def measure_testpoint(self,testpoint):

        GAIN=1
        OFFSET=0

        bRet,strRet=self.relayFromDict({"CONNECT":self.io_table.get("MeasureTable").get(testpoint)})
        if bRet:
            result = self.fctmeasure(self.dictADC[testpoint])
            result = result * GAIN + OFFSET
            bRet, strRet =self.relayFromDict({"CONNECT":self.io_table.get("MeasureTable").get("DISCONNECT")})
            if bRet:
                result = -99999
        else:
            result =-99999

        return result
    def measure_frequence_testpoint(self,strArgs0):
        Frequency_type = "A"
        result = None
        pdm_channel = "PDM"

        measure_frequency = ""
        duty_ratio_frequency=""
        strParam1 = strArgs0
        if "DMIC" in strParam1:
            listIO = self.io_table.get("THDNFrequencyTable").get(strParam1)
            bRetx ,strRetx= self.relayFromDict({"CONNECT":listIO})
            if bRetx:
                Frequency_type = listIO[2]
                dmic_channel = "ch1"
                if "1" in strParam1:
                    dmic_channel = "ch2"
                self.cmd_auto_format("dac output({},635)".format(Frequency_type),timeout=5000)
                self.m_objBTime.Delay(50)

                strRet = self.cmd_auto_format("dmic clk measure({},300,3000)".format(dmic_channel),timeout=5000)

                bRet,strRet = self.m_objBRe.MatchStr_b_list(strRet,"ACK\s*\((.+?)Hz,(.+?)\%")
                if bRet:

                    measure_frequency=strRet[0][0]
                    duty_ratio_frequency=strRet[0][1]
            else:
                bRet= bRetx
                strRet = "THDNFrequencyTable {} relay Fail".format(strParam1)
        else:
            listIO = self.io_table.get("THDNFrequencyTable").get(strParam1)
            bRetx, strRetx = self.relayFromDict({"CONNECT": listIO})
            if bRetx:

                Frequency_type = listIO[2]
                setting = listIO[1]
                self.cmd_auto_format("dac output(A,{})".format(listIO[1]))

                strRet = self.cmd_auto_format("frequency measure(-fd,{},{},300,3000)".format(Frequency_type,setting),timeout=5000)
                bRet, strRet = self.m_objBRe.MatchStr_b_list(strRet, "ACK\s*\((.+?)Hz,(.+?)\%")
                if bRet:

                    measure_frequency = strRet[0][0]
                    duty_ratio_frequency = strRet[0][1]
            else:
                bRet=bRetx
                strRet = "THDNFrequencyTable {} relay Fail".format(strParam1)

        self.listRet=[measure_frequency,duty_ratio_frequency]
        return self.listRet

    @public("measure")
    def measure(self, *args, **kwargs):
        bRet=True
        nRet = -1
        strUnit=kwargs["unit"]
        try:
            if "HZ" in strUnit:
                self.measure_frequence_testpoint(args[0])
                nRet = float(self.listRet[0])
            elif "%" in strUnit:
                nRet = float(self.listRet[1])
            else:
                nRet=-99999
        except:
            bRet = False
        return str(nRet)

    #
    # @public('datalogger')
    # def datalogger(self, *args, **kwargs):
    #     try:
    #         serial_num = ''
    #         with open('/vault/sn.txt') as f:
    #             serial_num = list(f.readlines())[self.uut].strip()
    #         para = ''
    #         result = ''
    #         if len(args) > 0:
    #             para = args[0].strip()
    #             try:
    #                 if para.upper() == 'OPEN':
    #                     self.sync_time()
    #                     result = self.send_recv('datalogger open(all)')
    #                     if 'DONE' in result:
    #                         p1 = Popen(['python', data_logger_path, '--ip=%s' % self.cfg['ip'], '--port=7610', '--addr=-%s-UUT%s-datalogger-VOLTAGE.csv' % (serial_num, self.uut), '--type=%s' % 'V'])
    #                         self.pid['logger1'] = p1.pid
    #                         p2 = Popen(['python', data_logger_path, '--ip=%s' % self.cfg['ip'], '--port=7611', '--addr=-%s-UUT%s-datalogger-CURRENT.csv' % (serial_num, self.uut), '--type=%s' % 'C'])
    #                         self.pid['logger2'] = p2.pid
    #                         return '--PASS--'
    #                 elif para.upper() == 'CLOSE':
    #                     result = self.send_recv('datalogger close()')
    #                     os.kill(self.pid['logger1'], signal.SIGKILL)
    #                     os.kill(self.pid['logger2'], signal.SIGKILL)
    #                 #print(result)
    #                 if result:
    #                     return '--PASS--'
    #             except Exception as e:
    #                 print(e)
    #                 return '--FAIL--'
    #         else:
    #             return '--FAIL--'
    #     except:
    #         return "--FAIL-- Except"
    #
    # @public('rms')
    #
    # def rms(self, *args, **kwargs):
    #     try:
    #         result = self.send_recv('scope rms measure(10, 40000000, 10V, 0)')
    #         print(result)
    #
    #     except Exception as e:
    #         print(e)
    #         return '--FAIL--'
    #
    #     return '--PASS--'
    #
    # @public('pwm')
    # def pwm(self, *args, **kwargs):
    #     try:
    #         para = ''
    #         result = ''
    #         if len(args) > 0:
    #             para = args[0].strip()
    #             try:
    #                 if 'CLOSE' == para.upper():
    #                     result = self.send_recv('codec close pwm()')
    #                     if 'DONE' in result:
    #                         return '--PASS--'
    #                 elif para.upper() == 'FREQUENCY':
    #                     result = self.send_recv('frequency measure(f, 10)')
    #                     print(result)
    #                     return '--PASS--'
    #                 elif para.upper() == 'DUTY':
    #                     result = self.send_recv('frequency measure(d, 10)')
    #                     return round(float(result),3)
    #
    #             except Exception as e:
    #                 print(e)
    #                 return '--FAIL--'
    #         else:
    #             return '--FAIL--'
    #     except Exception as e:
    #         return "--FAIL-- Except"
    #
    # @public('frequency')
    # def frequency(self, *args, **kwargs):
    #     try:
    #         para = ''
    #         result = ''
    #         if len(args) > 0:
    #             para = args[0].strip()
    #             try:
    #                 if 'MCU_CLOCK' == para.upper():
    #                     result = self.send_recv('frequency measure(B,f,10)')
    #                 elif 'FAN' == para.upper():
    #                     result = self.send_recv('frequency measure(A,f,10)')
    #                 if 'DONE' in result:
    #                     reg = '([\d\.]+)\sHz;'
    #                     try:
    #                         return round(float(re.search(reg, result).group(1)), 3)
    #                     except Exception as e:
    #                         return '--FAIL--'
    #                 else:
    #                     return '--FAIL--'
    #             except Exception as e:
    #                 print(e)
    #                 return '--FAIL--'
    #         else:
    #             return '--FAIL--'
    #     except Exception as e:
    #         return "--FAIL-- Except"
    #
    #
    #
    # @public('duty')
    # def duty(self, *args, **kwargs):
    #     try:
    #         para = ''
    #         result = ''
    #         if len(args) > 0:
    #             para = args[0].strip()
    #             try:
    #                 if 'MCU_CLOCK' == para.upper():
    #                     result = self.send_recv('frequency measure(B,d,10)')
    #                 elif 'FAN' == para.upper():
    #                     result = self.send_recv('frequency measure(A,d,10)')
    #                 if 'DONE' in result:
    #                     reg = '([\d\.]+)\s%;'
    #                     try:
    #                         return round(float(re.search(reg, result).group(1)), 3)
    #                     except Exception as e:
    #                         return '--FAIL--'
    #                 else:
    #                     return '--FAIL--'
    #             except Exception as e:
    #                 print(e)
    #                 return '--FAIL--'
    #         else:
    #             return '--FAIL--'
    #     except Exception as e:
    #         return "--FAIL-- Except"
    #
    #
    #
    # @public('digitizervoltage')
    # def digitizervoltage(self, *args, **kwargs):
    #     try:
    #         if len(args) > 0:
    #             bRet,strRet = self.switch_io(args[0], funcname='digitizer')
    #             if bRet:
    #                 time.sleep(0.1)
    #                 val = self.send_recv('scope rms measure(100, 40000000, 10V, 0)')
    #                 print(val)
    #                 if 'DONE' in val:
    #                     reg = '([\d\.]+)\smV'
    #                     try:
    #                         val = re.search(reg, val).group(1)
    #                         self.buf_dict.setdefault(args[0], val)
    #                         return round(float(val), 3)
    #                     except Exception as e:
    #                         return '--FAIL--'
    #                 else:
    #                     return '--FAIL--'
    #             else:
    #                 return '--FAIL--'
    #     except Exception as e:
    #         return "--FAIL-- Except"
    #
    #
    # @public('digitizercurrent')
    # def digitizercurrent(self, *args, **kwargs):
    #     try:
    #         if len(args) > 0:
    #             voltage = self.buf_dict.get(args[0])
    #             if voltage:
    #                 current = float(voltage) / 10.0
    #                 return round(current, 3)
    #             else:
    #                 return '--FAIL--'
    #     except Exception as e:
    #         return "--FAIL-- Except"
    #
    # @public('measurevoltage')
    # def measurevoltage(self, *args, **kwargs):
    #     try:
    #         if len(args) > 0:
    #             bRet,strRet = self.switch_io(args[0], funcname='digitizer')
    #             if bRet:
    #                 time.sleep(0.1)
    #                 val = self.send_recv('scope rms measure(100, 40000000, 10V, 0)')
    #                 print(val)
    #                 if 'DONE' in val:
    #                     reg = '([\d\.]+)\smV'
    #                     try:
    #                         val = re.search(reg, val).group(1)
    #                         self.buf_dict.setdefault(args[0], val)
    #                         return round(float(val), 3)
    #                     except Exception as e:
    #                         return '--FAIL--'
    #                 else:
    #                     return '--FAIL--'
    #             else:
    #                 return '--FAIL--'
    #     except Exception as e:
    #         return "--FAIL-- Except"
    #
    #
    # @public('measurecurrent')
    # def measurecurrent(self, *args, **kwargs):
    #     try:
    #         if len(args) > 0:
    #             bRet,strRet = self.switch_io(args[0], funcname='digitizer')
    #             if bRet:
    #                 time.sleep(0.1)
    #                 val = self.send_recv('scope rms measure(100, 40000000, 10V, 0)')
    #                 print(val)
    #                 if 'DONE' in val:
    #                     reg = '([\d\.]+)\smV'
    #                     try:
    #                         val = re.search(reg, val).group(1)
    #                         self.buf_dict.setdefault(args[0], val)
    #                         return round(float(val), 3)
    #                     except Exception as e:
    #                         return '--FAIL--'
    #                 else:
    #                     return '--FAIL--'
    #             else:
    #                 return '--FAIL--'
    #     except Exception as e:
    #         return "--FAIL-- Except"

    def relayFromDict(self,dictIo):
        bRet=True
        strRet=""
        try:
            dictRelay = dictIo
            strConnectto = "CONNECT"
            iocmd = dictRelay.get(strConnectto)[0]
            self.listDebugIoCmds.append(iocmd)


            strRet = self.cmd_auto_format(iocmd)
            if 'DONE' in strRet:
                strRet= '--PASS--'
            else:
                bRet=False
                strRet= '--FAIL--'

        except Exception as e:
            strRet= "--FAIL-- Except"
        return bRet,strRet


    @public('relay')
    def relay(self, *args, **kwargs):
        strRet="--FAIL--"
        try:
            #bRet,strRet = self.switch_io(args[0], funcname='relay')
            strTestpoint = args[0]

            strConnectto=""
            dictRelay = self.io_table.get("RelayTable").get(strTestpoint)
            if len(args)>=2:
                strConnectto = args[1]
            else:
                strConnectto ="CONNECT"
            iocmd = dictRelay.get(strConnectto)[0]

            self.listDebugIoCmds.append(iocmd)

            strRet =self.cmd_auto_format(iocmd,timeout=kwargs["timeout"]-1000)


            if 'DONE' in strRet:
                strRet = '--PASS--'
            else:
                strRet = '--FAIL--'
        except Exception as e:
            strRet= "--FAIL-- Except"
        return strRet


    @public('relaydisconnect')
    def relaydisconnect(self, *args, **kwargs):
        strRet="--FAIL--"
        try:
            #bRet,strRet = self.switch_io(args[0], funcname='relay')
            strTestpoint = args[0]


            dictRelay = self.io_table.get("RelayTable").get(strTestpoint)

            strConnectto ="DISCONNECT"
            iocmd = dictRelay.get(strConnectto)[0]

            self.listDebugIoCmds.append(iocmd)

            strRet =self.cmd_auto_format(iocmd,timeout=kwargs["timeout"]-1000)


            # if strTestpoint == "PP_VDD_MAIN" or strTestpoint == "PP_VRECT" or strTestpoint == "PP_BATT_VCC":
            #     MCU.InstrumentCmd("dac set", HWIO.SupplyTable[testpoint].DAC, 0)

            if 'DONE' in strRet:
                strRet = '--PASS--'
            else:
                strRet = '--FAIL--'
        except Exception as e:
            strRet = "--FAIL-- Except"
        return strRet

    @public('dmmdiff')
    def dmmdiff(self, *args, **kwargs):
        fRet = 0.0
        bRet = True
        try:

            strParam1 = ""
            strParam2 = ""
            if len(args)>=1:
                strParam1=str(args[0])
                strParam2=str(args[1])


            if "minuend" in strParam2 :
                self.minuendvalue = self.dmm(args[0],timeout=kwargs["timeout"],unit=kwargs["unit"])
                fRet = self.minuendvalue
            elif "subtrahend" in strParam2:
                self.subtrahendvalue = self.dmm(args[0], timeout=kwargs["timeout"], unit=kwargs["unit"])
                fRet=self.subtrahendvalue
            else:
                fRet=float(self.subtrahendvalue)-float(self.minuendvalue)

        except:
            bRet = False
            strRet = "--FAIL-- Except"

        return fRet if bRet else "--FAIL-- {}".format(strRet)

    @public('detectvoltagefall')
    def detectvoltagefall(self, *args, **kwargs):

        strRet = ""
        bRet = True
        try:
            dmm_test_point_t = []
            dmm_test_point_volt_t = []
            detect_level_t = []
            flag_t = []
            loop_timeout = int(kwargs["timeout"])-3000
            loop_count = 0
            each_delay = 1000

            strParam1 = str(args[0])
            strParam2 = str(args[1])

            bRet, listRet = self.m_objBRe.SplitStr_b_list(strParam1, ";")
            if bRet:
                for i in listRet:
                    bRet, listRetIn = self.m_objBRe.MatchStr_b_list(i, "(.+?)$")
                    if bRet:
                        bRetx, strRet = self.m_objBRe.SubStr_b_str(listRetIn[0], " ", "")
                        dmm_test_point_t.insert(0, strRet)
                        dmm_test_point_volt_t.insert(0, strRet + ":\r\n")
                        flag_t.insert(0, 0)
            bRet, listRet = self.m_objBRe.SplitStr_b_list(strParam2, ";")
            if bRet:
                for i in listRet:
                    bRet, listRetIn = self.m_objBRe.MatchStr_b_list(i, "(.+?)$")
                    if bRet:
                        bRetx, strRet = self.m_objBRe.SubStr_b_str(listRetIn[0], " ", "")
                        detect_level_t.insert(0, strRet)
            if len(dmm_test_point_t) == len(detect_level_t):
                bRet=True
                voltage_meas = []
                nEndTimestamp=0
                nBeginTimestamp=self.m_objBTime.Current()
                nLoopTimeout=loop_timeout
                while nEndTimestamp - nBeginTimestamp < nLoopTimeout:
                    loop_count = loop_count + 1
                    self.m_objBTime.Delay(50)
                    for i in range(0, len(dmm_test_point_t)):
                        strArgs1 = dmm_test_point_t[i]
                        detect_level = detect_level_t[i]
                        voltage_meas = self.dmm(strArgs1,timeout=500, unit=kwargs["unit"])
                        if float(voltage_meas) <= float(detect_level):
                            flag_t[i] = 1
                        dmm_test_point_volt_t[i] = dmm_test_point_volt_t[i] + str(voltage_meas) + "\r\n"
                    flag = 1
                    for i in flag_t:
                        if i == 0:
                            flag = 0
                            break
                    if flag != 1:
                        bRet = False
                    else:
                        bRet = True
                        break
                    nEndTimestamp=self.m_objBTime.Current()
            else:
                bRet = False

        except:
            bRet = False
            strRet = "--FAIL-- Except"

        return "--PASS--" if bRet else "--FAIL--"
    @public('detectvoltageraise')
    def detectvoltageraise(self, *args, **kwargs):

        strRet = ""
        bRet = True
        try:
            dmm_test_point_t = []
            dmm_test_point_volt_t = []
            detect_level_t = []
            flag_t = []
            loop_timeout = int(kwargs["timeout"])-3000
            loop_count = 0
            each_delay = 1000

            strParam1 = str(args[0])
            strParam2 = str(args[1])

            bRet,listRet = self.m_objBRe.SplitStr_b_list(strParam1,";")
            if bRet:
                for i in listRet:
                    bRet,listRetIn =  self.m_objBRe.MatchStr_b_list(i,"(.+?)$")
                    if bRet:
                        bRet,strRet = self.m_objBRe.SubStr_b_str(listRetIn[0]," ","")
                        dmm_test_point_t.insert(0,strRet)
                        dmm_test_point_volt_t.insert(0, strRet+":\r\n")
                        flag_t.insert(0,0)
            bRet, listRet = self.m_objBRe.SplitStr_b_list(strParam2, ";")
            if bRet:
                for i in listRet:
                    bRet, listRetIn = self.m_objBRe.MatchStr_b_list(i, "(.+?)$")
                    if bRet:
                        bRet, strRet = self.m_objBRe.SubStr_b_str(listRetIn[0], " ", "")
                        detect_level_t.insert(0,strRet)
            if len(dmm_test_point_t) == len(detect_level_t) :
                bRet = True
                voltage_meas = []
                nEndTimestamp = 0
                nBeginTimestamp = self.m_objBTime.Current()
                nLoopTimeout = loop_timeout
                while nEndTimestamp - nBeginTimestamp < nLoopTimeout:
                #while loop_count < (float(loop_timeout) / (each_delay + 1500)):
                    loop_count = loop_count + 1
                    self.m_objBTime.Delay(50)
                    for  i in range(0,len(dmm_test_point_t)):
                        strArgs1= dmm_test_point_t[i]
                        detect_level = detect_level_t[i]
                        voltage_meas = self.dmm(strArgs1,timeout =500,unit=kwargs["unit"])
                        print "wait raise -->>> {}   to({})".format(voltage_meas,detect_level)
                        if float(voltage_meas) > float(detect_level):
                            flag_t[i] = 1
                        dmm_test_point_volt_t[i] = dmm_test_point_volt_t[i]+str(voltage_meas)+"\r\n"
                    flag = 1
                    for i in flag_t:
                        if i ==0:
                            flag =0
                            break
                    if flag != 1:
                        bRet = False
                    else:
                        bRet=True
                        break
                    nEndTimestamp=self.m_objBTime.Current()
            else:
                bRet = False

        except Exception as e:
            bRet = False
            strRet = "--FAIL-- Except {}".format(e)
            print strRet

        return "--PASS--" if bRet else "--FAIL-- {}".format(strRet)


    def MonitorCtrl(self, *args, **kwargs):
        strRet = ""
        bRet = True
        try:
            self.cmd_raw_send(self.io_table.get("RelayTable").get("I2C_MONITOR_CTRL").get("CONNECT")[0])
            self.cmd_raw_send(self.io_table.get("RelayTable").get("DISCHARGE_CTRL").get("DISCONNECT")[0])

        except Exception as e:
            bRet = False
            strRet = "Except"
        return "--PASS--" if bRet else "--FAIL-- {}".format(strRet)
    @public('UsbfsKill')
    def UsbfsKill(self, *args, **kwargs):
        strRet = ""
        bRet = True
        try:
            self.m_objBShell.RunShell("pkill usbfs")
        except Exception as e:
            bRet = False
            strRet = "Except"
        return "--PASS--" if bRet else "--FAIL-- {}".format(strRet)

    @public('LogAndPsReset')
    def LogAndPsReset(self, *args, **kwargs):
        strRet = ""
        bRet = True
        try:

            listCmds = []

            listCmds.append("datalogger close(ALL)")
            listCmds.append("power sequence monitoring stop()")


            for i in listCmds:
                self.cmd_raw_send(i)



        except Exception as e:
            bRet = False
            strRet = "Except"
        return "--PASS--" if bRet else "--FAIL-- {}".format(strRet)
    @public('reset')
    def reset(self, *args, **kwargs):
        strRet = ""
        bRet = True
        try:

            listCmds = []


            listCmds.append("uart config(BATT,115200,8,1,none,ON)")
            listCmds.append("uart config(SOC,9600,8,1,none,ON)")
            listCmds.append("uart config(SMC,9600,8,1,none,ON)")
            listCmds.append("uart config(PCH,1250000,8,1,none,ON)")
            listCmds.append("eload dac ref(4,ch1=0,ch2=0,ch3=0,ch4=0)")
            self.m_objBTime.Delay(100)


            strConnectto = "DISCONNECT"
            listCmds.append(self.io_table.get("MeasureTable").get(strConnectto)[0])
            listCmds.append(self.io_table.get("DMMSwitchGNDTable").get(strConnectto)[0])
            listCmds.append(self.io_table.get("AISwtichTable").get(strConnectto)[0])



            listCmds.append(self.io_table.get("ELOAD").get(strConnectto)["io"])

            listCmds.append(self.io_table.get("THDNFrequencyTable").get(strConnectto)[0])

            dictRelayTable =  self.io_table.get("RelayTable")
            listCmds.append(dictRelayTable.get("PPVBAT_EN").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("SYS_DETECT").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("DUT_CTRL").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("SMC_LID_LEFT").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("SMC_LID_RIGHT").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("TP_SMC_DEV_SUPPLY_L").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("SWD_CTRL").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("CHARGE_TO_XA_VBUS").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("CHARGE_TO_XB_VBUS").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("VCCP_5V_DCI").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("SPEAKER_RESISTOR").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("POTASSIUM_BOX").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("USBC_XA_CHIMP_VBUS").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("USBC_XB_CHIMP_VBUS").get(strConnectto)[0])


            listCmds.append(dictRelayTable.get("USB_SOC_CTRL").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("USB_ELOAD_CTRL").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("FRE_CTRL").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("SOC_UART_CTRL").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("PCH_UART_CTRL").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("USBC_SIGNAL_CTRL").get(strConnectto)[0])
            listCmds.append(dictRelayTable.get("I2C_MONITOR_CTRL").get(strConnectto)[0])




            listCmds.append(dictRelayTable.get("DISCHARGE_CTRL").get("PPDCIN_G3H")[0])
            listCmds.append(dictRelayTable.get("DISCHARGE_CTRL").get("PP20V_USBC_XA_VBUS")[0])
            listCmds.append(dictRelayTable.get("DISCHARGE_CTRL").get("PPVBAT_G3H_CONN")[0])
            listCmds.append(dictRelayTable.get("DISCHARGE_CTRL").get("PP3V3_S0SW_LCD")[0])
            listCmds.append(dictRelayTable.get("TP_SMC_DEV_SUPPLY_L").get("LOW")[0])




            for i in listCmds:
                self.cmd_raw_send(i)


            self.MonitorCtrl()



        except Exception as e:
            bRet = False
            strRet = "Except"
        return "--PASS--" if bRet else "--FAIL-- {}".format(strRet)



    @public('settach')
    def settach(self, *args, **kwargs):
        strRet = ""
        bRet = True
        try:
            strFreq = "50"
            strDutSycle = "50"
            if len(args)>=1:
                strFreq=args[0]
            strRet = self.cmd_auto_format("signal enable(fan1,{},{})".format(strFreq, strDutSycle),timeout=kwargs["timeout"]-1000)
            if "DONE" not in strRet:
                bRet = False
        except Exception as e:
            bRet = False
            strRet= "--FAIL-- Except"

        return "--PASS--" if bRet else "--FAIL-- {}".format(strRet)
    @public('setio')
    def setio(self, *args, **kwargs):
        strRet = ""
        bRet = True
        try:
            strCmd = args[0]
            strRet = self.cmd_raw_send(strCmd)

        except Exception as e:
            bRet = False
            strRet = "Except"
        return "--PASS--" if bRet else "--FAIL-- {}".format(strRet)



    @public('pdmenable')
    def pdmenable(self, *args, **kwargs):

        strRet = ""
        bRet = True
        try:
            strFreq = "1000"
            if len(args)>=1:

                if len(args)>=2:
                    strFreq = args[1]

                strChannel = "ch1"
                if self.m_objBRe.MatchStr_b(args[0],"1"):
                    strChannel = "ch2"
                strRet = self.cmd_auto_format("pdm enable(2400000,{},3300,PDM,{})".format(strFreq,strChannel),timeout=kwargs["timeout"]-1000)
                if "DONE" not in strRet:
                    bRet = False
            else:
                bRet=False
                strRet = "Need Params 1 2"

        except Exception as e:
            strRet = "pdmenable Exception"
        return "--PASS--" if bRet else "--FAIL-- {}".format(strRet)

    @public('pdmdisable')
    def pdmdisable(self, *args, **kwargs):
        strRet = ""
        bRet = True
        try:
            strChannel = "ch1"
            if self.m_objBRe.MatchStr_b(args[0],"1"):
                strChannel = "ch2"
            strRet = self.cmd_auto_format("pdm disable({})".format(strChannel),timeout=kwargs["timeout"]-1000)
            if "DONE" not in strRet:
                bRet = False

        except Exception as e:
            bRet = False
            strRet = "pdmenable Exception"
        return "--PASS--" if bRet else "--FAIL-- {}".format(strRet)

    #ILOAD/ELOAD close load
    @public('iload')
    def iload(self, *args, **kwargs):
        strIloadName = "ILOAD_A"
        bRet = True
        try:
            bRet,listRet = self.m_objBRe.MatchStr_b_list(args[0],"(.*)_(.+)")
            if bRet:
                strIloadName="ILOAD_{}".format(listRet[0][1])

            strRet = (int(self.dmm(strIloadName,timeout=3000,unit="mV"))/self.eload_hw_gain)/self.eload_res_read

        except Exception as e:
            bRet =False
        return strRet if bRet else "--FAIL--"



    @public('closeload')
    def closeload(self, *args, **kwargs):
        bRet = True
        try:
            self.cmd_auto_format("eload dac ref(4,ch1=0,ch2=0,ch3=0,ch4=0)",timeout=kwargs["timeout"]-1000)
            self.m_objBTime.Delay(100)

        except Exception as e:
            bRet =False
        return "--PASS--" if bRet else "--FAIL--" 

    @public('eload')
    def eload(self, *args, **kwargs):
        strEloadName = "ELOAD_A"
        bRet = True
        strCurrent = args[1]
        try:
            strEloadName = args[0]
            if self.m_objBRe.MatchStr_b(args[0],"_A"):
                strEloadName="ELOAD_A"
            elif self.m_objBRe.MatchStr_b(args[0],"_B"):
                strEloadName="ELOAD_B"
            elif self.m_objBRe.MatchStr_b(args[0],"_C"):
                strEloadName="ELOAD_C"
            elif self.m_objBRe.MatchStr_b(args[0],"_D"):
                strEloadName="ELOAD_D"


            if self.io_table.get("ELOAD").get(strEloadName) and self.io_table.get("ELOAD").get(strEloadName).get("gain"):
                self.gain = eval(self.io_table.get("ELOAD").get(strEloadName).get("gain"))
            if self.io_table.get("ELOAD").get(strEloadName) and self.io_table.get("ELOAD").get(strEloadName).get("offset"):
                self.offset = eval(self.io_table.get("ELOAD").get(strEloadName).get("offset"))
            try:
                nRet = int(strCurrent)*self.gain + self.offset * 1000
                if nRet<0:
                    nRet = 0
            except Exception as e:
                if strCurrent == "DISCONNECT":
                    strEloadName = "DISCONNECT"
                    nRet = 0 
            eload_dac_value = (self.eload_res_set * nRet+(1.21*24.75))/self.eload_dac_amp
            if eload_dac_value <0:
                eload_dac_value = 0

            try:
                eload_cmd = ""
                dict_cmd = self.io_table.get("ELOAD").get(args[0])
                if dict_cmd and dict_cmd.get("dac") and dict_cmd.get("dac")!="":
                    strDac = dict_cmd.get("dac")
                    if strDac and strDac !="":
                        eload_cmd = "eload dac ref(1,ch{}={})".format(strDac, eload_dac_value)

                else:
                    eload_cmd = "eload dac ref(4,ch1={},ch2={},ch3={},ch4={})".format(eload_dac_value,
                                                                                        eload_dac_value,
                                                                                        eload_dac_value,
                                                                                        eload_dac_value)

    
                bRet = self.cmd_auto_format(eload_cmd)
                self.m_objBTime.Delay(30)

                if dict_cmd and dict_cmd.get("io") and dict_cmd.get("io")!="":
                    self.relay(self.io_table.get("EloadTable").get(args[0],""))
                    self.m_objBTime.Delay(30)
            except:
                bRet = False
                strRet = "Exception eload Get Dac Cmd"


        except Exception as e:
            bRet =False
            strRet = "Exception eload"

        return strCurrent if bRet else "--FAIL-- {}".format(strRet)


    @public('thdn')
    def thdn(self, *args, **kwargs):
        bRet = True
        try:
            thdn_timeout = 8000
            if int(kwargs["timeout"]) != 3000:
                thdn_timeout = int(kwargs["timeout"])

            strRet = self.cmd_raw_send("audio measure(-fnv,dual,OFF,20000,5,{})".format(thdn_timeout),thdn_timeout)
            bRet,listRet = self.m_objBRe.MatchStr_b_list(strRet,"ACK\(THD\+N=(.+?)dB,FREQ=(.+)Hz,VPP=(.+?)mV")
            if bRet and len(listRet)==1:
                self._thdn = float(listRet[0][0])
                self.fre = float(listRet[0][1])
                self.amp = float(listRet[0][2])
            else:
                bRet = False

        except Exception as e:
            bRet =False
        return  self._thdn if bRet else "--FAIL--"
    @public('amplitude')
    def amplitude(self, *args, **kwargs):
        bRet = True
        strRet = ""
        try:
            amplitude_value = 0
            thdn_timeout = 8000
            if len(args)>=1:
                thdn_timeout = int(args[0])
            #convert_units
            if "V" == kwargs["unit"]:
                self.amp = float(self.amp)/1000
            amplitude_value = float(self.amp)
            amplitude_value = ((float(amplitude_value))*3/math.sqrt(2))

            amplitude_value = amplitude_value*self.factor[0]+self.factor[1]
            
            strRet =amplitude_value

        except Exception as e:
            bRet =False
        return  strRet if bRet else "--FAIL--" 
    @public('frequency')
    def frequency(self, *args, **kwargs):
        bRet = True
        strRet = ""
        try:
            if "V" == kwargs["unit"]:
                self.fre = float(self.fre)/1000
            strRet = self.fre


        except Exception as e:
            bRet =False
        return  strRet if bRet else "--FAIL--" 





    @public('powersequencemonitor')
    def powersequencemonitor(self, *args, **kwargs):
        bRet =True
        strRet = ""
        try:

            strCmd = args[0]
            ps_ref_dec_command = "ps ref dac(40,"
            self.objPowerLog.Trace("Sequence Monitor Cmd:{}".format(strCmd))
            if "STOP" in strCmd.upper():
                self.objPowerLog.Trace("Sequence Send Cmd:power sequence monitoring stop()")
                self.cmd_auto_format("power sequence monitoring stop()",timeout=1000)
                self.m_objBTime.Delay(5000)
                self.objPowerS.StopDataLog(1)
                #self.power.StopDataLog()
            elif "LEFT" in strCmd.upper() or "IEFI" in strCmd.upper():
                #self.power.get_power_sequence_channel_config(0)
                self.all_channel_command = self.all_channel_command0
                self.group_flag = 0
            elif "RIGHT" in strCmd.upper() or "EFI" in strCmd.upper():
                #self.power.get_power_sequence_channel_config(1)
                self.all_channel_command = self.all_channel_command1
                self.group_flag = 1
            elif "ALL" in strCmd.upper():
                #self.power.get_power_sequence_channel_config(0)
                self.all_channel_command = self.all_channel_command1
                self.group_flag = 2
            elif "START" in  strCmd.upper():
                #self.power.get_power_sequence_channel_config(0)
                self.group_flag = 0
                self.all_channel_command = self.all_channel_command0

            self.objPowerLog.Trace("Sequence Use Channel:{}".format(self.all_channel_command))
            if "STOP" not in strCmd.upper():
                for i in range(0, 40):
                    if self.group_flag == 1:
                        ps_ref_dec_command = "{}ch{}={},".format(ps_ref_dec_command, i+1,self.io_table["CHANNEL"]["CH{}".format(i+40)][4])
                    else:
                        ps_ref_dec_command = "{}ch{}=400,".format(ps_ref_dec_command, i+1)
                response = ""
                ps_ref_dec_command=ps_ref_dec_command[:-1]
                ps_ref_dec_command = ps_ref_dec_command + ")"

                self.m_objBTime.Delay(50)

                strBasePath = self.objPowerLog.GetCurrentFolderPath()
                
                #self.objPowerS.StopDataLog(1)
                #self.m_objBTime.Delay(50)
                
                self.objPowerS.StartDataLog(strBasePath,args[1],1)


                self.sampling_rarte = 1000

                self.objPowerLog.Trace("Sequence Send Cmd:power sequence monitoring stop()")
                self.cmd_auto_format("power sequence monitoring stop()")#stop first
                self.objPowerLog.Trace("Sequence Send Cmd:power sequence trigger time start(10000)")
                self.cmd_auto_format("power sequence trigger time start(10000)")

                powersequence_cmd_str ="power sequence monitoring start({},{})".format(self.sampling_rarte,self.all_channel_command)
                self.objPowerLog.Trace("Sequence Send Cmd:{}".format(powersequence_cmd_str))
                self.m_objBTime.Delay(5000)
                response = self.cmd_auto_format(powersequence_cmd_str)


                bRet = self.m_objBRe.MatchStr_b(response, "DONE")
        except Exception as e:
            bRet = False
            strRet =  "--FAIL-- Except {}".format(e)

        self.objPowerLog.Trace("Sequence Monitor End:{} Info:{}".format(bRet,strRet))

        return "--PASS--" if bRet else "--FAIL--"
        #

    @public('powersequence_parse_data')
    def powersequence_parse_data(self,*args, **kwargs):
        channel_count = 0
        fina_cmd = ""
        cmd_temp = ""
        channel_switch_count = 40
        channel_tmp = 0
        bRet =True
        try:
            strParam1 = args[0]

            self.objPowerLog.Trace("Sequence Parse:{}".format(strParam1))
            if self.count > channel_switch_count:
                channel_switch_count = 0

            if "CH" not in strParam1.upper()  and "ALL" not in strParam1.upper():
                bRet,listRet = self.m_objBRe.MatchStr_b_list(strParam1+",","(.+?),")
                if bRet :
                    for cmd_translate in listRet:
                        for i in range(0,self.count):
                            channel_tmp = i
                            if self.group_flag==1:
                                channel_tmp = channel_switch_count + i
                            if self.io_table["CHANNEL"]["CH{}".format(i+1)][0]==cmd_translate:
                                channel_count +=1
                                cmd_temp = "{},ch{}".format(cmd_temp,i+1)
                                break
                    fina_cmd = "{}{}".format(str(channel_count),cmd_temp)
                    #bRet = True
                    try:
                        if int(fina_cmd)==0:
                            bRet = False
                    except Exception as e:
                        pass
            else:
                fina_cmd = strParam1

            strCmd= "power sequence trigger time read({},{})".format(self.waveform_type,fina_cmd)
            self.objPowerLog.Trace("Sequence Parse Send:{}".format(strCmd))
            power_sequence_timing_result_string = self.cmd_auto_format(strCmd)

            self.objPowerLog.Trace("Sequence Parse Recv:{}".format(power_sequence_timing_result_string))

            if power_sequence_timing_result_string.find("DONE")<0:
                bRet =False
            bRet,listRet = self.m_objBRe.MatchStr_b_list(power_sequence_timing_result_string,"ch\d+=\d+")
            if bRet :
                for cmd_translate in listRet:
                    bRet,listRetIn = self.m_objBRe.MatchStr_b_list(cmd_translate,"ch(.+)=(.+)")
                    if bRet and len(listRetIn)==1:
                        powersequence_channel_id = listRetIn[0][0]
                        powersequence_time_step  = listRetIn[0][1]
                        if int(powersequence_channel_id) == self.timing_start_line_channel:
                            self.timing_start_line_channel_value = int(powersequence_time_step)

                        self.powersequence_data_table[int(powersequence_channel_id)-1] = int(powersequence_time_step)

        except Exception as e:
            bRet = False
        self.objPowerLog.Trace("Sequence Parse End :{}".format(self.powersequence_data_table))
        return "--PASS--" if bRet else "--FAIL--"


    @public('powersequencert')
    def powersequencert(self, *args, **kwargs):
        powersequencetiming_result = None
        powersequencetiming_result_str = ""
        powersequencetiming_result_count = 0
        test_plan_netname = ""
        netname_count = 0
        netname_str = ""
        strParam1 = args[0]
        strParam2 = args[1]
        argsNew = []

        bRet = True
        try:

            self.objPowerLog.Trace("Sequence Sequencert Start :{} {}".format(strParam1,strParam2))
            if strParam1.upper() == "ALL":
                argsNew.append(self.all_channel_command)
                self.powersequence_parse_data(argsNew[0],timeout=kwargs["timeout"])
                for i in range(0,40):
                    test_plan_netname = "CH{}".format(i+1)
                    if self.io_table["CHANNEL"][test_plan_netname][0] != "NONE":
                        test_plan_netname = self.io_table["CHANNEL"][test_plan_netname][0]
                    powersequencetiming_result_str = "{},{}={}".format(powersequencetiming_result_str,test_plan_netname,self.powersequence_data_table[i])
            else:
                self.powersequence_parse_data(args[0],args[1],timeout=kwargs["timeout"])
                if strParam2.upper().find("CH") >=0:
                    bRet ,listRet =self.m_objBRe.MatchStr_b_list(strParam2+",","(.+?),")
                    if bRet:
                        for cmd_translate in listRet:
                            for i in range(1,41):
                                if self.io_table["CHANNEL"]["CH{}".format(i)][1] != cmd_translate:
                                    netname_count += 1
                                    if self.group_flag ==1:
                                        netname_str = "{},ch{}".format(netname_str,(i - 40))
                                    else:
                                        netname_str = "{},ch{}".format(netname_str,i)
                        strParam2= "{}{}".format(netname_count,netname_str)
                bRet,listRet = self.m_objBRe.MatchStr_b_list(strParam2+",","CH(.+?),")
                if bRet:
                    for i in range(0,len(listRet)):
                        powersequencetiming_result_count  +=  1
                        if self.group_flag ==1:
                            test_plan_netname = "CH{}".format(i+40)
                        else:
                            test_plan_netname = "CH{}".format(i)
                        if self.io_table["CHANNEL"][test_plan_netname][1] !="NONE":
                            test_plan_netname = self.io_table["CHANNEL"][test_plan_netname][1]
                        powersequencetiming_result_str = "{},{}={}".format(powersequencetiming_result_str,test_plan_netname,self.powersequence_data_table[i])
            if powersequencetiming_result_count ==1:
                bRet,listRet = self.m_objBRe.MatchStr_b_list(powersequencetiming_result,"=(.+)")
                if bRet:
                    powersequencetiming_result = float(listRet[0])
                else:
                    bRet,listRet = self.m_objBRe.MatchStr_b_list(powersequencetiming_result_str,"^[\s\S]{1}(.*)$")
                    response = ""
                    if bRet:
                        powersequencetiming_result = listRet[0]



        except Exception as e:
            bRet = False
        self.objPowerLog.Trace("Sequence Sequencert End :{} {}".format(bRet,powersequencetiming_result))
        return powersequencetiming_result if bRet else "--FAIL--"

    @public('powersequencedelta')
    def powersequencedelta(self, *args, **kwargs):
        delta_result = None
        delta_result_str = ""
        delta_result_count = 0
        channel_timing  = None
        check_count = 0
        waveform_type_tmp = ""
        timing_start_line_channel_tmp_str = ""
        flag = args[0]
        argstosend=[]

        bRet = True
        try:
            bRet,listRet =  self.m_objBRe.MatchStr_b_list(args[1],"(.+),(.+)")
            if bRet and  len(listRet) ==1 :
                waveform_type_tmp = listRet[0][0]
                timing_start_line_channel_tmp_str = listRet[0][1]
            
                for i in range(0,40):
                    if self.io_table["CHANNEL"]["CH{}".format(i+1)][0] == timing_start_line_channel_tmp_str:
                        if i>self.count:
                            self.timing_start_line_channel_tmp = i - self.count
                        else:
                            self.timing_start_line_channel_tmp = 1
            else:
                waveform_type_tmp = args[1]

            if self.timing_start_line_channel_tmp is None:

                self.timing_start_line_channel_tmp = self.timing_start_line_channel

            if flag.upper().find("ALL")>=0 :
                flag = self.all_channel_command
                if waveform_type_tmp.lower()=="rise" or waveform_type_tmp.lower()=="fall":
                    self.waveform_type = waveform_type_tmp.lower()
                self.powersequence_parse_data(self.all_channel_command,args[1],timeout=kwargs["timeout"])
                for i in range(0,self.count):

                    if self.powersequence_data_table[i] == 0: 
                        channel_timing = 0
                    else:
                        channel_timing = self.powersequence_data_table[i]-self.powersequence_data_table[self.timing_start_line_channel_tmp]
                    #channel_timing #unit Change
                    if kwargs["unit"].upper() == "MS":
                        channel_timing ="%0.3f"%float(channel_timing/1000000.0)
                    if i==0:
                        delta_result_str = "{}".format(channel_timing)
                    else:
                        delta_result_str = "{},{}".format(delta_result_str,channel_timing)
            else:
                for i in range(0,40):
                    if self.io_table["CHANNEL"]["CH{}".format(i+1)][0] == flag:
                        if i > self.count:
                            strParam1 = "1,ch{}".format(i-self.count)
                        else:
                            strParam1 = "1,ch{}".format(i)
                        break
                    else:
                        check_count+=1
                    if check_count>40:
                        bRet = False
                        break
                self.powersequence_parse_data(strParam1, args[1], timeout=kwargs["timeout"])
                if bRet :
                    bRet,listRet = self.m_objBRe.MatchStr_b_list(flag+",","CH(.+?),")
                    if bRet:
                        for delta_temp in listRet:
                            delta_result_count +=1
                            delta_result_tmp = self.powersequence_data_table[int(delta_temp)-1]-self.powersequence_data_table[self.timing_start_line_channel_tmp-1]
                            if delta_result_tmp<0:
                                delta_result_tmp = 0
                            delta_result_str = "{},{}".format(delta_result_str,delta_result_tmp)
            if bRet:
                if delta_result_count==1:
                    bRet,listRet = self.m_objBRe.MatchStr_b_list(delta_result_str,",(.+)")
                    if bRet:
                        delta_result = listRet[0]
                else:
                    delta_result=delta_result_str

                if "all" in args[0]:
                    self.finaltab={}
                    self.hwioresult=[]
                    bRet,listRet = self.m_objBRe.SplitStr_b_list(delta_result,",")
                    if bRet and len(listRet)==40:
                        for i in range(0,len(listRet)) :
                            self.finaltab[self.io_table["CHANNEL"]["CH{}".format(i+1)][0]]=listRet[i]


        except Exception as e:
            bRet = False
        print "powersequencedelta Restult is {}".format(delta_result_str)
        return "--PASS--" if bRet else "--FAIL--"



    @public('psdata_handle')
    def psdata_handle(self, *args, **kwargs):
        strRet = ""
        bRet = True
        try:
            self.objPowerLog.Trace("Sequence Handle Start :{}".format(args[0]))
            # if len(self.hwioresult)==0 :
            #     for i in range(0, 40):
            #         self.hwioresult.append(self.io_table["CHANNEL"]["CH{}".format(i+1)][0])

            strRet=self.finaltab[args[0]]


            self.objPowerLog.Trace("Sequence Handle Table :{}".format(self.finaltab))


        except Exception as e:
            bRet = False

        self.objPowerLog.Trace("Sequence Handle End :{} {}".format(bRet,strRet))
        return strRet if bRet else "--FAIL--"

