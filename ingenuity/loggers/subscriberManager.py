import json
import logging
import threading
from ingenuity.loggers import events

import tinyrpc
from ingenuity.loggers import LogSubscriber

logger = logging.getLogger('Statemachine_core')


class Subscriber(LogSubscriber):
    def __init__(self, port, level, url=None):
        super(Subscriber, self).__init__(port, level, url)
        self.lock = threading.Lock()
        self.level = level
        # self.status = 'stop'

    def write_out(self, msg):
        self.lock.acquire()
        print msg
        self.lock.release()

    def handle_msg(self, msg):
        print msg
        if len(msg) == 5:
            topic, ts, level, origin, data = msg[:]
            try:
                # handle msg from sequencer
                if 'event' in data and 'data' in data:
                    dict_data = json.loads(data)
                    Report.event = dict_data.get('event')
                    Report.data = dict_data.get('data')
                    # handle msg from engine
                elif 'response' in data and 'result' in data:
                    dict_data = json.loads(data[10:])
                    Report.event = None
                    Report.data = dict_data.get('result')
                elif data == tinyrpc.FCT_HEARTBEAT:
                    Report.event = events.FCT_HEARTBEAT
                    Report.data = data

                if int(level) <= self.level:
                    self.write_out('[' + ts + ']\t' + origin + ':' + Report.data)
            except Exception as e:
                logger.info('exception is thrown while parsing data: {0}'.format(e))
        else:
            self.write_out(str(msg))

            self.getName()
'''
    def getstatus(self):
        return self.status

    def setstatus(self, stat):
        self.status = stat
'''


class SubscriberManager(object):
    def __init__(self):
        self.listeners = []

    def start_all(self):
        for listener in self.listeners:
            listener.start()

    def add_listener(self, subscriber):
        if isinstance(subscriber, Subscriber):
            self.listeners.append(subscriber)


class Report(object):

    event = ""
    data = ""
