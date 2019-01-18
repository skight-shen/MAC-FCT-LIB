from TcpDriver import TcpDriver
from threading import Thread
import time

cfg = {
    "type": "tcp",
    "id": "123456",
    "endStr": "\r\n",
    "ip": "169.254.1.32",
    "port": 7621
}
import time
import socket

class Datalogger(Thread):
    def __init__(self):
        super(Datalogger, self).__init__()
        self.logger = TcpDriver(cfg)
        self.logger.connect()
        self.bRun=True
        self.size=0

        self._session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._session.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        ret = self._session.connect_ex(("169.254.1.32", 7621))
        print ret




    def run(self):
        print "Start "
        while self.bRun:
            #print 1
            try:
                data = self._session.recv(20480000)
                self.size+=1

            except Exception as e:
                print(e)
    def Stop(self):
        self.bRun=False
        print "  Last Size {}".format(self.size)


if __name__ == "__main__":
    logger1 = Datalogger()
    logger1.start()
