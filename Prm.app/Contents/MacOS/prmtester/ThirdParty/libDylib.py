import ctypes
g_strLibNanohippoPath ='./Lib/libAll.dylib'

##libPy = ctypes.cdll.LoadLibrary('/Users/mental/Library/Developer/Xcode/DerivedData/pytest-fziufxvgpheflifmsljofyokeczf/Build/Products/Release/libpytest.dylib')
libPy = ctypes.cdll.LoadLibrary(g_strLibNanohippoPath)
## void *createNanoHippoDev()
libPy.createNanoHippoDev.restype = ctypes.c_void_p
## void destroyNanoHippoDev(void *obj)
libPy.destroyNanoHippoDev.argtypes =  [ctypes.c_void_p] 
## int openSerial(const char *serialDev)t 
libPy.openSerial.argtypes =  [ctypes.c_void_p,ctypes.c_char_p] 
libPy.openSerial.restype = ctypes.c_int
## int closeAll()
libPy.closeAll.argtypes =  [ctypes.c_void_p] 
libPy.closeAll.restype = ctypes.c_int
## int SetWriteTimeInterval(int usleeps)
libPy.SetWriteTimeInterval.argtypes =  [ctypes.c_void_p,ctypes.c_int] 
libPy.SetWriteTimeInterval.restype = ctypes.c_int
## int WriteString(int port , const char* str )
libPy.WriteString.argtypes =  [ctypes.c_void_p,ctypes.c_int, ctypes.c_char_p] 
libPy.WriteString.restype = ctypes.c_int
## int WriteString(int port , const char* str )
libPy.ReadString.argtypes =  [ctypes.c_void_p,ctypes.c_int]
libPy.ReadString.restype = ctypes.c_char_p
## int WriteBytes(int port ,  const char* data , int len)
libPy.WriteBytes.argtypes =  [ctypes.c_void_p,ctypes.c_int, ctypes.c_char_p ,ctypes.c_int] 
libPy.WriteBytes.restype = ctypes.c_int
## int WriteStringBytes(int port , const char* str )
libPy.WriteStringBytes.argtypes =  [ctypes.c_void_p,ctypes.c_int, ctypes.c_char_p] 
libPy.WriteStringBytes.restype = ctypes.c_int
## void *readBuffer(int port)
libPy.readBuffer.argtypes =  [ctypes.c_void_p,ctypes.c_int] 
libPy.readBuffer.restype = ctypes.c_void_p
## const char* getStringFromBuffer(void *buffer)
libPy.getStringFromBuffer.argtypes =  [ctypes.c_void_p] 
libPy.getStringFromBuffer.restype = ctypes.c_char_p
## int getBufferLength( void *buffer)
libPy.getBufferLength.argtypes =  [ctypes.c_void_p] 
libPy.getBufferLength.restype = ctypes.c_int
## int getBytesFromBuffer(void *buffer , char* bytes , int length)
libPy.getBytesFromBuffer.argtypes =  [ctypes.c_void_p , ctypes.POINTER(ctypes.c_char) , ctypes.c_int] 
libPy.getBytesFromBuffer.restype = ctypes.c_int
## void destroyBuffer(void *buffer)
libPy.destroyBuffer.argtypes =  [ctypes.c_void_p] 
## const char * ReadChannels()
libPy.ReadChannels.argtypes =  [ctypes.c_void_p] 
libPy.ReadChannels.restype = ctypes.c_char_p
## const char * GetDetectString()
libPy.GetDetectString.argtypes =  [ctypes.c_void_p]
libPy.GetDetectString.restype = ctypes.c_char_p
## void ClearBuffer(int port)
libPy.ClearBuffer.argtypes =  [ctypes.c_void_p,ctypes.c_int]
#int SetLogFile(void *obj,int nPort, char* cstrPath)
libPy.SetLogFile.argtypes =  [ctypes.c_void_p,ctypes.c_int,ctypes.c_char_p]
libPy.SetLogFile.restype = ctypes.c_int
## int IsDataReady(int port)
libPy.IsDataReady.argtypes =  [ctypes.c_void_p,ctypes.c_int] 
libPy.IsDataReady.restype = ctypes.c_int
## int SetDetectString(const char* det)
libPy.SetDetectString.argtypes =  [ctypes.c_void_p,ctypes.c_char_p] 
libPy.SetDetectString.restype = ctypes.c_int
## int WaitDetect(int port, int timeout)
libPy.WaitDetect.argtypes =  [ctypes.c_void_p,ctypes.c_int,ctypes.c_int] 
libPy.WaitDetect.restype = ctypes.c_int

