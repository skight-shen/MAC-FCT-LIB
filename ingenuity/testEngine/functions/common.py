import os,time,datetime
from ingenuity.tinyrpc.dispatch import public
import struct

class Common(object):
    def __init__(self):
        self.startTime = ""

    @public
    def delay(self,*args,**kwargs):
        strParam1 = float(args[0])/1000
        time.sleep(strParam1)
        return "--PASS--"

    @public
    def skip(self, *args, **kwargs):
        return "--SKIP--"

    @public
    def hextoint(self, *args):
        iValue = int(args[0], 16)
        return iValue

    @public
    def hextofloat(self, *args, **kwargs):
        if'0x' in args[0]:
            hexValue = args[0][2:]
        else:
            hexValue = args[0]

        fValue = struct.unpack('!f', hexValue.decode('hex'))[0]
        return fValue

    @public
    def floattohex(self,*args, **kwargs):
        hexValue = struct.pack("<f", float(args[0])).encode('hex')
        hexValue = '0x{}'.format(hexValue)
        return hexValue

    @public
    def timerreset(self, *args, **kwargs):
        self.startTime = time.time()
        return True

    @public
    def timerstop(self, *args, **kwargs):
        fTimeDiff = "%0.03f"%(time.time() - self.startTime)
        return fTimeDiff