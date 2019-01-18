import zmq
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqClientTransport
from tinyrpc import RPCClient


class RPCClientWrapper:
    def __init__(self, transport, publisher, ctx=None, protocol=None):
        self.ctx = ctx if ctx else zmq.Context().instance()
        if isinstance(transport, ZmqClientTransport):
            self.transport = transport
        else:
            if 'tcp' not in str(transport):
                transport = "tcp://*:" + str(transport)
            self.transport = ZmqClientTransport.create(self.ctx, transport)

        self.protocol = protocol if protocol else JSONRPCProtocol()
        self.publisher = publisher
        self.transport.publisher = publisher

        self.rpc_client = RPCClient(self.protocol, self.transport, self.publisher, retries=1)

    def remote_server(self):
        return self.rpc_client.get_proxy()

    def hijack(self, mock, func=None):
        self.rpc_client._send_and_handle_reply = mock