## int WaitDetectStr(self.plibNanohippoObj, nPort, strDetect,nTimeout)
libPy.WaitDetectStr.argtypes =  [ctypes.c_void_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_int]
libPy.WaitDetectStr.restype = ctypes.c_int


libPy.SetFilterColorCode.argtypes = [ctypes.c_void_p,ctypes.c_int]
libPy.SetFilterColorCode.restype = ctypes.c_int

libPy.SetFilterUnreadable.argtypes = [ctypes.c_void_p,ctypes.c_int]
libPy.SetFilterUnreadable.restype = ctypes.c_int

libPy.CreatePub.argtypes = [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_int]
libPy.CreatePub.restype = ctypes.c_int

libPy.CreateRep.argtypes = [ctypes.c_void_p,ctypes.c_char_p]
libPy.CreateRep.restype = ctypes.c_int

libPy.WritePassControlBit.argtypes = [ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_char_p]
libPy.WritePassControlBit.restype = ctypes.c_int


##Sdev Dll


libPy.createSDev.restype = ctypes.c_void_p

libPy.destroySDev.argtypes =  [ctypes.c_void_p]


libPy.CreateIPC.argtypes = [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]
libPy.CreateIPC.restype = ctypes.c_int

libPy.PublishLog.argtypes = [ctypes.c_void_p ,ctypes.c_char_p]
libPy.PublishLog.restype = ctypes.c_int

libPy.Open.argtypes = [ctypes.c_void_p ,ctypes.c_char_p,ctypes.c_int]
libPy.Open.restype = ctypes.c_int

libPy.Close.argtypes = [ctypes.c_void_p]
libPy.Close.restype = ctypes.c_int

libPy.SDevWriteString.argtypes = [ctypes.c_void_p ,ctypes.c_char_p,ctypes.c_int]
libPy.SDevWriteString.restype = ctypes.c_int

libPy.SDevReadString.argtypes = [ctypes.c_void_p]
libPy.SDevReadString.restype = ctypes.c_char_p

libPy.SDevReadString2.argtypes = [ctypes.c_void_p]
libPy.SDevReadString2.restype = ctypes.c_char_p

libPy.SDevSetDetectString.argtypes = [ctypes.c_void_p,ctypes.c_char_p]
libPy.SDevSetDetectString.restype = ctypes.c_int

libPy.SDevWaitDetect.argtypes = [ctypes.c_void_p,ctypes.c_int]
libPy.SDevWaitDetect.restype = ctypes.c_int

libPy.SetHexmode.argtypes = [ctypes.c_void_p,ctypes.c_int]
libPy.SetHexmode.restype = ctypes.c_int



libPy.SDevSetFilterColorCode.argtypes = [ctypes.c_void_p,ctypes.c_int]
libPy.SDevSetFilterColorCode.restype = ctypes.c_int



