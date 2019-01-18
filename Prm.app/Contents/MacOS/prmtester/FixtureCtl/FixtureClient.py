import zmq
from Common.tinyrpc.transports.zmq import ZmqClientTransport
from Common import zmqports

from Common.BBase import *

import time
import re
class FixtureClient(object):
    def __init__(self):
        self.req_timeout = 10000
        ctx = zmq.Context()
        self.sub = ctx.socket(zmq.SUB)
        self.sub.connect("tcp://127.0.0.1:" + str(zmqports.FIXTURE_CTRL_PUB))
        self.sub.setsockopt(zmq.SUBSCRIBE, "")

        self.req = ZmqClientTransport.create(ctx, "tcp://127.0.0.1:" + str(zmqports.FIXTURE_CTRL_PORT))

        self.loop_test_flg = False
        self.need_zmq_flg = True

        self.ObjLock =cBaseThreadLock()
    def CheckMotion(self,strMsg):
        print "Check strMsg {}".format(strMsg)
        bRet = False
        try :
            if "OK" in strMsg:
                bRet = True
            elif "NG" in strMsg or "ERROR" in strMsg:
                bRet = False
            else:
                pass
        except:
            bRet=False
        return bRet
    def CheckFans(self,nIndex,strInfo):
        strRet = ""
        listRet = []
        if strInfo:
            listRet = re.findall("FAN{} ([\S]+)".format(nIndex+1),strInfo)
            strRet =""
            if len(listRet) >0 :
                strRet = listRet[0]

        return strRet
    def CheckFansR(self,nIndex,strInfo):
        strRet = ""
        listRet = []
        if strInfo:


            listRet = re.findall("FANR{} ([\S]+)".format(nIndex+1),strInfo)
            strRet =""
            if len(listRet) >0 :
                strRet = listRet[0]

        return strRet
    def CheckFansL(self,nIndex,strInfo):
        strRet = ""
        listRet = []
        if strInfo:


            listRet = re.findall("FANL{} ([\S]+)".format(nIndex+1),strInfo)
            strRet =""
            if len(listRet) >0 :
                strRet = listRet[0]

        return strRet
    def CheckFansB(self,nIndex,strInfo):
        strRet = ""
        listRet = []
        if strInfo:
            listRet = re.findall("FANB{} ([\S]+)".format(nIndex+1),strInfo)
            strRet =""
            if len(listRet) >0 :
                strRet = listRet[0]
        return strRet
    def CheckSatus(self,strCmd):
        return self.CheckMotion(self.send_cmd("{} STATUS".format(strCmd)))

    def StartWithDutCheck(self):
        nRet = -1
        nInFlag = -1
        nDutStatusFlag = -1
        nDownFlag = -1
        nTryTime = 3
        
        self.CheckMotion(self.send_cmd("IN"))
        for i in range(0,nTryTime):
            time.sleep(1)
            if self.CheckSatus("IN"):
                nInFlag = 0
                time.sleep(3)
                break
        if nInFlag == 0:
            for i in range(0,nTryTime):
                time.sleep(1)
                if self.CheckSatus("DUT"):
                    nDutStatusFlag = 0
                    time.sleep(3)
                    break
        if nDutStatusFlag == 0 :
            self.CheckMotion(self.send_cmd("DOWN"))
            for i in range(0,nTryTime):
                time.sleep(1)
                if self.CheckSatus("DOWN"):
                    nDownFlag = 0
                    time.sleep(3)
                    break
        if nDownFlag ==0:
            self.send_cmd("TEST START")
            nRet =0
        return nRet

    def Start(self):
        while True:
            if self.CheckMotion(self.send_cmd("DUT STATUS")):
                time.sleep(3)
                break
        while True:
            if self.CheckMotion(self.send_cmd("IN")):
                time.sleep(3)
                break
        while True:
            if self.CheckMotion(self.send_cmd("DOWN")):
                time.sleep(3)
                break
        self.send_cmd("TEST START")
    def End(self):
        nRet = -1
        nUpFlag = -1
        nTryTime = 3
        self.CheckMotion(self.send_cmd("UP"))
        for i in range (0,nTryTime):
            time.sleep(1)
            if self.CheckSatus("UP"):
                nUpFlag = 0
                time.sleep(3)
                break
        if nUpFlag ==0:          
            self.send_cmd("TEST DONE")
            nRet = 0
        return nRet
    def EndWithOUT(self):
        nUpFlag = -1
        nOutFlag = -1
        nTryTime = 3
        nRet = -1
        self.CheckMotion(self.send_cmd("UP"))
        for i in range (0,nTryTime):
            time.sleep(1)
            if self.CheckSatus("UP"):
                nUpFlag = 0
                time.sleep(3)
                break
        if nUpFlag ==0:
            self.CheckMotion(self.send_cmd("OUT"))
            for i in range (0,nTryTime):
                time.sleep(1)
                if self.CheckSatus("OUT"):
                    nOutFlag = 0
                    time.sleep(3)
                    break
        if nOutFlag ==0:           
            self.send_cmd("TEST DONE")
            nRet = 0

        return nRet

    def send_cmd(self, cmd):
        self.ObjLock.Lock(True)
        strRet =  self.send_msg("S:"+cmd + "\r\n")
        self.ObjLock.Lock(False)
        return strRet

    def set_loop_test_flg(self, flg):
        self.loop_test_flg = flg

    def get_loop_test_flg(self):
        return self.loop_test_flg

    def set_need_zmq_flg(self, flg):
        self.need_zmq_flg = flg

    def get_need_zmq_flg(self):
        return self.need_zmq_flg

    def set_req_timeout(self, millisecs):
        self.req_timeout = millisecs

    def get_req_timeout(self):
        return self.req_timeout

    def send_msg(self, msg):
        #print ("msg send to fixture is:" + msg)

        if self.need_zmq_flg:
            try:
                resp = self.req.send_reply(msg)
            except Exception as e:
                return None
            #print ("msg received from fixture is: " + str(resp))
            return str(resp).strip()
        else:
            return None

    def close(self):
        return self.send_cmd("DOWN")

    def press(self):
        return True
        # self.send_cmd("DOWN")

    def release(self):
        print ("fixture loop mode is: " + str(self.loop_test_flg))
        if self.loop_test_flg:
            self.send_cmd("DOWN")
        else:
            self.send_cmd("UP")

    def wait_for_start(self):
        while True:
            reply_msg = self.send_cmd("UP STATUS")
            if "DOWN OK" in reply_msg:
                return True
            return False


if __name__ == '__main__':
    abc = FixtureClient()

    # abc.send_cmd("TEST DONE")
    # abc.send_cmd("DUT STATUS")

    print abc.send_cmd("SET CH1:0500")
    print abc.send_cmd("READ CH1")




