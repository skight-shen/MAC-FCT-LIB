import socket
import time
import struct

from Common.BBase import *
class TcpDriver(object):
    """"
    TcpDriver is a non-blocking socket client
    not recommand to use this class to initialize a TcpDriver
    please use DriverManger to initialize Driver
    ----------------------------------------------------------
    args:
        cfg(dict):
            config format like blow
            cfgSample = {
                'type':'tcp'
                'endStr':'smu',
                'id':'123456',
                'ip':'192.168.99.66',
                'port':7600
            }

    """

    # TODO:add timeout sa self.timeout,beacause I need use self.timeout to computer the real timeout.
    def __init__(self, cfg):
        super(TcpDriver, self).__init__()
        self.cfg = cfg
        self.timeout = 0.2
        self.Id = cfg['id']
        self.endStr = self.cfg['endStr']
        self.netCfg = (self.cfg['ip'], self.cfg['port'])

        objChell = cShell()
        objChell.RunShell_n("ping {} -c 2 -t 2".format(self.cfg['ip']))
        self.status = False
        self._session = None


    def connect(self):
        bRet = True
        bRet = self.disconnect()
        try:
            self._session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._session.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self._session.settimeout(self.timeout)
        except Exception as e:
            bRet = False
        try:
            if self._session.connect_ex(self.netCfg)==0:
                self.status = True
            else:
                self.status = False
        except Exception as e:
            bRet = False
        time.sleep(0.01)
        return bRet
        # print(str(self.netCfg) + ' fail')

    def disconnect(self):
        if self._session and self.status:
            self._session.shutdown(socket.SHUT_RDWR)
            self._session.close()
            del self._session
            self.status = False
            self._session = None
            time.sleep(0.01)
        return True

    def sendMsg(self, command, **kwargs):
        if not self.status:
            self.connect()
        if self.status:
            command += self.endStr
        else:
            print "Exception('disconnect')"
            #raise Exception('disconnect')
        try:
            send = self._session.send(command)
            if send <= 0:
                raise RuntimeError('Pip Broken')
        except Exception as e:
            print "Exception {}".format(e)
            #raise e

    def sendMCU(self, command):
        if not self.status:
            self.connect()
        if self.status:
            try:
                self._session.send(command)
            except Exception as e:
                raise e

    # TODO change the recv func of TCP
    # IN OUT take
    def recvMsg(self, tm=10000):
        buf = ''
        size = 1024
        t = int(tm / (self.timeout * 1000))
        failtime = 0
        while True:
            try:
                rev = self._session.recv(size)
                buf += rev
                if buf[-1] == "\n" and buf != "":
                    self.disconnect()
                    return buf
            except Exception as e:
                if failtime >= t:
                    self.disconnect()
                    print(e)
                    print('get buf:' + buf)
                    break
                    #raise e
                else:
                    failtime += 1
                    continue

    def req_recv(self, command):
        result = None
        self.sendMsg(command)
        try:
            result = self.recvMsg()
        except:
            raise Exception('cmd:' + command + ' error')
        if result != None:
            return result
        if result == '':
            raise Exception('no result')

    # TODO change the recvData driver
    def recvData(self, tm, flag, transport):
        buf = ''
        size = 4096
        t = int(tm / (self.timeout * 1000))
        failtime = 0
        while True:
            try:
                buf += self._session.recv(size)
            except Exception as e:
                if failtime >= t:
                    self.disconnect()
                    print(e)
                    raise Exception("Time Out")
                else:
                    failtime += 1
                    if flag in buf and buf != "":
                        self.disconnect()
                        return buf
                    transport.check_heartbeat()

    def clear_buf(self):
        # self._session.close()
        # cfg = self.cfg
        # self.__init__(cfg)
        buf = ''
        size = 1024 * 10
        failtime = 0
        while True:
            try:
                buf = self._session.recv(size)
                if buf == "":
                    return True
            except Exception:
                if failtime >= 5:
                    self.disconnect()
                    return False
                else:
                    failtime += 1
                    if buf == "":
                        self.disconnect()
                        return True

    def recv_bin(self, length, driver):
        if self.status != True:
            # print('reconnect')
            self.connect()
        buf = ''
        size = 4096
        failtime = 0
        # self.clear_buf()
        # self._session.shutdown('SHUT_RDWR')
        msg = driver.req_recv('>AUDIO_RAW_DATA(16384)\r\n')
        # print(msg)
        # time.sleep()
        while len(buf) < length * 4:
            try:
                buf += self._session.recv(size)
            except Exception as e:
                failtime += 1
                # print(len(buf))
                # print(e)
                time.sleep(0.5)
                if failtime > 100:
                    self.disconnect()
                    raise Exception('time out')
        bufSize = len(buf)
        print(bufSize)
        data = struct.unpack('>' + 'f' * (bufSize / 4), buf)
        if bufSize / 4 > length or bufSize / 4 < length:
            with open(str(bufSize) + '.txt', 'a') as f:
                f.write(buf)
        # self._session.shutdown(socket.SHUT_RDWR)
        # self.close()
        return data

    def close(self):
        self._session.close()
        self.status = False

    @property
    def getSocket(self):
        return self._session
