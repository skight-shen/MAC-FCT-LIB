#export PYTHONPATH='/Library/python-sequencer'
#import argparse
#import cmd
#import csv
import time
#import logging
from threading import Thread
import zmq
from x527 import zmqports
from x527.loggers import StdOutPublisher, ZmqPublisher
from x527.rpc_client import RPCClientWrapper
from x527.rpc_server import RPCServerWrapper
from x527.tinyrpc.protocols import jsonrpc
from Dispatcher import *
from registration import register


class TestEngine(Thread):
    def __init__(self, site):
        super(TestEngine, self).__init__()
        self.site = site

        ctx = zmq.Context().instance()
        # Ensure subscriber connection has time to complete
        time.sleep(1)
        self.publisher = ZmqPublisher(
            ctx,
            "tcp://*:" + str(zmqports.TEST_ENGINE_PUB + site),
            "Engine_{}".format(site)
        )
        time.sleep(0.5)  # give time for the subscribers to connect to this publisher
        mydispatcher=Dispatcher(self.publisher)
        register(mydispatcher)
        self.wrapper = RPCServerWrapper(
            zmqports.TEST_ENGINE_PORT + site,
            self.publisher,
            dispatcher=mydispatcher
        )
        self.rpc_server = self.wrapper.rpc_server
        self.wrapper.dispatcher.server = self.wrapper

    def run(self):
        self.publisher.publish('Test Engine {} Starting...'.format(self.site))
        self.rpc_server.serve_forever()
        self.publisher.publish('Test Engine {} Stopped...'.format(self.site))



