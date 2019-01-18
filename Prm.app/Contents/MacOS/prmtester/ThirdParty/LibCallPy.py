
from Common.BBase import *
from Common import zmqports
from Log.LogClient import LogClient

from libDylib import *
import time
from AynsLock.LockClient import LockClient

class cPotassiumIdFinder(cShell):
	"""docstring for cPotassiumIdFinder"""
	dictPotassiumValue = {1:0x32,2:0x33,3:0x34,4:0x35}
	strKtoolPath = "/usr/local/bin/ktool"
	strAddrEEProm = "0x2004"
	objBRe = cBruceRe()
	def __init__(self):
		self.listPotassiumUrl=[]
		self.liststrUsbId = []
		self.dictPotassiumUrl={}
		self.strPotassiumUrl=""
		self.__Reflash()
		print "Auto Potassium Dict {}".format(self.dictPotassiumUrl)

	def PotassiumSize(self):
		return len(self.dictPotassiumUrl)
	def PotassiumInfo(self):
		return self.dictPotassiumUrl
	def ManualSetPotassiumId(self,strUsbUrl,nIndex):
		if self.KtoolWriteEEpromMannual(strUsbUrl,nIndex):
			print "{} {} set to {} success ".format(strUsbUrl,nIndex,self.dictPotassiumValue[nIndex])
		else:
			print "{} {} set to {} error ".format(strUsbUrl, nIndex, self.dictPotassiumValue[nIndex])


	def AutoPotassiumId(self,liststrUsbId):
		del self.dictPotassiumUrl
		self.dictPotassiumUrl={}
		bRet = True
		if len(liststrUsbId)>0:
			strCheckIndex = -1
			listCheckNumber =[]
			for strId in liststrUsbId:
				bRet, listInfo = self.objBRe.MatchStr_b_list(strId, "/dev/cu.usbmodem(\d+)")
				if bRet and len(listInfo) == 1:
					self.listPotassiumUrl.append(strId)
					listCheckNumber.append(listInfo[0])
			print listCheckNumber
			if len(listCheckNumber)>=2:
				strCheckIndex=0
				for i in range(0,len(listCheckNumber[0])):
					if listCheckNumber[0][i] == listCheckNumber[1][i]:
						strCheckIndex +=1
					else:
						break
				if strCheckIndex < len(listCheckNumber[0])-1:
					for strNumber in listCheckNumber:
						self.dictPotassiumUrl[int(strNumber[strCheckIndex])] = "/dev/cu.usbmodem{}".format(strNumber)
			else:
				bRet = False
		else:
			bRet = False
		return bRet

	def SetPotassiumId(self,nIndex,bReflush=True):
		if bReflush:
			self.__Reflash()
		bRet = True
		if nIndex in self.dictPotassiumUrl.keys():
			bRet =self.KtoolWriteEEprom(nIndex)
		else:
			bRet = False
		return bRet


	def GetPotassiumId(self,nIndex,bReflush=False):
		if bReflush:
			self.__Reflash()
		bRet = False
		strUrl = ""

		for PotassiumUrl in self.listPotassiumUrl:
			if self.KtoolReadEEpromMannual(PotassiumUrl) == self.dictPotassiumValue[nIndex]:
				bRet = True
				strUrl = PotassiumUrl
				break
		return strUrl


		# if nIndex in self.dictPotassiumUrl.keys():
		# 	if self.KtoolReadEEprom(nIndex) != self.dictPotassiumValue[nIndex]:
		# 		bRet=False
		# else:
		# 	bRet = False
		return self.dictPotassiumUrl[nIndex] if bRet else ""

	def KtoolWriteEEprom(self,nIndex):
		bRet, strInfo = self.RunShell_b_str(self.strKtoolPath,self.dictPotassiumUrl[nIndex],"write_eeprom",self.strAddrEEProm,hex(self.dictPotassiumValue[nIndex]))
		if bRet:
			bRet,listInfo = self.objBRe.MatchStr_b_list(strInfo,"Length.*[\s]+INFO:\s+?(\S+)")
			if bRet and len(listInfo)==1:
				strInfo = listInfo[0]
		if strInfo !=hex(self.dictPotassiumValue[nIndex])[-2:]:
			bRet = False
		return
	def KtoolWriteEEpromMannual(self,strUsbUrl,nIndex):
		bRet, strInfo = self.RunShell_b_str(self.strKtoolPath,strUsbUrl,"write_eeprom",self.strAddrEEProm,hex(self.dictPotassiumValue[nIndex]))
		return bRet

	def KtoolReadEEpromMannual(self,strUsbUrl):
		bRet, strInfo = self.RunShell_b_str(self.strKtoolPath,strUsbUrl,"read_eeprom",self.strAddrEEProm,1)
		print strInfo
		if bRet:
			bRet,listInfo = self.objBRe.MatchStr_b_list(strInfo,"Length.*[\s]+INFO:\s+?(\S+)")
			if bRet and len(listInfo)==1:
				strInfo = listInfo[0]
		nRet = -1
		if bRet:
			try:
				nRet=int(strInfo,16)
			except:
				nRet=-1
				bRet=False
		return nRet if bRet else -1
	def KtoolReadEEprom(self,nIndex):
		bRet, strInfo = self.RunShell_b_str(self.strKtoolPath,self.dictPotassiumUrl[nIndex],"read_eeprom",self.strAddrEEProm,1)
		print strInfo
		if bRet:
			bRet,listInfo = self.objBRe.MatchStr_b_list(strInfo,"Length.*[\s]+INFO:\s+?(\S+)")
			if bRet and len(listInfo)==1:
				strInfo = listInfo[0]
		nRet = 255
		if bRet:
			try:
				nRet=int(strInfo,16)
			except:
				nRet=255
				bRet=False
		return nRet if bRet else 255

	def __GetAllPotassiumId_b_liststr(self):
		bRet,strInfos =  self.RunShell_b_str("ls","/dev/cu.*")
		liststrRet =[]
		if bRet:
			liststrRet = self.__PraseStdoutInfos_liststr(strInfos)
			if len(liststrRet) <=0:
				bRet=False
		return bRet,liststrRet
	def __Reflash(self):
		bRet,liststrRet = self.__GetAllPotassiumId_b_liststr()
		if bRet:
			self.liststrUsbId=[]
			self.liststrUsbId = liststrRet
			self.AutoPotassiumId(self.liststrUsbId)

	def __PraseStdoutInfos_liststr(self,strStdoutInfos):
		liststrRet = []
		try:
			liststrInfos = re.split("\n",strStdoutInfos)
			for strInfo in liststrInfos:
				if len(re.findall("",strInfo))>0:
					liststrRet.append(strInfo)
		except Exception as e:
			pass
		return liststrRet



