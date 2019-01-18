from ingenuity.driver.dataDriver import SerialDriver
import os, sys, time, datetime
import threading
import tkMessageBox
import Tkinter

cfg = {
    'port' : '/dev/cu.usbserial-usbvdm32',
    'baudrate' :  115200,
    'parity' : 'N',
    'bytesize' : 8,
    'stopbits' : 1,
    'timeout' : 2,
    'end_str' : '\r\n'
}


class Client(threading.Thread):
    def __init__(self):
        super(Client, self).__init__()
        self.serialDriver = SerialDriver(cfg,0)
        self.serving = self.serialDriver.connect()

    def test_sendMsg(self, send_msg):
        self.serialDriver.sendMsg(send_msg)

    def test_recvMsg(self):
        strRet = self.serialDriver.recvMsg()
        return strRet

    def req_recv(self,send_msg):
        strRet = self.serialDriver.req_recv(send_msg)
        return strRet

    def run(self):
        while self.serving:
            send_msg = raw_input("[Inputting:]")
            self.req_recv(send_msg)

if __name__ == '__main__':
    serialClient = Client()
    serialClient.start()
