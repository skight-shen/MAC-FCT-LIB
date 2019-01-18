#coding=utf-8
import time
import Common.levels as levels
import json
import Common.events as events
import zmq
from TestUI.GUI.module.Treemodel import TreeItem

class Report(object):

    event = None
    data = None

    def _to_dict(self):
        jdata = dict(event=self.event, data=self.data)
        return jdata

    def serialize(self):
        return json.dumps(self._to_dict())

    def __repr__(self):
        r_str = 'event=' + events.get_name(self.event) + '; data=' + str(self.data)
        return r_str




class ReporterProtocol(object):

    @staticmethod
    def parse_report(msg):
        print "Check Coming Message {}".format(msg)
        if 'data' in msg and 'event' in msg and 'response' not in msg :
            report_dict = json.loads(msg)
            report = Report()
            report.event = report_dict['event']
            report.data = report_dict['data']
            return report
        elif 'data' in msg and 'event' in msg and 'result' in msg and "AMIOK ERROR" in msg:
            print "Check Coming Message SFC {}".format(msg)
            report_dict = json.loads(msg)
            report = Report()
            report.event = report_dict['event']
            report.data = report_dict['data']
            print "Check Return SFC Report {}".format(report)
            return report
        elif 'response' in msg and 'result' in msg :
            try:
                report_dict = json.loads(msg[10:])
                report = Report()
                report.data = report_dict['result']
                if isinstance(report_dict['result'],list):
                    report.event = events.LIST_ALL #add a new event
                else:
                    report.event = events.STATEMATHINE
                return report
            except Exception:
                pass
        elif 'FCT_HEARTBEAT' in msg:
            report = Report()
            report.data = msg
            report.event = events.HEATBEAT
            return report






        # else:
        #     print 'illegal report: {}'.format(msg)
        #     return None




# class ReportListener(Thread):
#     def __init__(self, port, url=None):
#         super(ReportListener, self).__init__()
#         ctx = zmq.Context.instance()
#         self.subscriber = ctx.socket(zmq.SUB)
#         if url is None:
#             url = 'tcp://localhost:' + str(port)
#         self.subscriber.connect(url)
#         self.url = url
#         self.subscriber.setsockopt(zmq.SUBSCRIBE, zmqports.PUB_CHANNEL)
#         self.receiving = True
#         self.level = levels.REPORTER #DEBUG REPORTER
#         self.listeners = []
#
#     def run(self):
#         protocol = ReporterProtocol()
#         self.receiving = True
#         print 'ready to subscribe to ' + str(self.url)
#         while self.receiving:
#             try:
#                 topic, ts, level, origin, data = self.subscriber.recv_multipart(zmq.NOBLOCK)
#                 if int(level) >= self.level:    # process Reporter message only
#                     for listener in self.listeners:
#                         listener.received(protocol.parse_report(data))
#             except zmq.ZMQError:
#                 pass
#             time.sleep(0.02)
#         self.subscriber.setsockopt(zmq.LINGER, 0)
#         self.subscriber.close()


# add by 20180304
from PyQt5.QtCore import QObject,pyqtSignal,QThread
import Common.zmqports as zmqports
import threading



class SmFixture(QThread):

    sig = pyqtSignal(str)
    def __init__(self, port=zmqports.SM_PUB,url=None):
        super(SmFixture, self).__init__()
        ctx = zmq.Context.instance()
        self.subscriber = ctx.socket(zmq.SUB)
        self.port = port
        if url is None:
            url = 'tcp://localhost:' + str(self.port)
        self.subscriber.connect(url)
        self.url = url
        self.subscriber.setsockopt(zmq.SUBSCRIBE, zmqports.PUB_CHANNEL)
        self.receiving = False

    def run(self):
        self.receiving = True
        print 'ready to subscribe to SMFixture'
        while self.receiving:
            try:
                topic, ts, level, origin, data = self.subscriber.recv_multipart(zmq.NOBLOCK)
                self.sig.emit("[{}--{}] : {}".format(ts, origin, data))
                #if origin == "StateMachine" and "FIXTURE" in data:
            except zmq.ZMQError:
                pass
            time.sleep(0.05)
        self.subscriber.setsockopt(zmq.LINGER, 0)
        self.subscriber.close()




