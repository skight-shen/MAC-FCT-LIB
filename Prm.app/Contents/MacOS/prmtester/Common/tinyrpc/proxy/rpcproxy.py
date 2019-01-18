

import zmq
import logging

from Common.tinyrpc.exc import RPCError


from ..protocols.jsonrpc import JSONRPCTimeoutError

class RPCProxy(object):
    def __init__(self, transport, protocol, publisher, retries):
        self.transport = transport
        self.publisher = publisher
        self.protocol = protocol
        self.identity = 'RPCProxy'
        self.retries = retries

    def send_request(self, request, timeout=1000):
        retries_left = self.retries
        # if request.function == 'start_test':
        #     self.transport.reconnect()

        poll = zmq.Poller()
        poll.register(self.transport.socket, zmq.POLLIN)
        while retries_left:
            s_req = request.serialize()
            self.transport.socket.send(s_req)
            logging.info("msg send: " + str(s_req))
            # self.publisher.publish(s_req, 'sent')
            retries_left -= 1

            if timeout != -1:
                z_timeout = timeout + 50 #give it a little time for overhead
                if timeout==0: #if timeout is 0 then no timeout
                    z_timeout=None
            else:
                z_timeout = None

            socks = dict(poll.poll(z_timeout))
            if socks.get(self.transport.socket) == zmq.POLLIN:
                # we always expect a reply
                reply = self.transport.socket.recv()
                response = self.protocol.parse_reply(reply)
                # self.publisher.publish(response.serialize(), 'received')
                logging.info("msg received: " + str(response.serialize()))
                return response
            else:
                logging.warn('timed out waiting for response to req[' + request.unique_id + ']')
                
                # self.publisher.publish(
                #     'timed out waiting for response to req[' + request.unique_id + '], retires left ' + str(retries_left))
                poll.unregister(self.transport.socket)
                self.transport.reconnect()
                poll.register(self.transport.socket, zmq.POLLIN)
                
        logging.warn("msg received nothing")
        return None

    def __getattr__(self, name):
        """Returns a proxy function that, when called, will call a function
        name ``name`` on the client associated with the proxy.
        """
        proxy_func = lambda *args, **kwargs: self.call(
            name,
            *args,
            **kwargs
        )
        return proxy_func

    def call(self, func, params, timeout=1000):
        response = self.send_cmd(func, params, timeout)
        if response is None:
            raise JSONRPCTimeoutError('request for ' + func + '(' + str(params) + ') timed out')
        if hasattr(response, 'error'):
            raise RPCError('Error calling remote procedure: %s' % \
                           response.error)

        return response.result

    def __del__(self):
        if not self.transport.socket.closed:
            self.transport.socket.setsockopt(zmq.LINGER, 0)
            self.transport.socket.close()
