import socket
import time
import struct
from Common.BBase import *
from Common.tinyrpc.dispatch import public
import numpy
import re
import json
import csv

class Tcp34410(object):
    """"
    Tcp34410 is a non-blocking socket client
    not recommand to use this class to initialize a Tcp34410
    please use DriverManger to initialize Driver
    ----------------------------------------------------------
    args:
        cfg(dict):
            config format like blow
            cfgSample = {
                'type':'tcp'
                'endStr':'smu',
                'id':'123456',
                'ip':'192.168.99.66',
                'port':7600
            }

    """

    # TODO:add timeout sa self.timeout,beacause I need use self.timeout to computer the real timeout.
    def __init__(self,objzynq=None):
        super(Tcp34410, self).__init__()
        self.objzynq = objzynq
        self.cfg = objzynq.cfg
        self.timeout = 0.2
        self.instrument_name = "Agilent-34410"
        #self.Id = cfg['id']
        self.endStr = '\r\n'#self.cfg['endStr']
        self.netCfg = ('169.254.4.10',5025)
        self.status = False
        self._session = None
        self.m_objBRe = cBruceRe()
        self.m_objBTime = cBruceTime()
        self.m_objBShell = cShell()
        # self.io_table = {}
        # self.load_io_table()
        self.eload_res_read = 0.05 #unit is "ohm"
        self.eload_hw_gain = (1 + (49.4 / 5.49))
        self.eload_res_set = 0.55  #unit is "ohm"
        self.eload_dac_amp = (1+1.21/1)
        self.load_calibrition_table()
        self.calibrition_table = {}
        self.fix_id = ''
        self.read_fix_id()


    def load_calibrition_table(self):
        table_name = 'Calibrition.json'
        with open(os.path.dirname(__file__) + '/' + table_name) as f:
            self.calibrition_table = json.load(f)


    def connect(self):
        bRet = True
        bRet = self.disconnect()
        try:
            self._session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._session.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self._session.settimeout(self.timeout)
        except Exception as e:
            bRet = False
        try:
            if self._session.connect_ex(self.netCfg)==0:
                self.status = True
            else:
                self.status = False
        except Exception as e:
            bRet = False
        time.sleep(0.01)
        return bRet
        # print(str(self.netCfg) + ' fail')

    def disconnect(self):
        if self._session and self.status:
            self._session.shutdown(socket.SHUT_RDWR)
            self._session.close()
            del self._session
            self.status = False
            self._session = None
            time.sleep(0.01)
        return True

    def sendMsg(self, command, **kwargs):
        if not self.status:
            self.connect()
        if self.status:
            command += self.endStr
            if command[0] != '>':
                command = '>' + command
        else:
            raise Exception('disconnect')
        try:
            send = self._session.send(command)
            if send <= 0:
                raise RuntimeError('Pip Broken')
        except Exception as e:
            raise e

    def sendMCU(self, command):
        if not self.status:
            self.connect()
        if self.status:
            try:
                self._session.send(command)
            except Exception as e:
                raise e

    # TODO change the recv func of TCP
    def recvMsg(self, tm=1000):
        buf = ''
        size = 1024
        t = int(tm / (self.timeout * 1000))
        failtime = 0
        while True:
            try:
                rev = self._session.recv(size)
                buf += rev
                #time.sleep(0.01)
                if buf[-1] == "\n" and buf != "":
                    self.disconnect()
                    return buf
            except Exception as e:
                if failtime >= t:
                    self.disconnect()
                    print(e)
                    print('get buf:' + buf)
                    raise e
                else:
                    failtime += 1
                    continue

    def req_recv(self, command):
        result = None
        # chance = 10
        # try:
        self.sendMsg(command)
        # while chance:
        #     try:
        try:
            result = self.recvMsg()
        except:
            raise Exception('cmd:' + command + ' error')
        #     raise Exception('no result')
        if result != None:
            return result
        if result == '':
            raise Exception('no result')

    # TODO change the recvData driver
    def recvData(self, tm, flag, transport):
        buf = ''
        size = 4096
        t = int(tm / (self.timeout * 1000))
        failtime = 0
        while True:
            try:
                buf += self._session.recv(size)
            except Exception as e:
                if failtime >= t:
                    self.disconnect()
                    print(e)
                    raise Exception("Time Out")
                else:
                    failtime += 1
                    if flag in buf and buf != "":
                        self.disconnect()
                        return buf
                    transport.check_heartbeat()

    def clear_buf(self):
        # self._session.close()
        # cfg = self.cfg
        # self.__init__(cfg)
        buf = ''
        size = 1024 * 10
        failtime = 0
        while True:
            try:
                buf = self._session.recv(size)
                if buf == "":
                    return True
            except Exception:
                if failtime >= 5:
                    self.disconnect()
                    return False
                else:
                    failtime += 1
                    if buf == "":
                        self.disconnect()
                        return True

    def recv_bin(self, length, driver):
        if self.status != True:
            # print('reconnect')
            self.connect()
        buf = ''
        size = 4096
        failtime = 0
        # self.clear_buf()
        # self._session.shutdown('SHUT_RDWR')
        msg = driver.req_recv('>AUDIO_RAW_DATA(16384)\r\n')
        # print(msg)
        # time.sleep()
        while len(buf) < length * 4:
            try:
                buf += self._session.recv(size)
            except Exception as e:
                failtime += 1
                # print(len(buf))
                # print(e)
                time.sleep(0.5)
                if failtime > 100:
                    self.disconnect()
                    raise Exception('time out')
        bufSize = len(buf)
        print(bufSize)
        data = struct.unpack('>' + 'f' * (bufSize / 4), buf)
        if bufSize / 4 > length or bufSize / 4 < length:
            with open(str(bufSize) + '.txt', 'a') as f:
                f.write(buf)
        # self._session.shutdown(socket.SHUT_RDWR)
        # self.close()
        return data

    def close(self):
        self._session.close()
        self.status = False

    def send_cmd(self, command, **kwargs):
        bRet = True
        if not self.status:
            bRet = self.connect()
        if self.status and bRet:
            command += self.endStr
            # self.log('send:' + command)
            #s = self._session.send(command)
            # print "zynq cmd :-->>> [{}{}]{}".format(self.uut,self.uut,command)
            s = self._session.send(command)
            if s <= 0:
                bRet = False
        return bRet

    def recv_result(self, tm=1000):
        bRet = True
        strRet = ""
        buf = ''
        size = 1024
        t = int(tm / (0.5 * 1000))
        failtime = 0
        while True:
            try:

                rev = self._session.recv(size)
                buf += rev
                time.sleep(0.01)
                if buf[-1] == "\n" and buf != "":
                    #self.disconnect()
                    # self.log('recv: %s' % buf)
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
        print "Agilent rev :-->>> {}".format(strRet)
        return bRet,strRet



    def send_recv(self, command,ntimeout=500):
        self.send_cmd(command)
        self.m_objBTime.Delay(30)
        bRet,strRet= self.recv_result(ntimeout)
        return strRet

    def instru_ctrl(self,strCommand,strParam1="",strParam2="",timeout=300):
        strRet = self.send_recv(strCommand,timeout)
        if "ERR" in strRet:
            strRet=""
        return strRet

    def Agilent34410_ReadVolt(self,par):
        agilent_voltage_auto_range_cmd = "MEAS:VOLT:DC?"
        agilent_voltage_1V_range_cmd = "MEAS:VOLT:DC? 1,0.0000001"
        agilent_voltage_cmd = "MEAS:VOLT:DC?"
        if "ONE" in str.upper(par):
            agilent_voltage_cmd = agilent_voltage_1V_range_cmd
        elif "AUTO" in str.upper(par):
            agilent_voltage_cmd = agilent_voltage_auto_range_cmd
        else:
            agilent_voltage_cmd = agilent_voltage_cmd
        self.send_cmd(agilent_voltage_cmd)
        self.m_objBTime.Delay(100)
        bRet,strRet = self.recv_result()
        strRet = strRet + ";"
        reg = "(.+);"
        result = self.m_objBRe.MatchStr_b_list(strRet,reg)
        return result


    def Aglent34410_ReadRes(self):
        pass
    def Aglent34410_ReadCurrent(self,par):
        agilent_current_ua_range_cmd = "MEAS:CURR:DC? 0.01, 0.000000001"
        # <10mA
        agilent_current_ma_range_cmd = "MEAS:CURR:DC? 1,0.000001"
        # <10A
        agilent_current_cmd = "MEAS:CURR:DC?"
        if "UA" in str.upper(par):
            agilent_current_cmd = agilent_current_ua_range_cmd
        elif "MA" in str.upper(par):
            agilent_current_cmd = agilent_current_ma_range_cmd
        else:
            agilent_current_cmd = agilent_current_cmd
        self.send_cmd(agilent_current_cmd)
        self.m_objBTime.Delay(100)
        bRet,strRet = self.recv_result()
        strRet = strRet + ";"
        reg = "(.+);"
        result = self.m_objBRe.MatchStr_b_list(strRet,reg)
        return result
    def listtostr(self,setlist,measlist,flag):
        strRet = ""
        for i in range(0,len(setlist)):
            strRet = strRet+",{},{}".format(setlist[i],measlist[i])
            if flag != "":
                strRet = strRet + ",{},{}\r\n".format((setlist[i]-measlist[i]),((setlist[i]-measlist[i])/measlist[i]*100))
            else:
                strRet = strRet + ",\r\n"
        return strRet




    def Sum_Average(self,listValue,listlen):
        value = 0
        for i in range(0,listlen):
            value = value + listValue[i]
        value = float(value/len(listValue))
        return  value

    def Squre_sum(self,listValue,listlen):
        value = 0
        for i in range(0,listlen):
            value = value + listValue[i] * listValue[i]
        return value

    def X_Y_By(self,X,Y,listlen):
        value = 0
        for i in range(0,listlen):
            value = value + X[i] * Y[i]
        return value

    def calfac(self,X,Y):
        if X and Y:
            return float(Y)/float(X)
        elif X == None:
            return "Get a nil X"
        elif Y == None:
            return "Get a nil Y"




    def Linear_Fit(self,X,Y):
        gain = 0
        offset = 0
        listlen = 0
        if len(X) >= len(Y):
            listlen = len(Y)
        elif len(Y) > len(X):
            listlen = len(X)
        x_ave = self.Sum_Average(X,listlen)
        y_ave = self.Sum_Average(Y,listlen)
        x_square = float(self.Squre_sum(X,listlen))
        x_y_multiply = float(self.X_Y_By(X,Y,listlen))
        gain = float((x_y_multiply - listlen * x_ave * y_ave)/(x_square - listlen * x_ave * x_ave))
        offset = float(y_ave - gain * x_ave)
        return gain,offset

    def read_fix_id(self):
        cmd = "eeprom string read(translation,cat08,0x020,17)"
        self.fix_id = self.objzynq.cmd_raw_send(cmd)
        print 'fix_id is : {}'.format(self.fix_id)
        # self.fix_id = re.sub("ÿ","",self.fix_id)
        self.fix_id = self.m_objBRe.MatchStr_b_list(self.fix_id,"ACK\s*\((.+?);")
        return self.fix_id


    @public('eload_cal')
    def eload_cal(self,*args,**kwargs):
        testpoint = args[0]
        bRet,listRet = self.m_objBRe.MatchStr_b_list(testpoint,"(.+?)_(.+?)")
        if bRet and len(listRet)==1:
            system_cal_type = listRet[0][0]
            channel = listRet[0][1]
        cal_spec = args[1]
        bRet, listRet = self.m_objBRe.MatchStr_b_list(cal_spec, "(.+?)_(.+?)_(.+)")
        if bRet and len(listRet)==1:
            st = float(listRet[0][0])
            ed = float(listRet[0][1])
            stp = float(listRet[0][2])
        if "ELOAD" in system_cal_type:
            return self.system_eload_cal_table(self,testpoint = testpoint,system_cal_type = system_cal_type,channel = channel,st = st,ed =ed,stp = stp)
        elif "ILOAD" in system_cal_type:
            return self.system_iload_cal_table(self,testpoint = testpoint,system_cal_type = system_cal_type,channel = channel,st = st,ed =ed,stp = stp)
        else:
            return "ERROR SEQUENCE PARAMETER"


    def set_eload_c(self,vol,channel):
        if "A" in channel or "1" in channel:
            DAC = 1
        elif "B" in channel or "2" in channel:
            DAC = 2
        elif "C" in channel or "2" in channel:
            DAC = 3
        elif "D" in channel or "2" in channel:
            DAC = 4
        dac_set = (self.eload_res_set * vol * 1000 +(1.21*24.75))/self.eload_dac_amp
        eload_cmd = "eload dac ref(1,ch{}={})".format(DAC,dac_set)
        print "send eload cmd>>>>>>>>>>{}".format(eload_cmd)
        self.objzynq.cmd_raw_send(eload_cmd)

    def savestr(self,filepath,filename,datastr):
        if os.path.exists(filepath):
            f = file(filename, "a+")
            f.write(datastr)
        else:
            os.makedirs(filepath)
            f = file(filename, "a+")
            f.write(datastr)
        f.close()



    def system_eload_cal_table(self,*args,**kwargs):
        Set_Cur_Bf_List = []
        Agilent_Cur_Bf_List = []
        Set_Cur_Af_List = []
        Agilent_Cur_Af_List = []
        Agilent_Cur = 0
        current_set = 0
        diff_data = 0
        st = float(kwargs["st"])
        ed = float(kwargs["ed"])
        stp = float(kwargs["stp"])
        channel = kwargs["channel"]
        testpoint = kwargs["testpoint"]

        dictRelayTable = self.objzynq.io_table.get("RelayTable")
        self.objzynq.cmd_raw_send(dictRelayTable.get("CURRENT_CAL_CTRL").get(testpoint)[0])
        vol_list =numpy.arange(st,ed,stp)
        for vol in range(0,len(vol_list)):
            self.set_eload_c(vol,channel)
            self.m_objBTime.delay(300)
            Agilent_Cur = float(self.Aglent34410_ReadCurrent())
            if Agilent_Cur != "":
                print (">>>>>>>>>>>>>>>>ELOAD SET BEFORE CAL : {}<<<<<<<<<<<<<<<<<<".format(testpoint))
                print (">>>>>>>>>>>>>>>>AGILENT READ BEFORE CAL : {}<<<<<<<<<<<<<<<<<<".format(testpoint))
                Set_Cur_Bf_List.append(vol)
                Agilent_Cur_Bf_List.append(Agilent_Cur)
        self.objzynq.cmd_raw_send("eload dac ref(4,ch1=0,ch2=0,ch3=0,ch4=0)")
        gain,offset = self.Linear_Fit(Agilent_Cur_Bf_List,Set_Cur_Bf_List)

        for vol in range(0, len(vol_list)):
            current_set = vol
            vol = vol * gain + offset
            self.set_eload_c(vol, channel)
            self.m_objBTime.delay(300)
            Agilent_Cur = float(self.Aglent34410_ReadCurrent())
            if Agilent_Cur != "":
                print (">>>>>>>>>>>>>>>>ELOAD SET AFTER CAL : {}<<<<<<<<<<<<<<<<<<".format(testpoint))
                print (">>>>>>>>>>>>>>>>AGILENT READ AFTER CAL : {}<<<<<<<<<<<<<<<<<<".format(testpoint))
                Set_Cur_Af_List.append(vol)
                Agilent_Cur_Af_List.append(Agilent_Cur)
            else:
                return "Agilent measure is nil"
            self.m_objBTime.delay(300)
            if(abs(current_set - Agilent_Cur) > current_set * 0.01):
                diff_data = diff_data +1
        self.objzynq.cmd_raw_send("eload dac ref(4,ch1=0,ch2=0,ch3=0,ch4=0)")
        self.objzynq.cmd_raw_send(dictRelayTable.get("CURRENT_CAL_CTRL").get("DISCONNECT")[0])

        # timenow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

        filepath = "/vault/PRM_CAL/{}".format(self.fix_id)
        filename = "/vault/PRM_CAL/Calbrition_{}/{}_{}.csv".format(self.fix_id, self.cfg['id'], testpoint)
        datastr = "testpoint,gain,offset\r\n"
        datastr = datastr + "{},{},{}\r\n".format(testpoint,gain,offset)
        datastr = datastr + "Before RawData:,measure(A),agilent(A),measure-agilent(A),Error(%)\r\n"
        datastr = datastr + self.listtostr(Set_Cur_Bf_List,Agilent_Cur_Bf_List,1)

        datastr = datastr + "After RawData:,measure(A),agilent(A),measure-agilent(A),Error(%)\r\n"
        datastr = datastr + self.listtostr(Set_Cur_Af_List,Agilent_Cur_Af_List,1)
        self.savestr(filepath,filename,datastr)
        if diff_data == 0:
            return "--PASS--"
        else:
            return "--FAIL--OUT OF LIMIT(1%) COUNT: {}".format(diff_data)



    def system_iload_cal_table(self,*args,**kwargs):
        DMM_Cur_Bf_List = []
        Agilent_Cur_Bf_List = []
        DMM_Cur_Af_List = []
        Agilent_Cur_Af_List = []
        Agilent_Cur = 0
        Iload_Cur = 0
        diff_data = 0
        st = float(kwargs["st"])
        ed = float(kwargs["ed"])
        stp = float(kwargs["stp"])
        channel = kwargs["channel"]
        testpoint = kwargs["testpoint"]

        dictRelayTable = self.objzynq.io_table.get("RelayTable")
        self.objzynq.cmd_raw_send(dictRelayTable.get("CURRENT_CAL_CTRL").get(testpoint)[0])
        vol_list =numpy.arange(st,ed,stp)
        for vol in range(0,len(vol_list)):
            self.set_eload_c(vol,channel)
            self.m_objBTime.delay(300)
            Agilent_Cur = float(self.Aglent34410_ReadCurrent())
            if Agilent_Cur != "":
                print (">>>>>>>>>>>>>>>>ELOAD SET BEFORE CAL : {}<<<<<<<<<<<<<<<<<<".format(testpoint))
                print (">>>>>>>>>>>>>>>>AGILENT READ BEFORE CAL : {}<<<<<<<<<<<<<<<<<<".format(testpoint))

            else:
                return "Agilent measure is nil"
            result = self.objzynq.dmmvoltage(testpoint)
            print "debug1_cal{},eload_hw_gain:{},eload_res_read:{}".format(result,self.eload_dac_amp,self.eload_res_read)
            Iload_Cur = ((float(result)/self.eload_hw_gain)/self.eload_res_read/1000)

            print(">>>>>>>>>>>>>>>>>DMM CAL BEFORE READ:{}: {}<<<<<<<<<<<<<<<<<<<".format(testpoint,Iload_Cur))
            print(">>>>>>>>>>>>>>>>>Agilent CAL BEFORE READ:{}: {}<<<<<<<<<<<<<<<<<<<".format(testpoint,Agilent_Cur))

            DMM_Cur_Bf_List.append(Iload_Cur)
            Agilent_Cur_Bf_List.append(Agilent_Cur)

        gain,offset = self.Linear_Fit(Agilent_Cur_Bf_List,DMM_Cur_Bf_List)

        for vol in range(0, len(vol_list)):
            # current_set = vol
            # vol = vol * gain + offset
            self.set_eload_c(vol, channel)
            self.m_objBTime.delay(300)

            Agilent_Cur = float(self.Aglent34410_ReadCurrent())
            result = self.objzynq.dmmvoltage(testpoint)
            print "debug2_cal{},eload_hw_gain:{},eload_res_read:{}".format(result, self.eload_dac_amp,self.eload_res_read)
            Iload_Cur = ((float(result)/self.eload_hw_gain)/self.eload_res_read/1000)
            Iload_Cur_After = Iload_Cur * gain +offset
            print(">>>>>>>>>>>>>>>>>DMM CAL AFTER READ:{}: {}<<<<<<<<<<<<<<<<<<<".format(testpoint, Iload_Cur_After))
            print(">>>>>>>>>>>>>>>>>Agilent CAL BEFORE READ:{}: {}<<<<<<<<<<<<<<<<<<<".format(testpoint, Agilent_Cur))
            DMM_Cur_Af_List.append(Iload_Cur_After)
            Agilent_Cur_Af_List.append(Agilent_Cur)

            self.m_objBTime.delay(300)
            if(abs(Iload_Cur_After - Agilent_Cur) > Iload_Cur_After * 0.01):
                diff_data = diff_data +1
        self.objzynq.cmd_raw_send("eload dac ref(4,ch1=0,ch2=0,ch3=0,ch4=0)")
        self.objzynq.cmd_raw_send(dictRelayTable.get("CURRENT_CAL_CTRL").get("DISCONNECT")[0])

        # timenow = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        filepath = "/vault/PRM_CAL/{}".format(self.fix_id)
        filename = "/vault/PRM_CAL/Calbrition_{}/{}_{}.csv".format(self.fix_id, self.cfg['id'], testpoint)
        datastr = "testpoint,gain,offset\r\n"
        datastr = datastr + "{},{},{}\r\n".format(testpoint,gain,offset)
        datastr = datastr + "Before RawData:,measure(A),agilent(A),measure-agilent(A),Error(%)\r\n"
        datastr = datastr + self.listtostr(DMM_Cur_Bf_List,Agilent_Cur_Bf_List,1)

        datastr = datastr + "After RawData:,measure(A),agilent(A),measure-agilent(A),Error(%)\r\n"
        datastr = datastr + self.listtostr(DMM_Cur_Af_List,Agilent_Cur_Af_List,1)
        self.savestr(filepath,filename,datastr)
        if diff_data == 0:
            return "--PASS--"
        else:
            return "--FAIL--OUT OF LIMIT(1%) COUNT: {}".format(diff_data)

    @public('signalwritefactortoarm')
    def signalwritefactortoarm(self,*args,**kwargs):
        len = 0x01
        addr = None
        redata = 0
        result = 0
        test_vt = {}

        testpoint = args[0]
        if "ELOAD" in testpoint or "ILOAD" in testpoint:
            test_vt = self.calibrition_table.get('ELOAD_CAL')

        elif "PPVBAT_G3H_CURRENT" in testpoint or "PPVBAT_G3H_VOLTAGE" in testpoint or "PPDCIN_G3H_CURRENT" in testpoint:
            test_vt = self.calibrition_table.get('DATALOGGER_CAL')

        elif "PP12V_G3H_ACDC_" in testpoint:
            test_vt = self.calibrition_table.get('DATALOGGER_826_CAL')

        else:
            keyword = re.findall("(.+)_(.+)",testpoint)
            test_vt = self.calibrition_table.get('ELOAD_CAL')  # no use

        print("test_vt is :{},testpoint is :{}".format(test_vt,testpoint))
        for i in test_vt:
            if i == testpoint:
                addr = self.calibrition_table.get('ELOAD_CAL').get(testpoint)

        # factorfile = ""
        # testcount = 0
        factorlist = []
        # filepath = "/vault/PRM_CAL/Calibrition_{}/{}_{}_data.csv".format(self.fix_id,self.cfg['id'],testpoint)
        filepath = "/vault/PRM_CAL/Calbrition_{}/{}_{}.csv".format(self.fix_id, self.cfg['id'], testpoint)
        csv_reader = csv.reader(open(filepath))
        for lines in csv_reader:
            print "'testpoint is :'{},'gain is :'{},'offset is :'{}".format(lines[0],lines[1],lines[2])
            if lines[0] == testpoint:
                factorlist[0] = lines[1]
                factorlist[1] = lines[2]
                result = self.writefactortoarmsub(factorlist,addr)
                if result == 0:
                    return "--PASS--"
                else:
                    return result

    def writefactortoarmsub(self,factorlist,addr):
        len = 0
        flag = 1
        length = 4
        numstr = ""
        dataflag = 0
        write_factor_board_name = "translation"
        if len(factorlist) < 1:
            return 'not found factorlist'
        print "factrolist[0] is {},factrolist[1] is {},factrolist[2] is {},".format(factorlist[0],factorlist[1],factorlist[2])
        self.ctrlfaceeprom(addr,"0x01")
        numstr = "01,00,00,00"
        addr = int(addr,16)
        addr = hex(addr+len)
        flagcmd = "eeprom write({},cat08,{},{},{})".format(write_factor_board_name,addr,length,numstr)
        print "flagcmd is {}".format(flagcmd)
        flagcmd2 = "eeprom write(testbase,cat08,{},{},{})".format(addr,length,numstr)
        print "flagcmd2 is {}".format(flagcmd2)
        result = self.objzynq.cmd_raw_send(flagcmd)
        print "eeprom result :{}".format(result)
        result2 = self.objzynq.cmd_raw_send(flagcmd2)
        print "eeprom result2 :{}".format(result2)
        if "DONE" not in result and "DONE" not in result2:
            dataflag = dataflag +1
        len = len + 4
        for i in range(0,len(factorlist)):
            hexstr = "0x{}".format(struct.pack("<f", float(factorlist[i])).encode('hex'))
            numstr = "{},{},{},{}".format(hexstr[8:],hexstr[6:8],hexstr[4:6],hexstr[2:4])
            print "numstr is :{}".format(numstr)
            addr = int(addr,16)
            addr = hex(addr+len)

            flagcmd = "eeprom write({},cat08,{},{},{})".format(write_factor_board_name,addr + len,length,numstr)
            print "flagcmd is {}".format(flagcmd)
            flagcmd2 = "eeprom write(testbase,cat08,{},{},{})".format(addr + len,length,numstr)
            print "flagcmd2 is {}".format(flagcmd2)
            result = self.objzynq.cmd_raw_send(flagcmd)
            print "eeprom result :{}".format(result)
            result2 = self.objzynq.cmd_raw_send(flagcmd2)
            print "eeprom result2 :{}".format(result2)
            len = len + 4
            if "DONE" in result:
                dataflag = dataflag + 2
            print "dataflag_{}".format(dataflag)
        return dataflag


    def ctrlfaceeprom(self,addr,length):
        datastr = ""
        length = int(length,16)
        for i in range(0,length):
            if i == length:
                datastr = datastr + "FF"
            else:
                datastr = datastr + "FF,"
        datalen = length
        print "addr is :{},daqtalen is :{},datastr is :{}".format(addr,datalen,datastr)
        ctrlcmd = "eeprom write(translation,cat08,{},{},{})".format(addr,datalen,datastr)
        ctrlcmd2 = "eeprom write(testbase,cat08,{},{},{})".format(addr,datalen,datastr)

        print "ctrlcmd is :{}".format(ctrlcmd)
        print "ctrlcmd2 is {}".format(ctrlcmd2)
        result = self.objzynq.cmd_raw_send(ctrlcmd)
        result2 = self.objzynq.cmd_raw_send(ctrlcmd2)

        print "result is :{}".format(result)
        print "result2 is :{}".format(result2)
        if "DONE" in result and "DONE" in result2:
            return 0
        else:
            return -1

    @public('readfactorfromarm')
    def readfactorfromarm(self, *args, **kwargs):
        VCfac = []
        addr = None
        cmd_temp = args[0]
        test_type = ""
        testpoint = ""
        if "ELOAD" in cmd_temp or "ILOAD" in cmd_temp:
            test_type = "ELOAD_CAL"
            testpoint = args[0]
        elif "PPVBAT_G3H_CURRENT" in cmd_temp or "PPVBAT_G3H_VOLTAGE" in cmd_temp or "PPDCIN_G3H_CURRENT" in cmd_temp:
            test_type = "DATALOGGER_CAL"
            testpoint = args[0]
        elif "PP12V_G3H_ACDC_" in cmd_temp:
            test_type = "DATALOGGER_826_CAL"
            testpoint = args[0]
        else:
            keyword = re.findall("(.+?)-(.+)",cmd_temp)
            test_type = keyword[0][0]
            testpoint = args[0]
        print("test_type is :{},testpoint is :{}".format(test_type,testpoint))
        index = args[1]
        test_dict = self.calibrition_table.get(test_type)
        count = len(test_dict)
        for i in test_dict:
            if i == testpoint:
                addr = test_dict.get(i)
        print "addr is :{}".format(addr)
        ktrtable = self.readfactorformarmsub(addr)
        if ktrtable == "":
            return "--FAIL--NO KTRTABLE"
        else:
            VCfac[0] = ktrtable[0]
            VCfac[1] = ktrtable[1]
            print "read gain is :{}".format(VCfac[0])
            print "read offset is :{}".format(VCfac[1])
        if index.upper() == "GAIN":
            return VCfac[0]
        elif index.upper() == "OFFSET":
            return VCfac[1]
        else:
            return "--FAIL-- NEED PARAM 2"

    def string_split(self,str,char):
        sub_str_list = []
        while True:
            pos = str.find(char)
            if pos == -1:
                sub_str_list.append(str)
                break
            sub_str = str[0:pos]
            sub_str_list.append(sub_str)
            str = str[pos+1:len(str)]
        return sub_str_list


    def readfactorformarmsub(self,addr):
        len = 0
        length =4
        recivestr = ""
        recivestr2 = ""
        read_factor_board_name = "translation"
        addr = int(addr,16)
        addr = hex(addr + len)
        flagcmd = "eeprom read({},cat08,{},{})".format(read_factor_board_name,addr,length)
        flagcmd2 = "eeprom read(testbase,cat08,{},{})".format(addr,length)
        recivestr = self.objzynq.cmd_raw_send(flagcmd)
        recivestr2 = self.objzynq.cmd_raw_send(flagcmd2)
        print "recive str is {}".format(recivestr)
        print "recive str2 is {}".format(recivestr2)
        if "ACK" not in recivestr or "ACK" not in recivestr2:
            return "{},{}".format(recivestr,recivestr2)
        if "ERR" in recivestr or "ERR" in recivestr2:
            return -3
        reg = "ACK\s*\((.+?);"
        recivestr = self.m_objBRe.MatchStr_b_list(recivestr,reg)
        recivestr2 = self.m_objBRe.MatchStr_b_list(recivestr2,reg)

        if str(recivestr) != str(recivestr2):
            print "translation board and testbase board calibration data is difference!"
        strlist = self.string_split(recivestr,",")
        strlist2 = self.string_split(recivestr2, ",")
        flagcmd = "0x{}{}{}{}".format("%2X" % int(strlist[3],16),"%2X" % int(strlist[2],16),"%2X" % int(strlist[1],16),"%2X" % int(strlist[0],16))
        flagcmd2 = "0x{}{}{}{}".format("%2X" % int(strlist2[3],16),"%2X" % int(strlist2[2],16),"%2X" % int(strlist2[1],16),"%2X" % int(strlist2[0],16))
        if "0x00000001" in flagcmd and "0x00000001" in flagcmd2:
            krt = []
            krt2 = []
            for i in range(1,2):
                len = len+4
                flagcmd = "eeprom read({},cat08,{},{})".format(read_factor_board_name,hex(int(addr,16)+len),length)
                flagcmd2 = "eeprom read(testbase,cat08,{},{}".format(hex(int(addr,16)+len),length)
                recivestr = self.objzynq.cmd_raw_send(flagcmd)
                recivestr2 = self.objzynq.cmd_raw_send(flagcmd2)
                if "ACK" not in recivestr and "ACK" not in recivestr2:
                    return recivestr
                if "ERR" in recivestr or "ERR" in recivestr2:
                    return "ERR response:{}------{}".format(recivestr,recivestr2)
                reg = "ACK\s*\((.+?);"
                recivestr = self.m_objBRe.MatchStr_b_list(recivestr,reg)
                recivestr2 = self.m_objBRe.MatchStr_b_list(recivestr2,reg)
                strlist = self.string_split(recivestr,",")
                strlist2 = self.string_split(recivestr2,",")
                krt[i] = strlist
                krt2[i] = strlist2
            factlist = [krt[1],krt[2]]
            return factlist
        else:
            return "can't find calibration flag!"

    def arraywritefactortoarm(self,*args,**kwargs):
        length = 0x10
        addr = None
        redata = 0
        result = 0
        factorlist = []
        test_vt = []
        testp_count = 0
        Test_type = str(args[0])
        TestPoint_Count = len(self.calibrition_table.get(Test_type))
        test_vt = self.calibrition_table.get(Test_type)
        for i in test_vt:
            testpoint = i
            addr = test_vt[i]
            print "$$$$$.{}".format(addr)
            print "^^^^^^^.{}".format(testpoint)
            filepath = "/vault/PRM_CAL/Calbrition_{}/{}_{}.csv".format(self.fix_id, self.cfg['id'], testpoint)
            csv_reader = csv.reader(open(filepath))
            for lines in csv_reader:
                print "'testpoint is :'{},'gain is :'{},'offset is :'{}".format(lines[0], lines[1], lines[2])
                if lines[0] == testpoint:
                    factorlist[0] = lines[1]
                    factorlist[1] = lines[2]
                    result = self.writefactortoarmsub(factorlist,addr)
                    if result == 0:
                        break
                    else:
                        return result
        return "--PASS--"

    def diff_relay(self,Test_type,Test_name,i,k):
        IU = "V"
        if "VOL_860_VT" in Test_type:
            testpoint = i
        self.objzynq.cmd_raw_send(self.objzynq.io_table.get("RelayTable").get("PPVBAT_EN").get(Test_name))
        self.objzynq.cmd_raw_send(self.objzynq.io_table.get("RelayTable").get("VLOTAGE_CAL_CTRL").get(testpoint))
        # else:
        #     return "--FAIL-- please cheack param !!!"
        return testpoint,IU


    @public('voltage_cal')
    def voltage_cal(self,*args,**kwargs):
        Test_type = args[0]
        bit_control = args[1]
        diffdata = 0
        DMM_Volt = None
        Agilent_Voltage = None
        test_rawdata_before_table = []
        test_rawdata_after_table = []
        Agilent_Vol_before_table = []
        DMM_Vol_before_table = []
        Agilent_Vol_after_table = []
        DMM_Vol_after_table = []
        TestPoint_Gain_Tab = []
        rawdata_data_before_show = ''
        rawdata_data_after_show = ''
        out_limit_show = ''
        count_show = ''
        factor_show = ''
        fail_count = ''
        testpoint = ''
        Test_name = ''
        gain = 1
        offset = 0
        count = 0

        #-----------------before cal-------------------

        for i in self.calibrition_table.get(Test_type):
            print "{}-times".format(i)
            for k in range(0,len(self.calibrition_table.get(bit_control))):
                Test_name = self.calibrition_table.get(bit_control)[k]
                testpoint,IU = self.diff_relay(Test_type,Test_name,i,k)
                self.m_objBTime.Delay(500)
                print "testpoint is :{}".format(testpoint)
                DMM_Volt = self.objzynq.dmmvoltage(testpoint,unit=IU)
                print "-------DMM  Cal  before  read :DMM_Volt is :{}".format(DMM_Volt)
                Agilent_Voltage = self.Agilent34410_ReadVolt("AUTO")
                print "------Agilent Cal before read: Agilent_Voltage is :{}".format(Agilent_Voltage)
                DMM_Vol_before_table.append(DMM_Volt)
                Agilent_Vol_before_table.append(Agilent_Voltage)
            if "860" in Test_type:
                self.objzynq.cmd_raw_send(self.objzynq.io_table.get("RelayTable").get("VOLTAGE_CAL_CTRL").get("DISCONNECT"))
            if "VOL_860_SIP_VT" in Test_type:
                print "DMM_Vol_before_table is :{}".format(DMM_Vol_before_table)
                print "Agilent_Vol_before_table is :{}".format(Agilent_Vol_before_table)
                gain = self.calfac(DMM_Volt,Agilent_Voltage)
                offset = 0
            else:
                gain,offset = self.Linear_Fit(DMM_Vol_before_table,Agilent_Vol_before_table)
            TestPoint_Gain_Tab.append(gain)
            TestPoint_Gain_Tab.append(offset)
            factor_show = "{}{},{},{}\r\n".format(factor_show,testpoint,gain,offset)
            test_rawdata_before_table.append(self.listtostr(DMM_Vol_before_table,Agilent_Vol_before_table))
            rawdata_data_before_show = "{}{}:{}".format(rawdata_data_before_show,testpoint,test_rawdata_before_table)
            print "rawdata_data_before_show:{}".format(rawdata_data_before_show)
            DMM_Vol_before_table = []
            Agilent_Vol_before_table = []

        # -------------------after cal-------------------------
        for i in self.calibrition_table.get(Test_type):
            count = count +1
            print "after cal{}-times".format(i)
            for k in range(0,len(self.calibrition_table.get(bit_control))):
                Test_name = self.calibrition_table.get(bit_control)[k]
                testpoint,IU = self.diff_relay(Test_type,Test_name,i,k)
                self.m_objBTime.Delay(500)
                print "after caltestpoint is :{}".format(testpoint)
                DMM_Volt = self.objzynq.dmmvoltage(testpoint,unit=IU)
                DMM_Volt_after = DMM_Volt * TestPoint_Gain_Tab[count*2-1] + TestPoint_Gain_Tab[count*2]
                print "after cal-------DMM  Cal  before  read :DMM_Volt is :{}".format(DMM_Volt_after)
                Agilent_Voltage = self.Agilent34410_ReadVolt("AUTO")
                print "after cal------Agilent Cal before read: Agilent_Voltage is :{}".format(Agilent_Voltage)
                DMM_Vol_after_table.append(DMM_Volt)
                Agilent_Vol_after_table.append(Agilent_Voltage)
                if abs(DMM_Volt_after-Agilent_Voltage) > Agilent_Voltage*0.001:
                    diffdata = diffdata + 1
                if diffdata > 0:
                    out_limit_show = "{}{}:{}\t".format(out_limit_show,testpoint,diffdata)

            if "860" in Test_type:
                self.objzynq.cmd_raw_send(self.objzynq.io_table.get("RelayTable").get("VOLTAGE_CAL_CTRL").get("DISCONNECT"))
            test_rawdata_after_table[count] = self.listtostr(DMM_Vol_after_table,Agilent_Vol_after_table,1)
            rawdata_data_after_show = "{}{}:{}".format(rawdata_data_after_show,testpoint,test_rawdata_after_table[count])

            print "after cal--rawdata_data_after_show:{}".format(rawdata_data_after_show)
            DMM_Vol_after_table = []
            Agilent_Vol_after_table = []

        filepath = "/vault/PRM_CAL/{}".format(self.fix_id)
        filename = "/vault/PRM_CAL/Calbrition_{}/{}_{}.csv".format(self.fix_id, self.cfg['id'], testpoint)
        datastr = "testpoint,gain,offset\r\n"
        datastr = "{}{}".format(datastr,factor_show)
        datastr = "{}{}".format(datastr,"Before RawData:,measure(V),agilent(V),measure-agilent(V),Error(%)\r\n")
        datastr = "{}{}".format(datastr,rawdata_data_before_show)
        datastr = "{}{}".format(datastr,"After RawData:,measure(V),agilent(V),measure-agilent(V),Error(%)\r\n")
        datastr = "{}{}".format(datastr,rawdata_data_after_show)
        self.savestr(filepath, filename, datastr)
        if diffdata > 0:
            return "--FAIL-- out of limit(0.1%) count : {}".format(out_limit_show)
        else:
            return "--PASS-- out of limit(0.1%) count : {}".format(diffdata)


    @property
    def getSocket(self):
        return self._session