import zmq
from Common.tinyrpc.transports.zmq import ZmqClientTransport
from Common import zmqports
from LockBase import *
from Common.BBase import *

class LockClientNet:
    objProctocal = cProtocal("")
    objThreadLock = cBaseThreadLock()
    def __init__(self):
        ctx = zmq.Context()
        self.sub = ctx.socket(zmq.SUB)
        self.sub.connect("tcp://127.0.0.1:" + str(zmqports.PRM_LOCK_PORT))
        self.sub.setsockopt(zmq.SUBSCRIBE, "")
        self.req = ZmqClientTransport.create(ctx, "tcp://127.0.0.1:" + str(zmqports.PRM_LOCK_PORT))
    def Lock(self,strGrounp,strItem):
        #return self.req.send_reply(self.objProctocal.CreateMessage("lock",strGrounp,strItem))
        return self.SendReply(self.objProctocal.CreateMessage("lock",strGrounp,strItem))
    def UnLock(self,strGrounp,strItem):
        #return self.req.send_reply(self.objProctocal.CreateMessage("unlock",strGrounp,strItem))
        return self.SendReply(self.objProctocal.CreateMessage("unlock",strGrounp,strItem))
    def SendReply(self,strMessage):
        strRet=""
        try:
            strRet =self.req.send_reply(strMessage)
        except Exception as e:
            pass
        return strRet





class LockClient:
    objLogClient = LockClientNet()
    def __init__(self, strGrounp, strItem):
        self.strGrounp = strGrounp
        self.strItem = strItem
    def Lock(self,bFlag):
        bContinue = True 
        if bFlag:
            while True:
                if self.objLogClient.Lock(self.strGrounp,self.strItem)=="0":
                    break
        else:
            if self.objLogClient.UnLock(self.strGrounp,self.strItem)=="0":
                bContinue  =  False

        return


if __name__ == '__main__':
    objlock = LockClient("potassium","1")

    objlock = LockClient("potassium","2")

    objlock = LockClient("potassium","3")

    objlock = LockClient("potassium","4")









