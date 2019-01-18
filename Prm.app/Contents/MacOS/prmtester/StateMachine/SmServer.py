
import logging
import zmq
import inspect
import traceback
import os
import re
import time
import sys
if not __package__:
    path = os.path.join(os.path.dirname(__file__), os.pardir)
    sys.path.insert(0, path)
from Common import zmqports
from Common.tinyrpc.dispatch import RPCDispatcher, public
from Common.tinyrpc.proxy import SequencerProxy
from Common.tinyrpc.exc import *
from Common.tinyrpc.protocols.StateMachineRpc import *
from Common.tinyrpc.protocols.jsonrpc import *

from Common.BBase import *
from FixtureSM import FixtureSM
from Driver import SerialDriver



from TestEngine.Driver.DriverManager import *

from FixtureCtl.FixtureClient import FixtureClient

from Log.LogClient import LogClient
class Uut(object):
    def __init__(self, ctx, publisher, uutNum):
        self.flag = False
        self.uutEnable = not self.flag
        self.uutSN = ""
        self.uutNum = uutNum

        logging.info("Begin init uut:%d", uutNum)

        addr = "tcp://127.0.0.1:" + str(int(zmqports.SEQUENCER_PUB) + uutNum)
        logging.info("SM receive sequencer SUB at addr: %s", addr)
        self.seqSub = ctx.socket(zmq.SUB)
        self.seqSub.connect(addr)
        self.seqSub.setsockopt(zmq.SUBSCRIBE, "")

        self.seqSub.setsockopt(zmq.RCVHWM,0)
        
        addr = "tcp://127.0.0.1:" + str(int(zmqports.SEQUENCER_PORT) + uutNum)
        logging.info("SM zmq REQ at addr: %s", addr)
        
        self.seqReq = SequencerProxy(uutNum, publisher, ctx=ctx, retries=1)
        
        
    def getUutSN(self):
        return self.uutSN
      
    def setUutSN(self, SN):
        self.uutSN = SN
        
    def getUutFlag(self):
        return self.flag
      
    def setUutFlag(self, flag):
        self.flag = flag 

    def getUutEnableFlag(self):
        return self.uutEnable
      
    def setUutEnableFlag(self, flag):
        self.uutEnable = flag  
        
    def getSeqReq(self):
        return self.seqReq 
    
    def getSeqSub(self):
        return self.seqSub 

from Common.BBase import *




from multiprocessing import Process
import os

g_objSM = None

def StartAutoProcess(objStateMachine):
    while objStateMachine.bAutoRuning:
        objStateMachine.AutoStart()





class cAutoTestThread(threading.Thread):
    def __init__(self,StateMachine =None,Frequence=2000):
        super(cAutoTestThread, self).__init__()
        self.objTimer = cBruceTime()
        self.objStateMachine = StateMachine
        self.nFrequence = Frequence


    def Stop(self):
        self.bRun = False


    def run(self):
        self.bRun = True
        self.objStateMachine.CheckOutFinish()
        while self.bRun:
            try:
                if self.objStateMachine.AutoStart():
                    pass
            except Exception as e:
                pass
            self.objTimer.Delay(self.nFrequence)

