import zmq
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqServerTransport
from tinyrpc.server import RPCServer
from tinyrpc.dispatch import RPCDispatcher


class RPCServerWrapper:
    def __init__(self, transport, publisher, ctx=None, protocol=None, dispatcher=None):
        self.ctx = ctx if ctx else zmq.Context().instance()
        self.protocol = protocol if protocol else JSONRPCProtocol()
        self.dispatcher = dispatcher if dispatcher else RPCDispatcher()

        if isinstance(transport, ZmqServerTransport):
            self.transport = transport
        else:
            if 'tcp' not in str(transport):
                transport = "tcp://*:" + str(transport)
            self.transport = ZmqServerTransport.create(self.ctx, transport)

        self.publisher = publisher
        self.transport.publisher = publisher

        self.rpc_server = RPCServer(self.transport, self.protocol, self.dispatcher)

        if hasattr(self.dispatcher, 'public'):
            @self.dispatcher.public('::stop::')
            def stop():
                self.rpc_server.serving = False

    # def start_server(self):
    #     self.rpc_server.serving = True

    def stop_server(self):
        self.rpc_server.serving = False