class cKtool(cShell):
	"""docstring for cKtool"""
	def __init__(self, strKtoolPath = "/usr/local/bin/ktool"):

		self.strKtoolPath = strKtoolPath

	def KtoolRun_b(self,strPotassiumId,strCmd,strCheckResultRex):
		bRet,strResultInfos =  self.RunShell_b_str(self.strKtoolPath,strPotassiumId,strCmd)
		if bRet and len(re.findall(strCheckResultRex,strResultInfos))>0:
			bRet=True
		else:
			bRet=False
		return bRet
		



from libDylib import  LibNanohippo,LibSocketDev



class cSocketDev(object):
	"""docstring for ClassName"""
	m_objBTime = cBruceTime()
	def __init__(self, nSlotId):
		super(cSocketDev, self).__init__()
		self.nSlotId = nSlotId

		self.bConnectFlag= False

		#Add strPubUrl/strRepUrl Auto Get


		self.objSocketDev = LibSocketDev()


		strRepUrl = "tcp://127.0.0.1:" + str(int(zmqports.UART2_PORT) + self.nSlotId )
		strPubUrl = "tcp://127.0.0.1:" + str(int(zmqports.UART2_PUB) + self.nSlotId )

		self.objSocketDev.CreateIPC(strRepUrl,strPubUrl)
		self.strZynqAddr = "169.254.1.{}".format(32+self.nSlotId)
		self.strPchport = 7603

		
		self.m_objBLog = LogClient(self.nSlotId,"pch_log_prm_efi.log")#cBruceLogs("/vault/pch_log_prm_efi.log")
		self.nConnectRet = -9
		self.Connect_b()



	def Connect_b(self):
		self.nConnectRet = self.objSocketDev.Open(self.strZynqAddr,self.strPchport)
		if self.nConnectRet<0:
			self.bConnectFlag = False
			print "Connect False Close"

		else:
			print "Connect True Close"
			self.bConnectFlag=True
		return self.bConnectFlag

	def Clr_spam_buff(self):
		pass

	def DutSendCmd_n_str(self,strCmd,nTimeout):
		nRet = -1
		strRet=""
		self.m_objBTime.Delay(500)
		if self.bConnectFlag:
			for i in strCmd:
				nRet = self.objSocketDev.WriteString(i,1)
				if nRet<0:
					self.m_objBTime.Delay(50)
					nRet = self.objSocketDev.WriteString(i, 1)
					strRet += "Byte {} Retry ".format(i)
				self.m_objBTime.Delay(50)

			nRet = self.objSocketDev.WriteString("\r\n",1)
			if nRet>=0:
				self.m_objBTime.Delay(20)
				nRet = self.objSocketDev.WaitDetect(nTimeout)
		else:
			print "Socket Dut Didn't Connected !! "
		return nRet,strRet

	def DutSendString_n(self,strData):
		nRet = -1
		strRet = ""
		self.m_objBTime.Delay(500)
		if self.bConnectFlag:
			for i in strData:
				nRet = self.objSocketDev.WriteString(i,1)
				if nRet<0:
					self.m_objBTime.Delay(50)
					nRet = self.objSocketDev.WriteString(i, 1)
					strRet += "Byte {} Retry ".format(i)
				self.m_objBTime.Delay(50)
			nRet = self.objSocketDev.WriteString("\r\n", 1)
			self.m_objBTime.Delay(20)
		else:
			print "Socket Dut Didn't Connected !! "
		return 0

	def DutReadString_str(self):
		strRet = ""
		if self.bConnectFlag:
			strRet =self.objSocketDev.ReadString()
			if strRet!="":
				self.m_objBLog.Trace(strRet)
		else:
			print "Socket Dut Didn't Connected !!DutReadString_str "
		return strRet
	def DutReadString2_str(self):
		strRet = ""
		if self.bConnectFlag:
			self.m_objBTime.Delay(50)
			strRet =self.objSocketDev.ReadString()
			if strRet!="":
				print "Efi Read:-->> {}".format(strRet)
				self.m_objBLog.Trace(strRet)
		else:
			print "Socket Dut Didn't Connected !!DutReadString_str "
		return strRet

	def DutSetDetectString(self,strData):
		self.objSocketDev.SetDetectString(strData)


	def DutWaitForString_n(self,nTimeout):
		nRet=-1
		nRet = self.objSocketDev.WaitDetect(nTimeout)
		return nRet

	
	def Close(self):
		if self.bConnectFlag:
			self.objSocketDev.Close()
		else:
			print  "Socket Dut Didn't Connected !!Close "