class ReportListener(QThread):

    sig = pyqtSignal(dict)
    sig2 = pyqtSignal(str)
    def __init__(self, port,url=None):
        super(ReportListener, self).__init__()
        ctx = zmq.Context.instance()
        self.subscriber = ctx.socket(zmq.SUB)
        self.port = port
        if url is None:
            url = 'tcp://localhost:' + str(self.port)
        self.subscriber.connect(url)
        self.url = url
        self.subscriber.setsockopt(zmq.SUBSCRIBE, zmqports.PUB_CHANNEL)
        self.receiving = True
        self.list = False
        self._ready = True
        self._start = False
        self.result = -1
        if self.port == 6250:
            self._col = 5
        elif self.port == 6251:
            self._col = 6
        elif self.port == 6252:
            self._col = 7
        elif self.port == 6253:
            self._col = 8


    def run(self):
        protocol = ReporterProtocol()
        self.receiving = True
        print 'ready to subscribe to ' + str(self.url)
        while self.receiving:
            try:

                topic, ts, level, origin, data = self.subscriber.recv_multipart(zmq.NOBLOCK)
                self.received(protocol.parse_report(data))
                self.sig2.emit("[{}--{}] : {}".format(ts,origin,data))
            except zmq.ZMQError:
                pass
            time.sleep(0.01)
        self.subscriber.setsockopt(zmq.LINGER, 0)
        self.subscriber.close()


    def get_start_status(self):
        return self._ready

    def set_start_status(self,value):
        self._ready = value


    def get_start(self):
        return self._start

    def set_start(self,value):
        self._start = value

    def received(self, report):
        sig_dict = {}
        if report == None :
            return None
        if report.event == events.LIST_ALL:
            print "LIST_ALL {}".format(report.data)
            data=[]
            if self.list == False:
                for row in report.data[1:]:
                    t = eval(row[1])
                    t["row"] = str(row[0])
                    data.append(t)
                sig_dict.setdefault("event",events.LIST_ALL)
                sig_dict.setdefault("result",data)

            else:
                return None
        elif report.event == events.ITEM_FINISH:
            sig_dict.setdefault("event", events.ITEM_FINISH)
            sig_dict.setdefault("value", report.data.get("value"))
            sig_dict.setdefault("result", report.data.get("result"))
            sig_dict.setdefault("error", report.data.get("error"))
            sig_dict.setdefault("tid", report.data.get("tid"))
            sig_dict.setdefault("col", self._col)

        elif report.event == events.SEQUENCE_END:
            sig_dict.setdefault("event",events.SEQUENCE_END)
            sig_dict.setdefault("result",report.data['result'])
            sig_dict.setdefault("name", self.port)
            self.set_start_status(True)
        elif report.event == events.ITEM_START:
            #print "ITEM_START {}".format(report.data)
            sig_dict.setdefault("event", events.ITEM_START)
            sig_dict.setdefault("group", report.data['group'])
            sig_dict.setdefault("tid", report.data['tid'])
            sig_dict.setdefault("col", self._col)
            sig_dict.setdefault("name", self.port)
        elif report.event == events.UOP_DETECT:
            print "MESSAGE RECIVE {}".format(report)
            sig_dict.setdefault("event",events.UOP_DETECT)
            sig_dict.setdefault("result",report.data['error'])
            self.set_start_status(True)
        elif report.event == events.HEATBEAT:
            sig_dict.setdefault("event",events.HEATBEAT)
            sig_dict.setdefault("name", self.port)
        elif report.event == events.SEQUENCE_START:
            #print "SEQUENCE_START {}".format(report.data)
            self.set_start_status(False)
            self.set_start(True)
            sig_dict.setdefault("event",events.SEQUENCE_START)
            sig_dict.setdefault("name", self.port)
            sig_dict.setdefault("col",self._col)
        elif report.event == events.STATEMATHINE:
            sig_dict.setdefault("event", events.STATEMATHINE)
            sig_dict.setdefault("name", self.port)
            sig_dict.setdefault("data",report.data)
        self.sig.emit(sig_dict)



class SubcribeManagement(QObject):

    seq_port = 	{'seq1':zmqports.SEQUENCER_PUB,'seq2':zmqports.SEQUENCER_PUB+1,'seq3':zmqports.SEQUENCER_PUB+2,'seq4':zmqports.SEQUENCER_PUB+3}
    engine_port = {'eng1':zmqports.TEST_ENGINE_PUB,'eng2':zmqports.TEST_ENGINE_PUB+1,'eng3':zmqports.TEST_ENGINE_PUB+2,'eng4':zmqports.TEST_ENGINE_PUB+3}
    logger_port = {'logger':zmqports.LOGGER_PUB}
    def __init__(self, parent=None):
        super(SubcribeManagement, self).__init__(parent)
        self.parent = parent
        self.seq = dict()
        self.engine = dict()
        self.logger = dict()
        self.sm = dict()
        self._finishedflag = False


    def start_one_threadding(self,port):
        return ReportListener(port)


    def check(self):
        if self._finishedflag:
            self._finishedflag = False
            return False
        else:
            if self.get_status():
                self._finishedflag = True
                return True


    def start_all_threading(self):
        for key in self.seq_port:
            self.seq[key] = self.start_one_threadding(self.seq_port[key])
            self.seq[key].start()
        for key in self.engine_port:
            self.engine[key] = self.start_one_threadding(self.engine_port[key])
            self.engine[key].start()
        for key in self.logger_port:
            self.logger[key] = self.start_one_threadding(self.logger_port[key])
            self.logger[key].start()




    def get_start(self):
        for key in self.seq:
            if self.seq[key].get_start()==True:
                return True
        return False

    def get_status(self):
        for key in self.seq:
            if self.seq[key].get_start_status()==False:
                return False
        return True



    def set_all_status(self,value):
        for key in self.seq:
            self.seq[key].set_start_status(value)

    def set_all_start(self, value):
        for key in self.seq:
            self.seq[key].set_start(value)

    def connect_all_signal(self,f):
        for key in self.seq:
            self.seq[key].sig.connect(f)
        for key in self.engine:
            self.engine[key].sig.connect(f)
        for key in self.logger:
            self.logger[key].sig.connect(f)

    def connect_engine(self,name,f):
        self.engine[name].sig2.connect(f)

    def set_level(self,status=False):
        for key in self.seq:
            self.seq[key].list = status










