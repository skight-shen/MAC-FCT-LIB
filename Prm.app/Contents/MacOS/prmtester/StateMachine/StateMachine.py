#!/usr/bin/env python
#encoding=utf-8

import sys
import os
print('sm start')
print(sys.path)


for osPath in ['/Users/prmeasure/python-sequencer', '/Library/TestSW/python-sequencer',
               "/Library/Python/2.7/site-packages"]:
    if os.path.isdir(osPath):
        os.putenv("PYTHONPATH", osPath)

sys.path.append(os.getcwd())
import zmq
import inspect
import argparse
import json
import traceback
import time
import logging
from logging.handlers import RotatingFileHandler
from Common.publisher import ZmqPublisher
from Common import zmqports
from Common.tinyrpc.server import RPCServer
from Common.tinyrpc.server.HeartBeat import HB
from Common.tinyrpc.protocols.StateMachineRpc import StateMachineRPCProtocol
from Common.tinyrpc.transports.zmq import ZmqServerTransport
import StateSwitch
from SmServer import StateMachine
from Common.rpc_client import RPCClientWrapper


from Log.LogClient import LogClient

VERSION = "%s %s" %("0.0.1", "updated on 2018-01-16")


class StateMachineServer(RPCServer):
    site_count = 4
    def __init__(self, args):
        if sys.platform == "darwin":
            logFile = "/vault/Prm_Log/StateMachineLog/StateMachine.log"
            self.init_file_log(logFile)
        elif sys.platform == "win32":
            logFile = "c:\\vault\\Prm_log\\StateMachineLog" + os.sep + "StateMachine.log"
            self.init_file_log(logFile)
        ctx = zmq.Context()

        sm_pub_addr = "tcp://*:" + str(zmqports.SM_PUB)
        logging.info("SM HB's zmq addr is:%s", sm_pub_addr)
        self.m_publisher = ZmqPublisher(ctx, sm_pub_addr, "StateMachine")
        self.sequencers = StateMachineServer.connect_to_sequencers(self.site_count)


        self.sm = StateMachine(ctx, self.m_publisher, args.slots,self.sequencers)
        self.sm.register_public_methods()

        self.frontend = ctx.socket(zmq.ROUTER)
        listenAddr = "tcp://*:" + str(zmqports.SM_PORT)
        logging.info("SM Create listen zmq addr at: " + listenAddr)

        self.frontend.bind(listenAddr)
        transport = ZmqServerTransport(self.frontend)
        transport.publisher = self.m_publisher

        self.poller = zmq.Poller()
        self.poller.register(self.frontend, zmq.POLLIN)

        super(StateMachineServer, self).__init__(
            transport,
            StateMachineRPCProtocol(),
            self.sm,
        )

        self.register_sock()
        HB(5,self.m_publisher).start()
        logging.info("StateMachine init successful")

        
        
    def register_sock(self):
        subSocks = self.sm.get_seq_subs()
        
        for sock in subSocks:
            self.poller.register(sock, zmq.POLLIN)
            
            
    def init_console_log(self):
        FORMAT = "%(asctime)s %(levelname)s %(filename)s %(message)s"
        logging.basicConfig(format=FORMAT, level=logging.INFO)
        
        
    def init_file_log(self, logFile):
        pass
    #     logPath = os.path.dirname(logFile)
    #     if not os.path.exists(logPath):
    #         os.mkdir(logPath)
    #
    #     FORMAT = "%(asctime)s %(levelname)s %(filename)s %(message)s"
    #
    #     logging.basicConfig(format=FORMAT, level=logging.INFO)
    #
    #     Rthandler = RotatingFileHandler(logFile, maxBytes=200 * 1024 * 1024, backupCount=10)
    #     Rthandler.setLevel(logging.INFO)
    #     formatter = logging.Formatter(FORMAT)
    #     Rthandler.setFormatter(formatter)
    #     logging.getLogger().addHandler(Rthandler)
    
    
    def serve_forever(self):
        while self.serving:
            try:
                socks = dict(self.poller.poll(5*1000))
                if socks.get(self.frontend) == zmq.POLLIN:
                    context, msg = self.transport.receive_message()
                    response = self.handle_message(context, msg)
                    s_rep = response.serialize()
                    self.transport.send_reply(context, s_rep)
                else:
                    self.sm.deal_with_sub(socks)
            except Exception as e:
                logging.error("%s", str(e), exc_info=True)

    @staticmethod
    def connect_to_sequencers(site_count):
        '''
        This is a helper method to connect to sequencers
        '''
        sites = range(site_count)
        ctx = zmq.Context().instance()
        url2 = "127.0.0.1"
        url = "169.254.1.10"
        sequencers = [RPCClientWrapper("tcp://" + url2 + ':' + str(zmqports.SEQUENCER_PORT + site),ZmqPublisher(ctx, "tcp://*:" + str(zmqports.SEQUENCER_PROXY_PUB + site),"Sequencer Proxy")).remote_server() for site in sites]
        return sequencers
        
        
        
if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='StateMachine')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s' + "'s version is " +  VERSION)
    #parser.add_argument('-f', '--file', help='the path of zmqports', type=str, default='TesterConfig' + os.sep + 'zmqports.json')
    parser.add_argument('-s', '--slots', help='Slots of the fixture', type=int, default=4)
    #parser.add_argument('-m', '--module', help='The number of fixture', type=int, default=0)
    args = parser.parse_args()
    
    server = StateMachineServer(args)
    server.serve_forever()

    
