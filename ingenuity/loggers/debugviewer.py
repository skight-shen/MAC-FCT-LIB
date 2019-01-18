import argparse
import sys
import threading

import levels
from ingenuity import zmqports, tinyrpc
from ingenuity.loggers import LogSubscriber


class DebugViewerLogSubscriber(LogSubscriber):
    def __init__(self, port, listen_to_hearbeat, level, url=None):
        super(DebugViewerLogSubscriber, self).__init__(port, level, url)
        self.listen_to_heartbeat = listen_to_hearbeat
        self.lock = threading.Lock()

    def write_out(self, msg):
        self.lock.acquire()
        print msg
        self.lock.release()

    def handle_msg(self, msg):
        print "start to handle msg"
        if len(msg) == 5:
            topic, ts, level, origin, data = msg[:]
            if data == tinyrpc.FCT_HEARTBEAT:
                if self.listen_to_heartbeat:
                    self.write_out('[' + ts + ']\t' + origin + ':' + str(data))
                return
            if int(level) <= self.level:
                self.write_out('[' + ts + ']\t' + origin + ':' + str(data))
        else:
            self.write_out(str(msg))


def list_ports():
    for item in dir(zmqports):
        if not item.startswith('__'):
            print item + ' = ' + str(eval('zmqports.' + item))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--ports', default='6250',
                        help='a comma separted list of ports to listen to, default to 6150')
    parser.add_argument('-b', '--heartbeat', action="store_true", default=False,
                        help='listen for heartbeat')
    parser.add_argument('-l', '--listports', action="store_true", default=False,
                        help='list all the possible zmq publisher ports')
    parser.add_argument('-v', '--level', type=int, default=levels.DEBUG,
                        help='the level of verbosity. Only messages with higher priority than level are received')
    parser.add_argument('-r', '--report', action="store_true", default=False,
                        help='This viewer only reports formatted reporter message')

    args = parser.parse_args()

    if args.listports:
        list_ports()
        exit(0)
    if args.report:
        args.level = levels.REPORTER

    ports = args.ports.split(',')
    int_ports = [int(p.strip()) for p in ports]
    subs = []
    for port in int_ports:
        print 'subscribing at port ' + str(port) + '; level is ' + str(args.level)
        s = DebugViewerLogSubscriber(port, args.heartbeat, args.level)
        s.start()
        subs.append(s)
    sys.stdout.write('press return to end\n')
    sys.stdin.readline()

    for s in subs:
        s.receiving = False
        s.join()