class cNanoHippoPy:
	"""docstring for ClassName"""
	m_objBTime = cBruceTime()
	m_objBRe =cBruceRe()
	nPubPort = 31337
	objKtool = cKtool()

	def __init__(self, nSlotId,objLock,strPotassiumUrl):

		self.nSlotId = nSlotId

		self.g_Lock = objLock

		self.PotassiumUrl = strPotassiumUrl

		self.bConnectFlag= False

		strRepUrl = "tcp://127.0.0.1:" + str(int(zmqports.UART_PORT) + self.nSlotId )
		strPubUrl = "tcp://127.0.0.1:" + str(int(zmqports.UART_PUB) + self.nSlotId )
		#Add strPubUrl/strRepUrl Auto Get

		self.objNanoHippoDev = LibNanohippo()

		self.objNanoHippoDev.CreatePub(strPubUrl,31337)#self.nPubPort)
		self.objNanoHippoDev.CreateRep(strRepUrl)

		self.objNanoHippoDev.SetFilterColorCode(1)
		self.objNanoHippoDev.SetFilterUnreadable(1)

		self.m_objBLog = LogClient(self.nSlotId, "dut.log")

		self.objPotassiumLock = LockClient("potassium", "{}".format(nSlotId))

		print "{} Auto Potassium Id :{}".format(self.nSlotId,self.PotassiumUrl)



	
	def PotassiumReset_b(self): 
		self.Close()
		bRet = True
		if bRet:
			self.objPotassiumLock.Lock(True)
			bRet = self.objKtool.KtoolRun_b(self.PotassiumUrl,"reset","Reset complete")
			self.objPotassiumLock.Lock(False)
			if bRet:
				self.m_objBTime.Delay(5000)
				bRet = self.Connect_b()
				if bRet:
					self.m_objBTime.Delay(1000)
					self.DutSendString_n("")
					self.m_objBTime.Delay(1000)
					self.DutReadString_str()
		return bRet



	def Connect_b(self):
		#bRet,strPotassiumId = self.objPotassiumFinder.GetPotassiumId_b_str(self.nSlotId,True)
		bRet = True
		strPotassiumId = self.PotassiumUrl
		if bRet:
			if self.bConnectFlag:
				#self.objNanoHippoDev.closeAll()
				self.bConnectFlag=False
			self.m_objBLog.Trace("Potassium Open {} Start".format(strPotassiumId))
			nRet=  self.objNanoHippoDev.openSerial(strPotassiumId)
			self.m_objBTime.Delay(1000)
			self.m_objBLog.Trace("Potassium Open {} End, {}".format(strPotassiumId,nRet))
			if nRet<0:
				self.m_objBLog.Trace("Potassium Open Error {}".format(strPotassiumId))
				self.bConnectFlag = False
			else:
				self.bConnectFlag=True
		return self.bConnectFlag


	def SetLogPaths(self,listNPort,listStrPath):
		if len(listNPort) != len(listStrPath):
			print "SetLog File Len different !!!! {} VS {}".format(str(listNPort),str(listStrPath))
		else:
			for i in range(0,len(listNPort)):
				nRet = self.objNanoHippoDev.SetLogFile(listNPort[i], listStrPath[i])
				self.m_objBLog.Trace("Set Log File {}:{} Ret:{}".format(listNPort[i], listStrPath[i],nRet))
	def SetLogfile( self,strDefaultLogAddr,nPort=-1):
		self.objNanoHippoDev.SetLogFile(nPort,strDefaultLogAddr)

	def SetSmcLogfile( self,nPort,strDefaultLogAddr ):
		self.objNanoHippoDev.SetLogFile(nPort,strDefaultLogAddr)


	def DutSendString_n(self,strData,nPort=31337):
		nRet = -1
		if self.bConnectFlag:
			self.m_objBTime.Delay(100)
			strWriteData = "\n"
			if nPort == None or nPort == "":
				nPort = 31337
			if strData.upper().find("ENTER")<0:
			    strWriteData = "{}\n".format(strData)

			nRet = self.objNanoHippoDev.WriteString(nPort,strWriteData)
		else:
			print "DutSendString_n Potassium Didn't Connect !!"
		return nRet
	def DutWaitStr_n(self,strDetect,nTimeout,nPort=31337):
		nRet = -1
		if self.bConnectFlag:
			if nPort == None or nPort == "":
				nPort = 31337
			nRet = self.objNanoHippoDev.WaitDetectStr(nPort,strDetect,nTimeout)

			print "dut waitforstring {}".format(strDetect)

		else:
			print "DutSendCmd_n_str Potassium Didn't Connect !!"
		return nRet



	def ClearBuffer(self,nPort=31337):
		nRet = -1
		if self.bConnectFlag:
			if nPort == None or nPort == "":
				nPort = 31337
			self.objNanoHippoDev.ClearBuffer(nPort)
		else:
			print "ClearBuffer Potassium Didn't Connect !!"
		return nRet

	
	def DutSetDetectString(self,strData):
		self.objNanoHippoDev.SetDetectString(strData)

	def DutGetDetectString(self):
		return self.objNanoHippoDev.GetDetectString()

	def DutWaitForString_n_str(self,nTimeout,nPort=31337):
		#if nPort == nil or nPort == "" then nPort = 31337
		nRet = -1
		strRet = ""
		if self.bConnectFlag:
			if nPort == None or nPort == "":
				nPort = 31337

			nRet = self.objNanoHippoDev.WaitDetect(nPort,nTimeout)

			strRet = ""
			if nRet==-1:
				strRet = "connection disconnect"
			elif nRet==-2:
				strRet = "Timeout"
			elif nRet!=0:
				strRet = "Unknow Error occur EFI_MODULEWait_For_String_"
		else:
			print "DutWaitForString_n_str Potassium Didn't Connect !!"
		return nRet,strRet


	def DutSendCmd_n_str(self,strCmd,nTimeout,nPort=31337):
		nRet = -1
		strRet = ""
		if self.bConnectFlag:
			if nPort == None or nPort == "":
				nPort = 31337

			self.DutSendString_n(strCmd,nPort)

			print "dut send cmd {}".format(strCmd)
			nRet, strRet= self.DutWaitForString_n_str(nTimeout,nPort)
			print "dut waitforstring {}".format(strCmd)

		else:
			print "DutSendCmd_n_str Potassium Didn't Connect !!"
		return nRet, strRet


	def DutReadString_str(self,nPort=31337):

		strRet = ""
		nTryTime=3
		if self.bConnectFlag:
			self.m_objBTime.Delay(30)
			if nPort == None or nPort == "":
				nPort = 31337

			strRet= self.objNanoHippoDev.ReadString(nPort)

			if strRet!="":
				self.ClearBuffer(nPort)
				bRet,strRet=self.m_objBRe.SubStr_b_str(strRet,"\+","")


		else:
			print "DutReadString_str Potassium Didn't Connect !!"

		print "dut read {}".format(strRet)
		return strRet
	
	
	
	def WriteCB(self,nSd, strCmd ,nPort=31337):
		nRet = -1
		if self.bConnectFlag:
			nRet = self.objNanoHippoDev.WritePassControlBit(nPort,nSd,strCmd)
		else:
			print "WriteCB Potassium Didn't Connect !!"
		return nRet
	
	
	
	def Close(self):
		if self.bConnectFlag:

			self.objNanoHippoDev.closeAll()

		else:
			print "Close Potassium Didn't Connect !!"




	def CheckAlive_n(self,nCount,strData):
		nRet = -1
		if self.bConnectFlag:
			if strData == None:
				strData = ":-)"

			self.DutSetDetectString(strData)
			nRet = -1
			for i in range(0,nCount):#(1) do
			    nRet = self.DutSendCmd_n("",1000)
			    if nRet == 0:
			        nRet=0
			       	break
		else:
			print "CheckAlive_n Potassium Didn't Connect !!"
		return nRet

	def LoopTryConnection(self,nCount,nPort=31337):
		strDutRespond = ""

		#if nCount == None or nCount == "" then nCount = 500
		bRet = True
		if self.bConnectFlag:
			if type(nCount) == int and type(nPort) == int:
				self.DutSetDetectString(":-)")

				nRet = -1
				for i in range(0,nCount):#(1) do
					nRet = self.DutSendCmd_n("version",9000)
					if nRet != 0:
						bRet = False
						break
					time.sleep(1)
					strDutRespond = self.objNanoHippoDev.ReadString(nPort)

					if strDutRespond==None:
						bRet = False
						break
					time.sleep(0.001)
		return bRet

