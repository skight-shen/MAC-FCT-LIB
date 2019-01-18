from Common.tinyrpc.dispatch import public
import time
import struct
import re
from Common.BBase import *

class General(object):
    def __init__(self):
        super(General, self).__init__()
        self.m_objRe = cBruceRe()
        self.m_objBtimer = cBruceTime()
    @public('vendorid')
    def vendorid(self, *args, **kwargs):
        return "prmeasure"

    @public('delay')
    def delay(self, *args, **kwargs):
        if len(args) > 0:
            self.m_objBtimer.Delay(float(args[0]))
        return '--PASS--'

    @public("skip")
    def skip(self, *args, **kwargs):
        return "--SKIP--"


    @public("hextoint")
    def hextoint(self, *args, **kwargs):
        bRet =True
        strRet = ""
        try:

            bRet,strHex  = self.m_objRe.SubStr_b_str(args[0]," ","")
            if bRet:
                strRet = int(strHex,16)

            print "hextto Int {} -->> {}".format(args,strRet)

        except Exception as e:
            bRet =False
            
        return strRet if bRet else "--FAIL--"
    @public("hextofloat")
    def hextofloat(self, *args, **kwargs):
        bRet =True
        strRet = ""

        try:
            listRet = re.split(" ",args[0])
            listRet.reverse()
            strHex=""
            for i in listRet:
                strHex+=str(i)

            floatHex=strHex.decode('hex')
            if len(floatHex)==4:
                strRet = str(struct.unpack('!f',floatHex )[0])
            else:
                strRet="Len is Not 4"

            print "hextofloat  {} -->> {}".format(args[0], strRet)
        except Exception as e:
            bRet =False
            strRet="Exception {}".format(e)
            
        return strRet if bRet else "--FAIL--"
    @public("floattohex")
    def floattohex(self, *args, **kwargs):
        bRet =True
        strRet = ""
        try:
            strRet = "0x{}".format(struct.pack("<f", float(args[0].encode('hex'))))
            print "floattohex  {} -->> {}".format(args, strRet)
        except Exception as e:
            bRet =False
            
        return strRet if bRet else "--FAIL--"
