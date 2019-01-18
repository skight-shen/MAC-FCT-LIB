import time
import zmq
import sys
import os
import sched

sys.path.append(os.getcwd())

if not __package__:
    path = os.path.join(os.path.dirname(__file__), os.pardir)
    sys.path.insert(0, path)

from threading import Thread
from Common.tinyrpc.transports.zmq import ZmqServerTransport
from Common.publisher import ZmqPublisher
from Common import zmqports

from Common.BBase import *

from Log.LogClient import LogClient

from LockBase import *

class cLockManager:
    def __init__(self):
        self.dictLockQueen    = {}
        self.ThreadLock = cBaseThreadLock()

    def GetInfo(self):
        return self.dictLockQueen

    def Lock(self,strGrounp,strItem):
        strRet = ""
        if strGrounp not in self.dictLockQueen.keys():
            self.ThreadLock.Lock(True)
            self.dictLockQueen[strGrounp] = []
            self.ThreadLock.Lock(False)
        if strItem not in self.dictLockQueen[strGrounp]:
            self.ThreadLock.Lock(True)
            self.dictLockQueen[strGrounp].append(strItem)
            self.ThreadLock.Lock(False)
        strRet = str(self.dictLockQueen[strGrounp].index(strItem))

        return strRet
    def UnLock(self,strGrounp,strItem):
        strRet = ""
        if strGrounp in self.dictLockQueen.keys():
            if strItem in self.dictLockQueen[strGrounp]:
                strRet = str(self.dictLockQueen[strGrounp].index(strItem))
                self.ThreadLock.Lock(True)
                self.dictLockQueen[strGrounp].remove(strItem)
                self.ThreadLock.Lock(False)

        return strRet

class LockServer(Thread):
    objLockManager = cLockManager()
    objLog =  LogClient("Lock", "LockSever.log")
    def __init__(self):
        super(LockServer, self).__init__()
        ctx = zmq.Context()

        listen_addr = "tcp://*:" + str(zmqports.PRM_LOCK_PORT)
        pub_addr    = "tcp://*:" + str(zmqports.PRM_LOCK_PUB)

        self.frontend = ctx.socket(zmq.ROUTER)
        self.frontend.bind(listen_addr)

        self.publisher = ZmqPublisher(ctx, pub_addr, "PRMLOCK")
        self.transport = ZmqServerTransport(self.frontend)
        self.transport.publisher = self.publisher



        self.serving = True

    def StopSever(self):
        self.serving = False
    def run(self):
        self.objLog.Trace("Start Prm Lock Sever Success!!")
        while self.serving:
            context, message = self.transport.receive_message()
            if message:
                self.objLog.Trace("Get Message {}".format(message))
                objProtocal = cProtocal(message)
                strCmd= objProtocal.GetCmd()
                strLockGrounp = objProtocal.GetLockGrounp()
                strLockItem   = objProtocal.GetLockItem()

                self.objLog.Trace("Get Parse {} {} {}".format(strLockGrounp,strLockItem,strCmd))
                if strCmd and strLockGrounp and strLockItem and  strCmd=="lock" :

                    strRet = self.objLockManager.Lock(strLockGrounp,strLockItem)


                    self.transport.send_reply(context, str(strRet))
                    self.objLog.Trace("Lock {} {} {}".format(strLockGrounp, strLockItem, strRet))


                elif strCmd and strLockGrounp and strLockItem and  strCmd=="unlock" :
                    strRet = self.objLockManager.UnLock(strLockGrounp,strLockItem)
                    self.transport.send_reply(context, str(strRet))
                    self.objLog.Trace("UnLock {} {} {}".format(strLockGrounp, strLockItem, strRet))
                else:
                    self.objLog.Trace("Sever Get Message Error : {}".format(message))
                del objProtocal

        print("LockServer Stoped")
        self.transport.shutdown()

if __name__=="__main__":
    objlogSeverThread = LockServer()
    objlogSeverThread.start()