class LibSocketDev:
	"""docstring for SocketDev"""
	def __init__(self):
		
		self.Sdev = libPy.createSDev()
	def delObj(self):
		if self.Sdev:
			ret = self.Sdev.destroyCPWRSEQ(self.Sdev)
		else:
			print "pyLib.delObj Error"
			ret =-1
		return ret

		
	def CreateIPC(self,strreply,strpubliser):
		if self.Sdev:
			ret = libPy.CreateIPC(self.Sdev,strreply,strpubliser)
		else:
			print "pyLibNanohippo.ReadChannels Error"
			ret =-1
		return ret

	def PublishLog(self,strLog):
		if self.Sdev:
			ret = libPy.PublishLog(self.Sdev,strLog)
		else:
			print "pyLibNanohippo.PublishLog Error"
			ret =-1
		return ret

	def Open(self,strName,nPort):
		if self.Sdev:
			ret = libPy.Open(self.Sdev,strName,nPort)
		else:
			print "pyLibNanohippo.Open Error"
			ret =-1
		return ret

	def Close(self):
		if self.Sdev:
			ret = libPy.Close(self.Sdev)
		else:
			print "pyLibNanohippo.IsDataReady Error"
			ret =-1
		return ret
	def WriteString(self,strData,nMutilFlag):
		if self.Sdev:
			ret = libPy.SDevWriteString(self.Sdev,strData,nMutilFlag)
		else:
			print "pyLibNanohippo.SDevWriteString Error"
			ret =-1
		return ret
	def ReadString(self):
		if self.Sdev:
			ret = libPy.SDevReadString(self.Sdev)
		else:
			print "pyLibNanohippo.WaitDetect Error"
			ret =-1
		return ret
	def ReadString2(self):
		if self.Sdev:
			ret = libPy.SDevReadString2(self.Sdev)
		else:
			print "pyLibNanohippo.WaitDetect Error"
			ret =-1
		return ret
	def SetDetectString(self,strData):
		if self.Sdev:
			ret = libPy.SDevSetDetectString(self.Sdev,strData)
		else:
			print "pyLibNanohippo.WaitDetect Error"
			ret =-1
		return ret
	def WaitDetect(self,nData):
		if self.Sdev:
			ret = libPy.SDevWaitDetect(self.Sdev,nData)
		else:
			print "pyLibNanohippo.WaitDetect Error"
			ret =-1
		return ret
	def SetHexmode(self,nmode):
		if self.Sdev:
			libPy.SetHexmode(self.Sdev,nmode)
		else:
			print "pyLibNanohippo.WaitDetect Error"

	def SetFilterColorCode(self,nmode):
		if self.Sdev:
			libPy.SDevSetFilterColorCode(self.Sdev,nmode)
		else:
			print "pyLibNanohippo.WaitDetect Error"

