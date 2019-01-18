from ingenuity.loggers import ZmqPublisher
from ingenuity.rpc_server import RPCServerWrapper

from ingenuity.tinyrpc.dispatch import RPCDispatcher
import zmq
from ingenuity import zmqports
import time
import argparse
import threading
import traceback
from ingenuity.fixture.Fixture import Fixture


class FixtureServer(threading.Thread):
    def __init__(self, publisher=None,dispatcher=None):
        super(FixtureServer, self).__init__()
        self.fixture = Fixture()
        if publisher:
            self.publisher = publisher
        else:
            ctx = zmq.Context().instance()
            self.publisher = ZmqPublisher(ctx,"tcp://*:"+str(zmqports.FIXTURE_PUB),"FIXTURE_SERVER")
            time.sleep(1)#give the publisher sometime

        if dispatcher:
            self.dispatcher = dispatcher
        else:
            self.dispatcher = RPCDispatcher()
            self.dispatcher.register_instance(self.fixture)

        self.rpcserver = RPCServerWrapper(
            zmqports.FIXTURE_PORT,
            self.publisher,
            dispatcher=self.dispatcher
        ).rpc_server

    def run(self):
        self.publisher.publish('FixtureServer starting ......')
        print "fixture server starting"
        try:
            self.rpcserver.serve_forever()
            self.publisher.publish('Fixture server stopped ......')
        except Exception as e:
            print 'error running the fixture rpc server: ' + e.message
        print 'fixture server stopping'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
#    parser.add_argument('-c', '--count', help='the count of the sequencer thread', type=int, default=1)
    args = parser.parse_args()

    server = FixtureServer()
    server.start()

    assert server.rpcserver.serving