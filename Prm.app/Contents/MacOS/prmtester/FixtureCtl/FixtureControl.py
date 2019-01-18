#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'PRM --jinhui.huang--'

import zmq
from Common import zmqports
from Common.tinyrpc.dispatch import RPCDispatcher
from Common.publisher import ZmqPublisher
import serial
from threading import Thread
from Common.rpc_server import RPCServerWrapper
import time
import argparse
from Common.tinyrpc.dispatch import public
from Fixture import Fixture
from FixtureDriver import SerialDriver

VERSION = "%s %s" % ("0.0.1", "updated on 2018-03-28")


class FixtureControl(RPCDispatcher):
    def __init__(self, publisher):
        super(FixtureControl, self).__init__()
        self.dispatch = RPCDispatcher()
        self.publisher = publisher
        self.fixture_cfg = {}
        self.fixture = Fixture(SerialDriver(), self.publisher)

    @public('start')
    def start(self):
        self.fixture.open()

    @public('press')
    def press(self):
        self.fixture.press()
        print self.fixture.getFixtureStatus()

    @public('control')
    def control(self, cmd):
        self.fixture.control(cmd)

    @public('setLoopTestFlg')
    def setLoopTestFlg(self, flag):
        self.fixture.setLoopTestFlg(flag)

    @public('getLoopTestFlg')
    def getLoopTestFlg(self):
        return self.fixture.getLoopTestFlg()

    @public('send_cmd')
    def send_cmd(self, command):
        return '--test--'


class FixtureControlServer(Thread):
    def __init__(self, args):
        super(FixtureControlServer, self).__init__()
        ctx = zmq.Context()
        # create a publisher for FIXTURE Control
        self.publisher = ZmqPublisher(ctx, "tcp://*:" + str(zmqports.FIXTURE_CTRL_PUB), "FixtureControl")
        time.sleep(1)

        self.fixture = FixtureControl(self.publisher)
        # create a server wrapper
        self.wrapper = RPCServerWrapper("tcp://*:" + str(zmqports.FIXTURE_CTRL_PORT), self.publisher)

        self.wrapper.dispatcher.register_instance(self.fixture)
        # get rpc server instance
        self.rpc_server = self.wrapper.rpc_server

    def run(self):
        self.publisher.publish("Fixture Control Starting...")
        print 'Fixture Control Starting'

        try:
            self.rpc_server.serve_forever()
            self.publisher.publish('Fixture Control Stopped...')
            print 'Fixture Control Stoped'
        except Exception as e:
            print 'error starting the Fixture Control: ' + e.message


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='FixtureControl')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s' + "'s version is " + VERSION)
    args = parser.parse_args()

    server = FixtureControlServer(args)
    server.start()