class LibNanohippo:
	def __init__(self):
		self.plibNanohippoObj = libPy.createNanoHippoDev()
		print "Add NanoHippo Obj {}".format(self.plibNanohippoObj)
	def delObj(self):
		if self.plibNanohippoObj:
			ret = self.plibNanohippoObj.destroyNanoHippoDev()
		else:
			print "pyLibNanohippo.delObj Error"
			ret =-1
		return ret
	def openSerial(self,strSerialDev):
		if self.plibNanohippoObj:
			ret = libPy.openSerial(self.plibNanohippoObj,strSerialDev)
		else:
			print "pyLibNanohippo.openSerial Error"
			ret =-1
		return ret
	def closeAll(self):
		if self.plibNanohippoObj:
			ret = libPy.closeAll(self.plibNanohippoObj)
		else:
			print "pyLibNanohippo.closeAll Error"
			ret =-1
		return ret

	def SetWriteTimeInterval(self,nSleeps):
		if self.plibNanohippoObj:
			ret = libPy.SetWriteTimeInterval(self.plibNanohippoObj,nSleeps)
		else:
			print "pyLibNanohippo.SetWriteTimeInterval Error"
			ret =-1
		return ret

	def SetLogFile(self,nPort,strPath):
		if self.plibNanohippoObj:
			ret = libPy.SetLogFile(self.plibNanohippoObj,nPort,strPath)
		else:
			print "pyLibNanohippo.SetLogFile Error"
			ret =-1
		return ret

	def WaitDetectStr(self,nPort, strDetect, nTimeout):
		if self.plibNanohippoObj:
			ret = libPy.WaitDetectStr(self.plibNanohippoObj, nPort, strDetect,nTimeout)
		else:
			print "pyLibNanohippo.WriteString Error"
			ret = -1
		return ret

	#def ReadString(self,nPort):
	def ReadString(self, nPort):
		if self.plibNanohippoObj:
			ret = libPy.ReadString(self.plibNanohippoObj, nPort)

		else:
			print "pyLibNanohippo.ReadString Error"
			ret = -1
		if ret == None:
			ret =""
		return ret

	def WriteString(self,nPort,strData):
		if self.plibNanohippoObj:
			ret = libPy.WriteString(self.plibNanohippoObj,nPort,strData)
		else:
			print "pyLibNanohippo.WriteString Error"
			ret =-1
		return ret
	def WriteBytes(self,nPort,strData,nLen):
		if self.plibNanohippoObj:
			ret = libPy.WriteBytes(self.plibNanohippoObj,nPort,strData,nLen)
		else:
			print "pyLibNanohippo.WriteString Error"
			ret =-1
		return ret
	def WriteStringBytes(self,nPort,strData):
		if self.plibNanohippoObj:
			ret = libPy.WriteStringBytes(self.plibNanohippoObj,nPort,strData)
		else:
			print "pyLibNanohippo.WriteStringBytes Error"
			ret =-1
		return ret
	def readBuffer(self,nPort):
		if self.plibNanohippoObj:
			ret = libPy.readBuffer(self.plibNanohippoObj,nPort)
		else:
			print "pyLibNanohippo.readBuffer Error"
			ret =-1
		return ret
	def getStringFromBuffer(self,stdData):
		if self.plibNanohippoObj:
			ret = libPy.getStringFromBuffer(self.plibNanohippoObj,stdData)
		else:
			print "pyLibNanohippo.getStringFromBuffer Error"
			ret =-1
		return ret
	def getBufferLength(self,stdData):
		if self.plibNanohippoObj:
			ret = libPy.getBufferLength(self.plibNanohippoObj,stdData)
		else:
			print "pyLibNanohippo.getBufferLength Error"
			ret =-1
		return ret

	def getBytesFromBuffer(self,stdData,nLen):
		if self.plibNanohippoObj:
			ret = libPy.getBytesFromBuffer(self.plibNanohippoObj,stdData,nLen)
		else:
			print "pyLibNanohippo.getBytesFromBuffer Error"
			ret =-1
		return ret
	def destroyBuffer(self,stdData):
		if self.plibNanohippoObj:
			ret = libPy.destroyBuffer(self.plibNanohippoObj,stdData)
		else:
			print "pyLibNanohippo.destroyBuffer Error"
			ret =-1
		return ret
	def ReadChannels(self):
		if self.plibNanohippoObj:
			ret = libPy.ReadChannels(self.plibNanohippoObj)
		else:
			print "pyLibNanohippo.ReadChannels Error"
			ret =-1
		return ret

	def GetDetectString(self):
		if self.plibNanohippoObj:
			ret = libPy.GetDetectString(self.plibNanohippoObj)
		else:
			print "pyLibNanohippo.GetDetectString Error"
			ret =-1
		return ret

	def ClearBuffer(self,nPort):
		ret = 0
		if self.plibNanohippoObj:
			libPy.ClearBuffer(self.plibNanohippoObj,nPort)
		else:
			print "pyLibNanohippo.ClearBuffer Error"
			ret =-1
		return ret

	def IsDataReady(self,nPort):
		if self.plibNanohippoObj:
			ret = libPy.IsDataReady(self.plibNanohippoObj,nPort)
		else:
			print "pyLibNanohippo.IsDataReady Error"
			ret =-1
		return ret
	def SetDetectString(self,strData):
		if self.plibNanohippoObj:
			ret = libPy.SetDetectString(self.plibNanohippoObj,strData)
		else:
			print "pyLibNanohippo.SetDetectString Error"
			ret =-1
		return ret
	def WaitDetect(self,nPort,nTimeOut):
		if self.plibNanohippoObj:
			ret = libPy.WaitDetect(self.plibNanohippoObj,nPort,nTimeOut)
		else:
			print "pyLibNanohippo.WaitDetect Error"
			ret =-1
		return ret
	def SetFilterColorCode(self,nFlag):
		if self.plibNanohippoObj:
			ret = libPy.SetFilterColorCode(self.plibNanohippoObj,nFlag)
		else:
			print "pyLibNanohippo.WaitDetect Error"
			ret =-1
		return ret
	def SetFilterUnreadable(self,nFlag):
		if self.plibNanohippoObj:
			ret = libPy.SetFilterUnreadable(self.plibNanohippoObj,nFlag)
		else:
			print "pyLibNanohippo.WaitDetect Error"
			ret =-1
		return ret
	def CreatePub(self,strPublic,nPort):
		if self.plibNanohippoObj:
			ret = libPy.CreatePub(self.plibNanohippoObj,strPublic,nPort)
		else:
			print "pyLibNanohippo.WaitDetect Error"
			ret =-1
		return ret
	def CreateRep(self,strPublic):
		if self.plibNanohippoObj:
			ret = libPy.CreateRep(self.plibNanohippoObj,strPublic)
		else:
			print "pyLibNanohippo.WaitDetect Error"
			ret =-1
		return ret
	def WritePassControlBit(self,nPort, nStationid,strSzCmd):
		if self.plibNanohippoObj:
			ret = libPy.WritePassControlBit(self.plibNanohippoObj,nPort, nStationid,strSzCmd)
		else:
			print "pyLibNanohippo.WritePassControlBit Error"
			ret =-1
		return ret



