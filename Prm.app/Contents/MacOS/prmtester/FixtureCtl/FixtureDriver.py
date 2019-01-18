#!/usr/bin/env python
# encoding=utf-8

import serial
import serial.tools.list_ports as pts
import os
import json
import binascii
import time

plist = list(pts.comports())

if len(plist) <= 0:
    print "没有发现端口"
else:
    for port in plist:
        print port


class DriverFactor(object):

    def connect(self):
        pass

    def sendMsg(self, command):
        pass

    def recvMsg(self, dt=None):
        pass

    def req_recv(self, command):
        pass

    def close(self):
        pass

    @property
    def getSocket(self):
        pass


class SerialDriver(DriverFactor):

    def __init__(self):
        super(SerialDriver, self).__init__()
        self.__session = serial.Serial()
        self.fixture_cfg = {}
        self.end_str = ''
        self.status = ""
        self.load_config()

    def load_config(self, config_file='fixture_config.json'):
        path = os.path.join(os.path.split(__file__)[0], config_file)
        cfg = os.path.abspath(path)
        if os.path.exists(path):
            with open(cfg, 'r') as f:
                config = json.load(f)
            self.fixture_cfg = config['fixture']['uart']

    def connect(self):
        if not self.__session.isOpen():
            try:
                self.__session.timeout = self.fixture_cfg['timeout']
                self.__session.baudrate = self.fixture_cfg['baud_rate']
                self.__session.port = self.fixture_cfg['port']
                self.__session.stopbits = self.fixture_cfg['stop_bits']
                self.__session.bytesize = self.fixture_cfg['byte_size']
                self.__session.parity = self.fixture_cfg['parity']
                self.__session.xonxoff = 0
                self.__session.open()
                self.status = True
                self.end_str = self.fixture_cfg['end_str']
                print ('Fixture Connected.', self.fixture_cfg.get('port'))
            except Exception as e:
                print ('fixture connect failed ', e)

        return self.__session.is_open

    def sendMsg(self, command):
        if self.status:
            try:
                self.__session.write(command)
                time.sleep(0.3)
            except Exception as e:
                raise e

    def recvMsg(self, dt=None):
        buf = ''
        if self.__session.isOpen() and self.__session.inWaiting():
            try:
                buf = self.__session.read(self.__session.inWaiting())
            except:
                raise Exception(self.__class__.__name__ + "recMsg Error")
        if dt == 'hex':
            buf = binascii.b2a_hex(buf)
        self.status = buf
        return buf

    def req_recv(self, command):
        result = None
        if self.status:
            self.sendMsg(command)
            time.sleep(0.05)
            while True:
                if self.__session.inWaiting():
                    result = self.recvMsg()
                    return result
                time.sleep(0.05)
        return result

    def isOpen(self):
        return self.__session.isOpen()

    def isWaiting(self):
        return self.__session.inWaiting()

    def close(self):
        self.__session.close()
        self.status = False

    @property
    def getSocket(self):
        return self.__session
