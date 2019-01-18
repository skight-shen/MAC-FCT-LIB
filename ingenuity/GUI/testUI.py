import argparse
import time
import os
import sys
import zmq
from ingenuity.tinyrpc.protocols.jsonrpc import RPCError
from ingenuity.loggers.publisher import ZmqPublisher
from ingenuity.rpc_client import RPCClientWrapper
from ingenuity import zmqports
from threading import Thread
import cmd
from functools import wraps
import readline
import traceback
from ingenuity.loggers import levels
from ingenuity.loggers.subscriberManager import Subscriber, Report
from ingenuity.loggers import events


class MainLoop(Thread):
    def __init__(self, sub):
        super(MainLoop, self).__init__()
        self.sm = RPCClientWrapper('tcp://localhost:' + str(zmqports.STATEMACHINE_PORT),
                                   ZmqPublisher(zmq.Context().instance(), "tcp://*:" + str(zmqports.SM_PROXY_PUB),
                                                'SMProxy')).remote_server()
        # TODO: call up different modules

        self.sub =sub
        self.receiving = True

    def run(self):
        # load_script(script_path)
        self.sm.dut_ready('/Users/admin/PycharmProjects/Repository/J140_FCT_IA/TM_Release/Profile/J140_MP_TESTPLAN_BE__20180903.csv')
        while self.receiving:
            rep = self.sm.get_fixture_state()
            if(hasattr(rep,'result')):
                # print rep.result
                if(rep.result == "READY"):
                    self.start_button()

            self.handlemsg(Report)
        return

    def handlemsg(self, report):
        # handle data based on event
        if report.event == events.FCT_HEARTBEAT:
            print "start item:{0}".format(Report.data)

        return

    def start_button(self):
        e_travelers = {0:{'attributes':{'sn':000}}}
        self.sm.start(e_travelers)
        self.sm.set_fixture_state('RUNNING')

    def abort_button(self):
        self.sm.abort()

if __name__ == "__main__":

    sub_seq = Subscriber(zmqports.TEST_ENGINE_PUB,levels.DEBUG)
    sub_seq.start()

    mainThread = MainLoop(sub_seq)
    mainThread.start()