g_strLibGh = './Lib/libGhInfo.dylib'
libGh = ctypes.cdll.LoadLibrary(g_strLibGh)

## int openSerial(const char *serialDev)t
libGh.GetInfo.argtypes =  [ctypes.c_char_p]
libGh.GetInfo.restype = ctypes.c_char_p

class LibGh:
	def GetInfo(self,strKey):
		return libGh.GetInfo(strKey)


g_strLibArmDl = './Lib/libArmDL.dylib'
libDl = ctypes.cdll.LoadLibrary(g_strLibArmDl)


libDl.createArmDl.restype = ctypes.c_void_p

libDl.destroyArmdl.argtypes =  [ctypes.c_void_p] 

libDl.CreateTCPClient.argtypes =  [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_int16]
libDl.CreateTCPClient.restype = ctypes.c_int

libDl.CreatZmqPub.argtypes =  [ctypes.c_void_p,ctypes.c_char_p] 
libDl.CreatZmqPub.restype = ctypes.c_int

libDl.setLogPath.argtypes =  [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p]


libDl.startDataLogger.argtypes =  [ctypes.c_void_p]
libDl.startDataLogger.restype = ctypes.c_int

libDl.stopDataLogger.argtypes =  [ctypes.c_void_p]
libDl.stopDataLogger.restype = ctypes.c_int

libDl.updateConfig.argtypes =  [ctypes.c_void_p,ctypes.c_int,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_int,ctypes.c_int]


