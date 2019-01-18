#!/usr/bin/env python
# encoding=utf-8

import zmq
import re
import logging

from threading import Thread

import Common.tinyrpc.transports.zmq as tinyrpc_zmq

import time


class Fixture(Thread):
    def __init__(self, ser, publisher):
        super(Fixture, self).__init__()

        self.need_uart_flg = True

        self.publisher = publisher
        self.ser = ser
        self.loop_test_flg = True
        self.receiving = False
        self.status = ""
        self.command = ""
        self.recv_msg = ''
        self.start()

    def run(self):
        self.open()
        time.sleep(0.5)
        self.receiving = True
        while self.receiving:
            try:
                if self.ser.status:
                    if self.command == "":
                        rep = self.ser.recvMsg()
                    else:
                        rep = self.ser.req_recv(self.command)
                        self.recv_msg = rep
                        self.command = ""
                    if rep:
                        print (self.recv_msg)

                    if "FIXTURE" in rep:
                        if "FIXTURE OUT" in rep:
                            self.status = "OUT"
                        elif "FIXTURE DOWN" in rep:
                            self.status = "DOWN"
                        elif "FIXTURE UP" in rep:
                            self.status = "UP"
                        self.publisher.publish(rep)
                else:
                    pass
                    # print "serial port issue"
            except Exception:
                self.open()
            time.sleep(0.5)
        self.close()

    def setLoopTestFlg(self, flg):
        self.loop_test_flg = flg

    def getLoopTestFlg(self):
        return self.loop_test_flg

    def setNeedUartFlg(self, flg):
        self.need_uart_flg = flg

    def getNeedUartFlg(self):
        return self.need_uart_flg

    #
    # def sendMsg(self, msg):
    #     #logging.info("msg will be send to fixture is: %s", msg)
    #
    #     if self.need_uart_flg:
    #         resp = self.ser.sendMsg(msg)
    #         #logging.info("msg received from fixture is: %s", resp)
    #
    # def sendCmd(self, cmd):
    #     return self.sendMsg(cmd + "\r\n")

    def close(self):
        self.ser.close()

    def press(self):
        if self.status == "DOWN":
            return
        self.command = "FIXTURE IN\r\n"
        self.waitforpress()

    def control(self, cmd):

        self.command = cmd + "\r\n"
        print self.command
    def release(self):
        if self.status == "OUT":
            return
        self.command = "FIXTURE OUT\r\n"
        self.waitforrelease()

    def waitforpress(self):
        t = 0
        while True:
            if t < 10:
                if self.status == "DOWN":
                    break
                self.command = "FIXTURE IN\r\n"
                time.sleep(0.5)
                t += 1
            else:
                self.publisher.publish("FIXTURE " + self.__class__.__name__ + "waitforpress press timeout!")
                break

    def waitforrelease(self):
        t = 0
        while True:
            if t < 10:
                if self.status == "OUT":
                    break
                self.command = "FIXTURE OUT\r\n"
                time.sleep(0.5)
                t += 1
            else:
                self.publisher.publish("FIXTURE " + self.__class__.__name__ + "waitforrelease press timeout!")
                break

    def getFixtureStatus(self):
        return self.status

    def open(self):
        # self.ser.close()
        self.ser.connect()

    def getFixtureID(self):
        #         reply_msg = self.sendCmd("readid")
        # #         result = re.match(r"ReadID[\s\t](.+)[\r\n])", reply_msg)
        # #         result = result.group(0) if result else result
        #
        #         return reply_msg
        pass


if __name__ == '__main__':
    pass
