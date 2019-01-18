#!/usr/bin/env python
#encoding=utf-8

import zmq
import re
import logging


import  Common.tinyrpc.transports.zmq as tinyrpc_zmq


class Fixture(object):
    def __init__(self, ser, publisher):

        self.need_uart_flg = True
        
        self.publisher = publisher
        self.req_timeout = 1000 #3secs
        self.ser = ser
        self.loop_test_flg = True 
    
    def setLoopTestFlg(self, flg):
        self.loop_test_flg = flg
        
    def getLoopTestFlg(self):
        return self.loop_test_flg


    def setNeedUartFlg(self, flg):
        self.need_uart_flg = flg

    def getNeedUartFlg(self):
        return self.need_uart_flg

    
    def sendMsg(self, msg):
        logging.info("msg will be send to fixture is: %s", msg)
        
        if self.need_uart_flg:
            resp = self.ser.write_read(msg)
            logging.info("msg received from fixture is: %s", resp)
            return resp
        else:
            return None
    
    
    def sendCmd(self, cmd):
        return self.sendMsg(cmd + "\r\n")
    
    def close(self):
        #self.sendCmd("in")
        #self.ser.connect()
        print 'close'
        pass

    
    def press(self):
        #self.sendCmd("down")
        #self.ser.getPort()
        print 'press'
        pass
    
    
    def release(self):
        logging.info("fixture loop mode is: %s", str(self.loop_test_flg))
        if self.loop_test_flg:
            #self.sendCmd("out")
            print 'out'
        else:
            #self.sendCmd("release")
            print 'release'
        pass
    
    def open(self):
        #self.sendCmd("out")
        #self.ser.close()
        print 'open'
        pass
        
        
    def getFixtureID(self):
#         reply_msg = self.sendCmd("readid")
# #         result = re.match(r"ReadID[\s\t](.+)[\r\n])", reply_msg)
# #         result = result.group(0) if result else result
#
#         return reply_msg
        pass
    
    
    
    
if __name__ == '__main__':
    pass