class LibArmDl:
	def __init__(self):
		self.plibDLObj = libDl.createArmDl()
		print "Add ArmDl Obj {}".format(self.plibDLObj)
	def delObj(self):
		if self.plibDLObj:
			ret = libDl.destroyArmdl(self.plibDLObj)
		else:
			print "ArmDl.delObj Error"
			ret =-1
		return ret
	def CreateTCPClient(self,strName,strIp,nPort):
		if self.plibDLObj:
			ret = libDl.CreateTCPClient(self.plibDLObj,strName,strIp,nPort)
		else:
			print "ArmDl.CreateTCPClient Error"
			ret =-1
		return ret
	def CreatZmqPub(self,strUrl):
		if self.plibDLObj:
			ret = libDl.CreatZmqPub(self.plibDLObj,strUrl)
		else:
			print "ArmDl.CreatZmqPub Error"
			ret =-1
		return ret

	def setLogPath(self,strHeader,strFileName):
		if self.plibDLObj:
			libDl.setLogPath(self.plibDLObj,strHeader,strFileName)
		else:
			print "ArmDl.setLogPath Error"

	def startDataLogger(self):
		if self.plibDLObj:
			ret = libDl.startDataLogger(self.plibDLObj)
		else:
			print "ArmDl.startDataLogger Error"
			ret =-1
		return ret
	def stopDataLogger(self):
		if self.plibDLObj:
			ret = libDl.stopDataLogger(self.plibDLObj)
		else:
			print "ArmDl.stopDataLogger Error"
			ret =-1
		return ret
	def updateConfig(self,nChannel,fResdiv, fGain, fRefVolt, fRes, nflag=0, nUnitConvert=1):
		if self.plibDLObj:
			libDl.updateConfig(self.plibDLObj,nChannel,fResdiv, fGain, fRefVolt, fRes, nflag, nUnitConvert)
		else:
			print "ArmDl.setLogPath Error"
		
## int openSerial(const char *serialDev)t
##PS



g_strLibPSDl = './Lib/libPwrSequence.dylib'
libPs = ctypes.cdll.LoadLibrary(g_strLibPSDl)



libPs.createCPWRSEQ.restype = ctypes.c_void_p
libPs.destroyCPWRSEQ.argtypes =  [ctypes.c_void_p]

libPs.CreateTCPClient.argtypes =  [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_int16]
libPs.CreateTCPClient.restype = ctypes.c_int

libPs.CreatZmqPub.argtypes =  [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_int]
libPs.CreatZmqPub.restype = ctypes.c_int

libPs.startDataLogger.argtypes =  [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_int]
libPs.startDataLogger.restype = ctypes.c_int

libPs.stopDataLogger.argtypes =  [ctypes.c_void_p,ctypes.c_int]
libPs.stopDataLogger.restype = ctypes.c_int

libPs.updateConfig.argtypes =  [ctypes.c_void_p,ctypes.c_char_p,ctypes.c_int,ctypes.c_int]



class LibPs:
	def __init__(self):
		self.plibDLObj = libPs.createCPWRSEQ()
		print "Add ArmDl Obj {}".format(self.plibDLObj)
	def delObj(self):
		if self.plibDLObj:
			ret = libPs.destroyCPWRSEQ(self.plibDLObj)
		else:
			print "ArmDl.delObj Error"
			ret =-1
		return ret
	def CreateTCPClient(self,strName,strIp,nPort):
		if self.plibDLObj:
			ret = libPs.CreateTCPClient(self.plibDLObj,strName,strIp,nPort)
		else:
			print "ArmDl.CreateTCPClient Error"
			ret =-1
		return ret
	def CreatZmqPub(self,strUrl,nWriteLog=0):
		if self.plibDLObj:
			ret = libPs.CreatZmqPub(self.plibDLObj,strUrl,nWriteLog)
		else:
			print "ArmDl.CreatZmqPub Error"
			ret =-1
		return ret
	def startDataLogger(self,strLogPath,nFlag):
		if self.plibDLObj:
			ret = libPs.startDataLogger(self.plibDLObj,strLogPath,nFlag)
		else:
			print "ArmDl.startDataLogger Error"
			ret =-1
		return ret
	def stopDataLogger(self,nFlag):
		if self.plibDLObj:
			ret = libPs.stopDataLogger(self.plibDLObj,nFlag)
		else:
			print "ArmDl.stopDataLogger Error"
			ret =-1
		return ret
	def updateConfig(self,strConfig,nFlag,nConfigId):
		if self.plibDLObj:
			libPs.updateConfig(self.plibDLObj,strConfig,nFlag,nConfigId)
		else:
			print "ArmDl.setLogPath Error"