class cCArmDLpy:
	def __init__(self,nUut,dictDataLog,nPubPort):
		self.dictDataLog=dictDataLog
		self.nUut=nUut
		self.strIp = "169.254.1.{}".format(32+int(self.nUut))
		self.nPort = 7611
		self.libArm = LibArmDl()
		self.strMid = "cCArmDLpy_{}".format(self.nUut)
		self.strHeader= ""

		#self.strLogFileName="{}_log.csv".format(self.strMid)
		self.strUrl= "tcp://*:{}".format(nPubPort + self.nUut)
		self.Init()
		self.Connect()
	def Init(self):
		self.strHeader=""
		for i in range(0,4):
			self.strHeader = self.strHeader+"timestamp"+"{}".format(i+1)+","+self.dictDataLog["CH{}".format(i+1)][4]
			if i<3:
				self.strHeader = self.strHeader+","
			else:
				self.strHeader =self.strHeader + "\r\n"

	def Connect(self):
		if self.libArm:
			self.libArm.CreateTCPClient(self.strMid,self.strIp,self.nPort)
			for i in range(0,4):
				print float(eval(self.dictDataLog["CH{}".format(i+1)][0])),\
										   float(eval(self.dictDataLog["CH{}".format(i + 1)][1])),\
										 float(eval(self.dictDataLog["CH{}".format(i + 1)][2])),\
										 float(eval(self.dictDataLog["CH{}".format(i + 1)][3]))
				self.libArm.updateConfig(i,float(eval(self.dictDataLog["CH{}".format(i+1)][0])),\
										   float(eval(self.dictDataLog["CH{}".format(i + 1)][1])),\
										 float(eval(self.dictDataLog["CH{}".format(i + 1)][2])),\
										 float(eval(self.dictDataLog["CH{}".format(i + 1)][3])), 1, 1000)
			self.libArm.CreatZmqPub(self.strUrl)

		else:
			print "Connect libArm Obj Didn't Create"

	def SetLogPath(self,strLogPath):
		if self.libArm:
			self.libArm.setLogPath(self.strHeader, "{}/{}".format(strLogPath,self.strMid))
		else:
			print "SetLogPath libArm Obj Didn't Create"
	def StartDataLog(self,strLogPath):
		self.SetLogPath(strLogPath)
		if self.libArm:
			self.libArm.startDataLogger()
		else:
			print "StartDataLog libArm Obj Didn't Create"
	def StopDataLog(self):
		if self.libArm:
			self.libArm.stopDataLogger()
		else:
			print "StopDataLog libArm Obj Didn't Create"

