#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import  # needed for zmq import
import six
import zmq
import time
from ingenuity.tinyrpc import HEARTBEAT_INTERVAL, FCT_HEARTBEAT
from . import ServerTransport, ClientTransport


DEFAULT_RPC_TIMEOUT = 1000


class ZmqServerTransport(ServerTransport):
    """Server transport based on a :py:const:`zmq.ROUTER` socket.

    :param socket: A :py:const:`zmq.ROUTER` socket instance, bound to an
                   endpoint.
    """

    def __init__(self, socket, polling_milliseconds=0):
        self.publisher = None
        self.socket = socket
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)
        self.polling_milliseconds = polling_milliseconds
        self.heartbeat_at = time.time()

    def broadcast(self, msg):
        self.publisher.publish(msg)
        self.heartbeat_at = time.time() + HEARTBEAT_INTERVAL
        # TODO: HB shall be out per 5sec or only needed as NOP when PUB idle?

    def check_heartbeat(self):
        t_now = time.time()
        if t_now >= self.heartbeat_at:
            self.broadcast(FCT_HEARTBEAT)

    def receive_message(self):
        """Asynchronous poll socket"""
        socks = dict(self.poller.poll(HEARTBEAT_INTERVAL*1000))
        if socks.get(self.socket) == zmq.POLLIN:
            msg = self.socket.recv_multipart()
            context, message = msg[:-1], msg[-1]
            self.broadcast('received: ' + message)
        else:
            context, message = None, None
        return context, message

    def send_reply(self, context, reply):
        self.socket.send_multipart(context + [reply])
        self.broadcast('response: ' + reply)

    @classmethod
    def create(cls, zmq_context, endpoint, polling_milliseconds=0):
        """Create new server transport.

        Instead of creating the socket yourself, you can call this function and
        merely pass the :py:class:`zmq.core.context.Context` instance.

        By passing a context imported from :py:mod:`zmq.green`, you can use
        green (gevent) 0mq sockets as well.

        :param zmq_context: A 0mq context.
        :param endpoint: The endpoint clients will connect to.
        """
        socket = zmq_context.socket(zmq.ROUTER)
        socket.bind(endpoint)
        return cls(socket, polling_milliseconds)

    def shutdown(self):
        if not self.socket.closed:
            self.socket.setsockopt(zmq.LINGER, 0)
            self.socket.close()


class ZmqClientTransport(ClientTransport):
    """Client transport based on a :py:const:`zmq.REQ` socket.

    :param socket: A :py:const:`zmq.REQ` socket instance, connected to the
                   server socket.
        :param zmq_context: A 0mq context.
        :param endpoint: The endpoint the server is bound to.
    """

    def __init__(self, socket, context, endpoint, timeout=DEFAULT_RPC_TIMEOUT):
        self.publisher = None
        self.socket = socket
        self.context = context
        self.endpoint = endpoint
        self.timeout = timeout

    def reconnect(self):
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.close()
        time.sleep(0.1)
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(self.endpoint)

    def send_reply(self, message):
        poll = zmq.Poller()
        poll.register(self.socket, zmq.POLLIN)

        if six.PY3 and isinstance(message, six.string_types):
            # pyzmq won't accept unicode strings
            message = message.encode()

        self.socket.send(message)

        z_timeout = self.timeout+50 if self.timeout > 0 else None  # give it a little time for overhead
        socks = dict(poll.poll(z_timeout))
        if socks.get(self.socket) == zmq.POLLIN:
            reply = self.socket.recv()
        else:
            reply = None
            poll.unregister(self.socket)
            self.reconnect()  # reconnect socket otherwise ZMQ socket stuck in unusable state
            poll.register(self.socket, zmq.POLLIN)

        return reply

    def shutdown(self):
        if not self.socket.closed:
            self.socket.setsockopt(zmq.LINGER, 0)
            self.socket.close()

    @classmethod
    def create(cls, zmq_context, endpoint):
        """Create new client transport.

        Instead of creating the socket yourself, you can call this function and
        merely pass the :py:class:`zmq.core.context.Context` instance.

        By passing a context imported from :py:mod:`zmq.green`, you can use
        green (gevent) 0mq sockets as well.

        :param zmq_context: A 0mq context.
        :param endpoint: The endpoint the server is bound to.
        """
        socket = zmq_context.socket(zmq.REQ)
        socket.connect(endpoint)
        return cls(socket, zmq_context, endpoint)
