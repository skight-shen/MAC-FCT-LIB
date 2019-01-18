import argparse
import json
import new
import time
import traceback
from threading import Thread

import zmq

import levels
from filelogger import *
from puddinglogger import *
from userlogger import *
from publisher import ZmqPublisher
from x527 import zmqports
from x527.tinyrpc import FCT_HEARTBEAT, HEARTBEAT_INTERVAL


def extend(obj, cls, alias, func_name):
    """ Add/replace instance method dynamically during runtime

    :param obj: class instance
    :param cls: class name
    :param alias: desired new method name
    :param func_name: source function name to be added as a instance method
    :return: success flag
    """
    def NoOp():
        return

    if not func_name:
        setattr(obj, alias, new.instancemethod(NoOp, obj, cls))
        return True
    func = globals().get(func_name)
    if func:
        setattr(obj, alias, new.instancemethod(func, obj, cls))
        return True
    else:
        print 'function: {} not found'.format(func_name)
        return False


class LoggerServer(Thread):

    socket_callbacks = {}

    def __init__(self, publisher, site_count=6, url='tcp://localhost:'):
        super(LoggerServer, self).__init__()
        self.heartbeat_at = 0
        self.poller = zmq.Poller()
        self.loggers = []
        self.receiving = True
        self.publisher = publisher
        self.url = url
        self.site_count = site_count
        self.path = '/tmp'

    def load_config(self, disable_pudding, config_file='config.json'):
        path = os.path.join(os.path.split(__file__)[0], os.path.pardir, config_file)
        cfg = os.path.abspath(path)
        if os.path.exists(cfg):
            config = json.load(open(cfg, 'rU'), encoding='ascii')
        else:
            return False

        defaults = config.get('defaults')
        if defaults:
            self.site_count = int(defaults.get('site', self.site_count))
            self.url = defaults.get('url', self.url) + ':'
            self.path = defaults.get('log_file_path', self.path)
            if not os.path.exists(self.path):
                os.mkdir(self.path)

        root = config.get('logger')
        if root:
            default_subs = root.get('default_subscribers', [])
            loggers = root.get('loggers', [])
            for logger in loggers:
                if logger.get('enabled').upper() != 'YES':
                    print '"{}" is disabled'.format(logger.get('alias', 'anonymous'))
                    continue
                if logger.get('alias') == 'Pudding' and disable_pudding:
                    print 'Pudding logger is disabled by command-line argument'
                    continue
                cls_name = logger.get('class', 'FileLogger')
                cls = globals().get(cls_name)
                if not cls:
                    print 'class: {} not found'.format(cls_name)
                    return False
                path = logger.get('log_file_path', self.path)
                sub_per_site = logger.get('subscriber_per_site', 1)
                suffix = logger.get('log_file_suffix', '.log')
                level = logger.get('level', levels.DEBUG)
                f_log = cls(path, self.site_count, sub_per_site, self.publisher, suffix, level)
                print logger.get('alias'), path, self.site_count, sub_per_site, self.publisher, suffix, level
                f_log.alias = logger.get('alias')
                if f_log.alias == 'Pudding':
                    f_log.server = self
                f_log.sub_alias = logger.get('sub_alias')
                if f_log.sub_alias and len(f_log.sub_alias) != sub_per_site:
                    print 'sub_alias {0} length mismatch with sub_per_site {1}'.format(f_log.sub_alias, sub_per_site)
                    return False
                self.loggers.append(f_log)
                event_callbacks = [i for i in logger if i.startswith('on_') or i.startswith('post_')]
                for event in event_callbacks:
                    extend(f_log, cls, event, logger[event])
                subs = default_subs + logger.get('subscribers', [])
                for sub in subs:
                    port = getattr(zmqports, sub.get('port'), None)
                    if not port:
                        print sub['port'] + ' not defined in zmqports.py'
                        return False
                    channel = sub.get('zmq_channel', '')
                    if len(channel) > 0:
                        channel = getattr(zmqports, channel, None)
                        if not channel:
                            print channel + ' not defined in zmqports.py'
                            return False
                    func_name = sub.get('callback', 'default_log')
                    if not hasattr(f_log, func_name):
                        if not extend(f_log, cls, func_name, func_name):
                            return False
                    for i in range(self.site_count * sub_per_site):
                        socket = self.subscribe(self.url, str(port+i), channel, getattr(f_log, func_name))
                        if str(sub.get('need_timestamp', '')).upper() == 'YES':
                            f_log.need_timestamp.append(socket)
                        if str(sub.get('auto_line_ending', '')).upper() == 'YES':
                            f_log.auto_line_ending.append(socket)
                    formatter_name = sub.get('msg_formatter')
                    if formatter_name and formatter_name != 'default_log_formatter':
                        if not extend(f_log, cls, 'default_log_formatter', formatter_name):
                            return False
        return True

    def subscribe(self, url, port, channel, callback):
        ctx = zmq.Context.instance()
        socket = self.__find_socket(port)
        if not socket:
            socket = ctx.socket(zmq.SUB)
            socket.setsockopt(zmq.IDENTITY, port)
            socket.setsockopt(zmq.SUBSCRIBE, channel)
            socket.connect(url + port)
            self.poller.register(socket, zmq.POLLIN)
        self.__register_callback(self.socket_callbacks, socket, callback)
        return socket

    def unsubscribe(self, socket):
        self.poller.unregister(socket)
        socket.setsockopt(zmq.LINGER, 0)
        socket.close()

    def get_log_paths(self, site):
        log_lst = []
        for logger in self.loggers:
            logs = logger.get_log_path(site)
            if isinstance(logs, list):
                log_lst.extend(logs)
            else:
                log_lst.append(logs)
        return log_lst

    def __get_sockets(self):
        tup_list = self.poller.sockets
        sockets = [i[0] for i in tup_list]
        return sockets

    def __find_socket(self, port):
        for socket in self.__get_sockets():
            if str(port) == socket.getsockopt(zmq.IDENTITY):
                return socket
        return None

    @staticmethod
    def __register_callback(registry, socket, callback):
        if socket not in registry:
            registry[socket] = [callback, ]
        else:
            registry[socket].append(callback)

    def __shutdown(self):
        for socket in self.__get_sockets():
            self.unsubscribe(socket)

    def __signal_heartbeat(self):
        t_now = time.time()
        if t_now >= self.heartbeat_at:
            self.publisher.publish(FCT_HEARTBEAT, level=levels.INFO, id_postfix='logger thread')
            self.heartbeat_at = t_now + HEARTBEAT_INTERVAL

    def __read_socket_with_callback(self, socket):
        try:
            while self.receiving:
                msg = socket.recv_multipart(zmq.NOBLOCK)
                for func in self.socket_callbacks.get(socket, []):
                    func(socket, msg)
        except:
            pass

    def run(self):
        self.publisher.publish('logger started', level=levels.INFO, id_postfix='logger thread')
        self.heartbeat_at = time.time() + HEARTBEAT_INTERVAL
        while self.receiving:
            try:
                socks = dict(self.poller.poll(1000))
                for socket in self.__get_sockets():
                    if socket in socks and socks[socket] == zmq.POLLIN:
                        self.__read_socket_with_callback(socket)
            except zmq.ZMQError as e:
                print e.message, traceback.format_exc()
            self.__signal_heartbeat()
        self.__shutdown()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--disable_pudding', help='disable pudding logger and override config.json setting',
                        action='store_true', default=False)
    args = parser.parse_args()

    ctx = zmq.Context()
    publisher = ZmqPublisher(ctx, "tcp://*:" + str(zmqports.LOGGER_PUB), 'Logger')
    logger_server = LoggerServer(publisher)

    if not logger_server.load_config(args.disable_pudding):
        print "Fail to initialize loggers"
        exit()

    time.sleep(0.2)
    logger_server.start()

    raw_input()
    logger_server.receiving = False
