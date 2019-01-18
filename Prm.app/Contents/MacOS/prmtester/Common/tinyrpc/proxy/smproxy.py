import zmq

from Common.tinyrpc.proxy.rpcproxy import RPCProxy
from Common.tinyrpc.protocols.jsonrpc import JSONRPCTimeoutError
from Common.tinyrpc.transports.zmq import ZmqClientTransport
from Common import zmqports
from Common.tinyrpc.protocols.StateMachineRpc import StateMachineRPCProtocol, StateMachineRPCRequest
# from tinyrpc.protocols.smrpc import StateMachienRPCProtocol, StateMachineRPCRequest

class SMProxy(RPCProxy):

    #timeout in seconds
    def __init__(self, publisher, url='tcp://localhost', retries=2, ctx=None):
        if not ctx:
            ctx = zmq.Context()
            
        super(SMProxy, self).__init__(ZmqClientTransport.create(ctx, url + ':' + str(zmqports.SM_PORT)),
                                      StateMachineRPCProtocol(),
                                      publisher,
                                      retries)
        self.identity = 'SMProxy'
        

    def send_cmd(self, event_name, event_data, timeout = 3000):
        req = self.protocol.create_request(event_name, event_data)
        response = self.send_request(req, timeout) 
        return response