class cPowerSequence:
	def __init__(self,nUut,dictDataLog,nPubPort):
		self.dictDataLog=dictDataLog
		self.nUut=nUut
		self.strIp = "169.254.1.{}".format(32+int(self.nUut))
		self.nPort = 7621
		self.libPs = LibPs()
		self.strMid = "cPowerSequence_{}".format(self.nUut)
		self.strHeader= ""

		#self.strLogFileName="{}_log.csv".format(self.strMid)
		self.strUrl= "tcp://*:{}".format(nPubPort + self.nUut)
		self.strChannelConfig = ""
		self.Init()

		self.bStartFlag=False

		self.Connect()



	def Init(self):
		self.strHeader=""
		for i in range(0,40):
			channel_temp = "CH{}".format(i+1)
			self.strChannelConfig = self.strChannelConfig+";"+self.dictDataLog[channel_temp][0]+","+str((5.002 * float(eval(self.dictDataLog[channel_temp][1]))))+","+(self.dictDataLog[channel_temp][2])+","+(self.dictDataLog[channel_temp][3])
		self.strChannelConfig=self.strChannelConfig[1:]

	def Connect(self):
		if self.libPs:
			self.libPs.CreateTCPClient(self.strMid,self.strIp,self.nPort)
			self.libPs.updateConfig(self.strChannelConfig,1,self.nUut)
			self.libPs.CreatZmqPub(self.strUrl)
		else:
			print "Connect libArm Obj Didn't Create"

	def StartDataLog(self,strLogPath,strType,nFlag=1):
		if self.libPs:
			if self.bStartFlag==False:
				self.libPs.startDataLogger("{}/{}_{}_PS.csv".format(strLogPath,self.strMid,strType),nFlag)
				self.bStartFlag=True
		else:
			print "StartDataLog libArm Obj Didn't Create"
	def StopDataLog(self,nFlag=1):
		if self.libPs:
			if self.bStartFlag==True:
				self.libPs.stopDataLogger(nFlag)
				self.bStartFlag=False
		else:
			print "StopDataLog libArm Obj Didn't Create"




