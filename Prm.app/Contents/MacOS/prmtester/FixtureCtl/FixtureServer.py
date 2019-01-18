import time
import zmq
import sys
import os



sys.path.append(os.getcwd())

if not __package__:
    path = os.path.join(os.path.dirname(__file__), os.pardir)
    sys.path.insert(0, path)

from threading import Thread
from Common.tinyrpc.transports.zmq import ZmqServerTransport
from Common.publisher import ZmqPublisher
from Common import zmqports
from FixtureDriver import SerialDriver




from TcpDriver import *

    # abc.send_cmd("DUT STATUS")


class FixtureServer(Thread):
    def __init__(self):
        super(FixtureServer, self).__init__()
        ctx = zmq.Context()
        self.frontend = ctx.socket(zmq.ROUTER)
        listen_addr = "tcp://*:" + str(zmqports.FIXTURE_CTRL_PORT)
        self.frontend.bind(listen_addr)
        pub_addr = "tcp://*:" + str(zmqports.FIXTURE_CTRL_PUB)
        self.publisher = ZmqPublisher(ctx, pub_addr, "FIXTURE")
        self.transport = ZmqServerTransport(self.frontend)
        self.transport.publisher = self.publisher

        self.fixture = SerialDriver()

        cfg = {"id":0,"ip":"169.254.1.32","port":7643,"endStr":"\n"}

        self.fixture = TcpDriver(cfg)

        self.serving = self.fixture.connect()

        self.status = ""




    def run(self):
        print ("FixtureSrver is Starting...")
        while self.serving:
            context, message = self.transport.receive_message()
            if message:
                result = self.fixture.req_recv(message)
                self.transport.send_reply(context, str(result))

        print("FixtureServer Stoped")
        self.fixture.close()
        self.transport.shutdown()


fs = FixtureServer()
fs.start()