class StateMachine(RPCDispatcher):
    def __init__(self, ctx, publisher, slots,sequencers):
        super(StateMachine, self).__init__()
        self.objLog = LogClient("StateMachine", "StateMachine.log")
        self.currentLoopTimes = 0
        self.totalLoopTimes = 1
        self.testingFlag = False
        self.bTestingFlag = False
        self.publisher = publisher
        self.stopLoopFlag = True
        self.sequencers = sequencers
        self.uuts = []
        
        for uutNum in xrange(slots):
            self.uuts.append(Uut(ctx, publisher, uutNum))
        #ser = SerialDriver(ser=config)
        self.fixtureSM = FixtureSM(SerialDriver(), publisher)
        self.fixture = FixtureClient()
        
        self.DummyCheckobjs=None
        self.CreateRealCheckObj()


        self.UUtInfos=[{'uutNum': 0, 'SN': None}, {'uutNum': 1, 'SN': None}, {'uutNum': 2, 'SN': None}, {'uutNum': 3, 'SN': None}]




        #self.objSMlog=LogClient("SM","Flow.log")

        self.objSMconfig=cBruceConfig("./Config/SM.json")

        
        self.FixtureMode = 0
        self.FixtureMode = self.objSMconfig.GetConfig("AutoMode")


        self.bOutFlagOpen = -1

        self.objAutoStartThread =cAutoTestThread(self,2000)

        self.bAutoThreadFlag=0

        self.bAutoTestStart=-1

        self.bAutoRuning = 1

        g_objSM = self

        self.objAutoStartThread.start()
        self.bAutoThreadFlag = 1



    def CreateRealCheckObj(self):
        if self.DummyCheckobjs == None:
            self.DummyCheckobjs = DriverManager().CreateZynqDrivers()

    def checkAllFlag(self):
        for uut in self.uuts:
            if uut.getUutEnableFlag() and uut.getUutFlag() == False:
                return False
        return True
     
     
    def clearAllFlag(self):
        for uut in self.uuts:
            if uut.getUutEnableFlag():
                uut.setUutFlag(False)
        return True
    
    
    def clearAllSN(self):
        for uut in self.uuts:
            uut.setUutSN("")
        return True
    
         
    def get_seq_subs(self):
        subSocks = []
        for uut in self.uuts:
            subSocks.append(uut.seqSub)
        return subSocks
    
    
    def deal_with_sub(self, socks):
        for sock in socks:
            if socks.get(sock) != zmq.POLLIN or sock not in self.get_seq_subs():
                continue
            uut = None
            for item in self.uuts:
                if item.getSeqSub() == sock:
                    uut = item
                    break
            if uut == None:
                continue
            msg = sock.recv()
            #self.objLog.Trace("Sub Message Start {}".format(msg))
            if re.search(r"\"event\"\s*:\s*1", msg) != None:
                logging.info("SM recv sub mesg:%s", msg)
                uut.setUutFlag(True)

                self.objLog.Trace("Sub AllFinish  Start {}".format(self.checkAllFlag()))
                if self.checkAllFlag():
                    self.objLog.Trace("AllFinish  Start 1")
                    self.fixtureSM.state_switch(FixtureSM.EVENT["FINISH"])
                    self.fixtureSM.state_switch(FixtureSM.EVENT["WILL_UNLOAD"])
                    self.fixtureSM.state_switch(FixtureSM.EVENT["REMOVED"])
                    self.objLog.Trace("AllFinish  Start 2")


                    self.clearAllFlag()

                    self.objLog.Trace("AllFinish  Start 3")


                    self.testingFlag = False
                    self.currentLoopTimes += 1

                    self.currentLoopTimes = 0
                    self.totalLoopTimes = 0


                    self.objLog.Trace("AllFinish  Start Fixture End 4")
                    for i in range(0,3):                      
                        if self.fixture.End()==0:
                            break
                        else:
                            print "End Fail {}".format(i)
            
                    self.objLog.Trace("AllFinish  Finish Fixture End 5")
                    self.bTestingFlag = False

                    self.objLog.Trace("AllFinish  Start ZipLog 6")
                    strRet = self.objLog.StopTest()
                    self.objLog.Trace("AllFinish  Start ZipLog {} 7".format(strRet))


            
    def sendStartMsgToAllSeqs(self):
        self.testingFlag = True
        self.bTestingFlag = True
        self.objLog.StartTest()
        self.fixtureSM.state_switch(FixtureSM.EVENT["START"])
        self.fixture.send_cmd("TEST START")
        if self.UUtInfos:
            self.handleSetUutSNMsg(self.UUtInfos)
        index = 0

        for uut in self.uuts:
            self.objLog.Trace("EnableFlag {}:{}".format(index,uut.getUutEnableFlag()))
            if uut.getUutEnableFlag():
                uut.setUutEnableFlag(self.DummyCheckobjs[index].DummyCheck())

            if uut.getUutEnableFlag():
                if True:  # uut.getUutSN():
                    resp = uut.getSeqReq().send_cmd("run", {"attributes": {"MLBSN": ""}},
                                                    timeout=1000)
                else:
                    resp = uut.getSeqReq().send_cmd("run", None, timeout=1000)
                try:
                    if resp is None or getattr(resp, "error"):
                        uut.setUutFlag(True)
                except AttributeError:
                    pass
            index += 1

        bStartFlag = False
        for uut in self.uuts:
            if uut.getUutEnableFlag():
                bStartFlag = True

        if not bStartFlag:
            self.testingFlag = False
            self.bTestingFlag = False
            self.fixture.End()

        return True

    @public('checkchange')
    def handleCheckMsg(self, params):
        self.objLog.Trace("Get Check Message TestFlag:{}".format(self.testingFlag))

        if "uutinfo" in params:
            self.UUtInfos = params["uutinfo"]

        self.objLog.Trace("Start  Return {}".format(self.testingFlag))
        return True
    @public('start')
    def handleStartMsg(self, params):
        self.objLog.Trace("Get Start Message TestFlag:{}".format(self.testingFlag))
        if self.FixtureMode==0:
            if self.testingFlag:
                #raise SMInternalError("SM in Testing status")
                return False
    
            self.totalLoopTimes = int(params["times"])
            if self.totalLoopTimes > 1:
                self.stopLoopFlag = False
                self.fixtureSM.setLoopTestFlg(True)
            
            if "uutinfo" in params:
                self.handleSetUutSNMsg(params["uutinfo"])


            self.objLog.StartTest()
            self.sendStartMsgToAllSeqs()
    
            return True
        elif self.FixtureMode==1:
            self.objLog.Trace("Auto Mode Start  Message {}".format(self.testingFlag))


            if self.testingFlag:
                # raise SMInternalError("SM in Testing status")
                return False

            self.totalLoopTimes = int(params["times"])
            if self.totalLoopTimes > 1:
                self.stopLoopFlag = False
                self.fixtureSM.setLoopTestFlg(True)

            if "uutinfo" in params:
                self.handleSetUutSNMsg(params["uutinfo"])
            self.UUtInfos = params["uutinfo"]
            for i in range (0,3):
                if self.fixture.StartWithDutCheck()==0:
                    break
                else:
                    print "StartWithDutCheck Fail {}".format(i)

            self.objLog.Trace("Start  Return {}".format(self.testingFlag))
            return True
            
    def CheckOutFinish(self):
        self.objLog.Trace("AutoStart Check Out Flag:{}".format(self.bOutFlagOpen))
        if self.bOutFlagOpen!=0:
            while 1:
                if self.fixture.CheckSatus("OUT"):
                    self.bOutFlagOpen=0
                    break
        self.objLog.Trace("AutoStart Check Out Flag:{}".format(self.bOutFlagOpen))

    def AutoStart(self):
        self.objLog.Trace("AutoStart IN:{} DOWN:{} Testing:{}".format(self.fixture.CheckSatus("IN"),self.fixture.CheckSatus("DOWN"),self.bTestingFlag))
        if self.fixture.CheckSatus("IN") and self.fixture.CheckSatus("DOWN") and  not self.bTestingFlag:
            self.sendStartMsgToAllSeqs()
            return True
        return False
    

    @public('abort')
    def handleAbortMsg(self):
        self.stopLoopFlag = True
        self.testingFlag = False
        self.fixtureSM.state_switch(FixtureSM.EVENT["ABORT"])
        for uut in self.uuts:
            if uut.getUutEnableFlag():
                uut.getSeqReq().send_cmd("abort", None)
        return True

    @public('status')
    def handleStatusMsg(self):
        test_states = [s.status().result != "RUNNING" for s in self.sequencers]
        return all(test_states)




    @public('load')
    def handleLoadMsg(self,params):
        for uut in self.uuts:
            uut.getSeqReq().send_cmd("load", params)
        return True

    @public('list')
    def handleListMsg(self,params):
        self.uuts[0].getSeqReq().send_cmd("list", params)
        return True

    
        
    @public('setsn')
    def handleSetUutSNMsg(self, params):
        for uut in self.uuts:
            uut.setUutEnableFlag(False)
        for item in params:
            if item["uutNum"] < 0 or item["uutNum"] >= len(self.uuts):
                errMsg = "uutNum should be in [0, %d); But uutNum in params is %d" %(len(self.uuts), item["uutNum"])

                raise JSONRPCInvalidParamsError(errMsg)
            
            self.uuts[item["uutNum"]].setUutSN(item["SN"])
            self.uuts[item["uutNum"]].setUutEnableFlag(True)
            self.uuts[item["uutNum"]].setUutFlag(False)
            
        return True
    
    
    def register_public_methods(self):
        for name, f in inspect.getmembers(
                self, lambda f: callable(f) and hasattr(f, '_rpc_public_name')
        ):
            self.add_method(f, f._rpc_public_name)


    def _dispatch(self, request):
        try:
            try:
                method = self.get_method(request.method)
            except MethodNotFoundError as e:
                return request.error_respond(e)

            # we found the method
            try:
                if request.params:
                    result = method(request.params)
                else:
                    result = method()
            except RPCError as e:
                # an error occured within the method, return it
                logging.error("%s", e.message, exc_info=True)
                return request.error_respond(e)
            # respond with result
            return request.respond(result)
        except Exception as e:
            logging.error("%s", traceback.format_exc())
            return request.error_respond(JSONRPCServerError(e.message + os.linesep + traceback.format_exc()))
        
        
        
         
    