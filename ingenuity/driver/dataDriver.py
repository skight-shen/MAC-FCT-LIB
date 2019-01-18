import serial
import sys, datetime,time, os, threading
from ingenuity.loggers import ZmqPublisher
from ingenuity import zmqports
import zmq, logging
import socket
    
class TcpClient(object):
    def __init__(self, addr=('127.0.0.1', 7643)):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.__socket.settimeout(1)
        self.__id = '0'
        self.__address = addr

    def connect(self):
        erro_code = self.__socket.connect_ex(self.__address)
        time.sleep(0.01)
        if erro_code == 0:
            return True
        else:
            return False

    def close(self):
        self.__socket.shutdown(socket.SHUT_RDWR)
        self.__socket.close()
        time.sleep(0.1)
        return True

    def sendMsg(self, send_msg):
        t = datetime.datetime.now()
        ts = datetime.datetime.strftime(t, '%m-%d_%H:%M:%S.%f')
        try:
            send_msg = send_msg + '\r\n'
            print str(ts) +' [sending]: ' + send_msg
            data_len = self.__socket.send(send_msg)
            if data_len < len(send_msg):
                logging.info('Network is busy, pip broken.')
            else:
                return data_len
        except Exception as e:
            print e.message

    def recvMsg(self):
        t = datetime.datetime.now()
        ts = datetime.datetime.strftime(t, '%m-%d_%H:%M:%S.%f')
        buf = ''
        while 1:
            try:
                buf += self.__socket.recv(1024)
                if buf != "" and buf[-1] == "\n":
                    print str(ts) + '[Recived]:' + buf
                    return buf
            except:
                raise Exception("Failed to receive msg by socket")


    def req_recv(self, msg):
        self.sendMsg(msg)
        result = self.recvMsg()
        return result


#TcpServer is running in Xaview. It's only for testing here.
class TcpServer(object):
    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect(self):
        self.__socket.bind(('127.0.0.1', 7643))
        self.__socket.listen(10)
        logging.info('waiting for connection......')
        while 1:
            session, address = self.__socket.accept()
            t = threading.Thread(target=self.tcplink, args=(session, address))
            t.start()

    def tcplink(self, sock, addr):
        print 'Accept new connection from %s: %s ...'% addr
        sock.send(u'Welcome!')
        while True:
            data = sock.recv(1024)
            time.sleep(1)
            if not data or 'exit' in data:
                break
            else:
                print data
                sock.send('OK\r\n')
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
        sock.close()
        print('Connection from %s:%s closed.' % addr)


class SerialDriver(object):
    def __init__(self, dict_cfg, site):
        self.__serialPort = serial.Serial()
        self.__serialPort.port = dict_cfg.get('port', '/dev/cu.usbserial-usbvdm32')
        self.__serialPort.baudrate = dict_cfg.get('baudrate', 115200)
        self.__serialPort.parity = dict_cfg.get('parity', serial.PARITY_NONE)
        self.__serialPort.bytesize = dict_cfg.get('bytesize', serial.EIGHTBITS)
        self.__serialPort.stopbits = dict_cfg.get('stopbits', serial.STOPBITS_ONE)
        self.__serialPort.timeout = dict_cfg.get('timeout', 2)
        self.end_str = dict_cfg.get('end_str', '\r')

        self.detection = u':-)'

        ctx = zmq.Context().instance()

        self.publisher = ZmqPublisher(
            ctx,
            "tcp://*:" + str(zmqports.UART_PUB + site),
            "Nanohippo_{}".format(site)
        )

    def connect(self):
        if not self.__serialPort.isOpen():
            try:
                self.__serialPort.open()
                print 'Successfully Connected to Fixture by Serial port:{}'.format(self.__serialPort.port)
            except Exception as e:
                print 'Failed to connect to fixture by serial port:{}\r\n Erro message is:{}'.format(self.__serialPort.port, e.message)

        return self.__serialPort.is_open

    def close(self):
        if self.__serialPort.is_open():
            self.__serialPort.close()
        return self.__serialPort.is_open()

    def sendMsg(self, send_msg):
        nLen = ''
        send_msg += self.end_str
        if self.__serialPort.is_open:
            try:
                self.__serialPort.flushInput()
                nLen = self.__serialPort.write(send_msg)
                print "[Sending:] " + send_msg
                self.publisher.publish("[Sending:] " + send_msg)
                return nLen
            except Exception as e:
                print "Error message: %s" % e.message
                return nLen

    def recvMsg(self):
        recv_data = ''
        try:
            if self.__serialPort.is_open:
                #time.sleep(0.5)
                while self.__serialPort.inWaiting():
                    recv_data = self.__serialPort.read_all()
                print "[Received:] " + recv_data
                self.publisher.publish("[Received:] " + recv_data)
        except Exception as e:
            print 'Failed to receive message. \r\n %s' % e.message
        return recv_data

    def req_recv(self, send_msg):
        self.sendMsg(send_msg)
        time.sleep(0.5)
        return self.recvMsg()

    def WaitDetect(self, nTimeout):
        startTime = time.time()
        nRet = -2
        strRet = self.recvMsg()
        while time.time()-startTime < nTimeout:
            if self.detection in strRet:
                nRet = 0
                break
            elif r':-)' in strRet:
                nRet = -1
                break
            strRet = self.recvMsg()
        return nRet