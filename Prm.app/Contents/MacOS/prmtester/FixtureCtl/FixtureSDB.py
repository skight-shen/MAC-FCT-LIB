import argparse
import cmd
import os
import readline
import sys
import time
import traceback
from datetime import datetime
from functools import wraps

import zmq

from Common import zmqports
from Common.rpc_client import RPCClientWrapper
from Common.tinyrpc.protocols.jsonrpc import RPCError
from Common.publisher import ZmqPublisher

readline.parse_and_bind("bind ^I rl_complete")


def handle_response(afunc):
    @wraps(afunc)
    def _(*args, **kwargs):
        try:
            reply = afunc(*args, **kwargs)
            if reply:
                if hasattr(reply, 'result'):
                    print reply.result
                else:
                    print str(reply)
        except RPCError as e:
            print e.message, os.linesep, traceback.format_exc()

    return _


class FixtureDebugger(cmd.Cmd):
    prompt = 'sdb>'
    intro = 'Fixture RPC client debugger'
    fixture = None
    break_points = []
    this_run = None
    stat = ''

    @handle_response
    def do_start(self, line):
        self.fixture.start()

    @handle_response
    def do_control(self, cmd):
        self.fixture.control(cmd)

    @handle_response
    def do_press(self, line):
        self.fixture.press()

    def do_EOF(self, line):
        """Ctrl-D to quit sdb without stopping the sequencer server"""
        return True

    def do_quit(self, line):
        """quit sdb and stop the sequencer server. If you just want to quit sdb without stopping
        the sequencer server you should use ctrl-D"""
        self.fixture.__getattr__('::stop::')()
        return True

    def emptyline(self):
        pass


def create_sdb(url):
    sdb = FixtureDebugger()
    ctx = zmq.Context.instance()
    fixture = RPCClientWrapper("tcp://" + url + ":" + str(zmqports.FIXTURE_CTRL_PORT),
                               ZmqPublisher(ctx, "tcp://*:" + str(zmqports.SEQUENCER_PROXY_PUB + 1),
                                            "Sequencer Proxy")).remote_server()
    sdb.fixture = fixture
    return sdb


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='Sequencer URL', default="127.0.0.1")
    args = parser.parse_args()

    sdb = create_sdb(args.url)

    sdb.cmdloop()
