#encoding=utf-8


import logging
import zmq

# import sys
# import os
#
# sys.path.append(os.getcwd())
# print "sys.path is as follow:"


from Common import zmqports
from Common.publisher import ZmqPublisher
import StateSwitch
import Fixture


#跟业务相关的代码
class FixtureSM(StateSwitch.StateSwitch):
    EVENT = {
        "ABORT" : "ABORT",
        "LOADED" : "UUT_LOAD",
        "START" : "TEST_START",
        "FINISH" : "TEST_FINISH",
        "ERROR" : "ERROR",
        "WILL_UNLOAD" : "UUT_WILL_UNLOAD",
        "REMOVED" : "UUT_REMOVED"
    }
        
    STATE = {
        "IDLE" : "SM_IDLE",
        "LOADED" : "SM_UUT_LOADED",
        "TESTING" : "SM_TESTING",
        "DONE" : "SM_TESTING_DONE",
        "UNLOAD" : "SM_UUT_UNLOADED",
        "ERROR" : "SM_ERROR"
    }
    
    def __init__(self, ser, publisher):
        super(FixtureSM, self).__init__(FixtureSM.STATE["IDLE"], publisher)
        # req_addr = "tcp://127.0.0.1:" + str(zmqports.FIXTURE_CTRL_PORT)
        # sub_addr = "tcp://127.0.0.1:" + str(zmqports.FIXTURE_CTRL_PUB)
        self.fixture = Fixture.Fixture(ser, publisher)
        
        self.init_sm()
        
    def setLoopTestFlg(self, flag):
        self.fixture.setLoopTestFlg(flag)
        
        
    def start(self):
        self.fixture.close()
        self.fixture.press()

    def abort(self):
        self.fixture.release()
        self.fixture.open()
           
    def init_sm(self):
        self.add_transition(FixtureSM.STATE["IDLE"], FixtureSM.STATE["LOADED"], FixtureSM.EVENT["LOADED"], self.fixture.close)
        self.add_transition(FixtureSM.STATE["IDLE"], FixtureSM.STATE["TESTING"], FixtureSM.EVENT["START"], self.start)
        
        self.add_transition(FixtureSM.STATE["LOADED"], FixtureSM.STATE["TESTING"], FixtureSM.EVENT["START"], self.start)
        self.add_transition(FixtureSM.STATE["LOADED"], FixtureSM.STATE["IDLE"], FixtureSM.EVENT["ABORT"], None)
        
        self.add_transition(FixtureSM.STATE["TESTING"], FixtureSM.STATE["DONE"], FixtureSM.EVENT["FINISH"], self.fixture.release)
        self.add_transition(FixtureSM.STATE["TESTING"], FixtureSM.STATE["IDLE"], FixtureSM.EVENT["ABORT"], None)
        
        self.add_transition(FixtureSM.STATE["DONE"], FixtureSM.STATE["UNLOAD"], FixtureSM.EVENT["WILL_UNLOAD"], self.fixture.open)
        self.add_transition(FixtureSM.STATE["DONE"], FixtureSM.STATE["TESTING"], FixtureSM.EVENT["START"], self.fixture.press)
        
        self.add_transition(FixtureSM.STATE["UNLOAD"], FixtureSM.STATE["IDLE"], FixtureSM.EVENT["REMOVED"], None)
        self.add_transition(FixtureSM.STATE["UNLOAD"], FixtureSM.STATE["TESTING"], FixtureSM.EVENT["START"], self.fixture.close)
