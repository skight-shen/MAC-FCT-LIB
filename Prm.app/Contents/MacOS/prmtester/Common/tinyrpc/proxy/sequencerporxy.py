
import zmq

from rpcproxy import RPCProxy
from Common.tinyrpc.protocols.sequencerrpc import SequencerRPCProtocol
from Common.tinyrpc.transports.zmq import ZmqClientTransport
from Common import zmqports
from Common.tinyrpc.protocols.jsonrpc import JSONRPCTimeoutError

class SequencerProxy(RPCProxy):

    #timeout in seconds
    def __init__(self, site, publisher, url=None, retries=2, timeout=1, ctx=None):
        if not url:
            url = "tcp://127.0.0.1"
        if not ctx:
            ctx = zmq.Context.instance()
        super(SequencerProxy, self).__init__(ZmqClientTransport.create(ctx, url + ':' + str(int(zmqports.SEQUENCER_PORT) + site)),
                                      SequencerRPCProtocol(),
                                      publisher,
                                      retries)
        self.identity = 'SequencerProxy'

    def send_cmd(self, function, params, timeout=1000):
        req = self.protocol.create_request(function, params)
        response = self.send_request(req, timeout)
        # if response is None:
        #     raise JSONRPCTimeoutError('time out calling ' + function + '('
        #                               + str(params) + ')')
        return response
