import threading

import zmq

from ingenuity import zmqports
from ingenuity.loggers import ZmqPublisher
from ingenuity.rpc_client import RPCClientWrapper


class FixtureClient(threading.Thread):
    def __init__(self):
        super(FixtureClient, self).__init__()

        ctx = zmq.Context().instance()
        url = "127.0.0.1"
        self.publisher = ZmqPublisher(ctx, 'tcp://*:' + str(zmqports.FIXTURE_PROXY_PUB), 'FixtureClient')
        self.rpc_client = RPCClientWrapper("tcp://" + url + ':' + str(zmqports.FIXTURE_PORT),
                                           self.publisher)
        self.proxy = self.rpc_client.remote_server()
        self.serving = True

    def run(self):
        while (self.serving):
            reply = self.proxy.get_state()

            self.handle_msg(reply)
        return

    def handle_msg(self, recv):
        if recv == 'Ready':
            pass
        return recv


if __name__ == '__main__':
    client = FixtureClient()
    client.start()
