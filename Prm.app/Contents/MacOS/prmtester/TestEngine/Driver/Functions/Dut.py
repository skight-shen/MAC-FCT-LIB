from Common.tinyrpc.dispatch import public
import serial
import time
import binascii


class Dut(object):
    def __init__(self, cfg, publisher=None):
        super(Dut, self).__init__()
        # publisher for publish all communication data
        self.pub = publisher
        self.cfg = cfg
        self.__session = serial.Serial()
        self.status = False
        try:
            self.connect()
        except Exception as e:
            raise e

    def log(self, msg):
        self.pub.publish(msg)

    def connect(self):
        self.close()
        time.sleep(1)
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
                self.end_str = "\r\n"
                print ('%s Connected.' % self.cfg.get('port'))
            except Exception as e:
                print ('%s connect failed.' % self.cfg.get('port'))
                print(e)

        return self.__session.is_open

    @public('diags')
    def diags(self, *args, **kwargs):
        return '--PASS--'

    @public('tbd')
    def tbd(self, *args, **kwargs):
        return '--PASS--'

    @public('send')
    def send(self, *args, **kwargs):
        result = ''
        for _ in range(2):
            result = self.req_recv(str(args[0]) + '\r\n')
            if result:
                break
            time.sleep(1)
        print(result)
        if 'DONE' in result:
            return '--PASS--'
        else:
            return '--FAIL--'

    def close(self):
        if self.__session.isOpen():
            try:
                self.__session.close()
                self.status = False
                print(self.__session.port + ' disconnect')
            except Exception as e:
                print e
                print 'COM Close Fail!!!'

    def send_msg(self, command):
        if self.status:
            try:
                self.__session.write(command.encode("utf-8"))
                self.log(command)
                print('seraial send: %s' % command)
                time.sleep(0.3)
            except Exception as e:
                raise e

    def recv_msg(self, dt=None):
        buf = ''
        if self.__session.isOpen() and self.__session.inWaiting():
            try:
                buf = self.__session.read(self.__session.inWaiting())
                print('seraial send: %s' % buf)
                self.log(buf)

            except Exception as e:
                print(e)
                self.log(e)
                raise Exception(self.__class__.__name__ + "recMsg Error")
        if dt == 'hex':
            buf = binascii.b2a_hex(buf)
        self.status = buf
        return buf

    def req_recv(self, command):
        result = None
        self.connect()
        if self.status:
            self.send_msg(command)
            time.sleep(0.05)
            # result = self.__session.readlines(2)
            while True:
                if self.__session.inWaiting():
                    result = self.recv_msg()
                    return result
                time.sleep(0.05)
        return result

    def isOpen(self):
        return self.__session.isOpen()

    def isWaiting(self):
        return self.__session.inWaiting()

    def getSocket(self):
        return self.__session
