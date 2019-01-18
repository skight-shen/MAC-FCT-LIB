# coding:utf-8

import serial
import serial.tools.list_ports as pts
#
#
# plist = list(pts.comports())
#
# if len(plist) <= 0:
#     print "没有发现端口"
# else:
#     for port in plist:
#         print port
#



config = {
    "port":"/dev/cu.usbserial-A5016SCA",
    "baudrate":"115200",
    "bytesize":8,
    "parity":'N',
    "stopbits":1,
    "timeout":2
}

class SerialDriver(object):
    """
    """

    def __init__(self, cfg=config):
        super(SerialDriver, self).__init__()
        self.__session = serial.Serial()
        self.cfg = cfg
        self.status = False

    def connect(self):
        if not self.__session.isOpen():
            try:
                self.__session.timeout = self.cfg['timeout']
                self.__session.baudrate = self.cfg['baudrate']
                self.__session.port = self.cfg['port']
                self.__session.stopbits = self.cfg['stopbits']
                self.__session.bytesize = self.cfg['bytesize']
                self.__session.parity = self.cfg['parity']
                self.__session.xonxoff = 0
                self.__session.open()
                self.status = True
                print 'COM is open'
            except Exception as e:
                print e
                print 'COM Open Fail!!!'

    def writeCommand(self, msg):
        if self.status:
            self.__session.write(msg)

    def readBuffer(self):
        buf = self.__session.readlines(self.cfg['timeout'])
        return buf

    def write_read(self,msg):
        self.writeCommand(msg)
        return self.readBuffer()


    def close(self):
        if self.__session.isOpen():
            try:
                self.__session.close()
                self.status = False
                print 'COM Closed'
            except Exception as e:
                print e
                print 'COM Close Fail!!!'

    def getPort(self):
        plist = list(pts.comports())

        if len(plist) <= 0:
            print "没有发现端口"
        else:
            for port in plist:
                print port



#
# import time
# a = SerialDriver(config)
# a.connect()
# for i in range(1000):
#     req = a.write_read("FIXTURE STATUS\r\n")
#     print "当前次数{0},内容是{1}".format(i,req)
#
# a.close()