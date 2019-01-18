from Common.tinyrpc.dispatch import public
#from TestEngine.Driver.zynqdriver import ZYNQ
from Common.BBase import *
from FixtureCtl.FixtureClient import FixtureClient
from Log.LogClient import LogClient
from ThirdParty.LibCallPy import *
class CallBack(object):
    def __init__(self, dictArgs):
        super(CallBack, self).__init__()
        self.zynq = dictArgs["zynq"]
        self.dut = dictArgs["dut"]
        self.m_objTimer = cBruceTime()
        self.m_objFixtureClient = FixtureClient()
        self.objDataLog = cCArmDLpy(self.zynq.uut,self.zynq.io_table["DataLog"],zmqports.DATALOGGER_PUB)
        self.m_objLogClient= LogClient("dut{}".format(self.zynq.uut),"CallBack.log")



    @public('start_test')
    def start_test(self, *args, **kwargs):

        self.m_objLogClient.Trace(" Start Test Call")
        self.m_objTimer.Start()
        self.zynq.reset()
        self.zynq.MonitorCtrl()
        self.m_objTimer.Delay(500)
        self.zynq.LogAndPsReset()
        self.zynq.UsbfsKill()
        strOfflineLogPath = self.m_objLogClient.GetCurrentFolderPath()
        strOnlineLogPath = self.m_objLogClient.GetOnlineFolderPath()
        strOnlineProjectName = self.m_objLogClient.GetOnlineProjectName()
        self.dut.SetLogPath(strOfflineLogPath,31337)
        strSmcLogPath = self.dut.SetLogPath(strOnlineLogPath, 31339,strProjectName="J140")
        self.zynq.cmd_raw_send("datalogger close(ALL)")
        self.objDataLog.StopDataLog()
        self.zynq.cmd_raw_send("datalogger open(ALL,ADC_NORMAL)")
        self.objDataLog.StartDataLog(strOfflineLogPath)
        return strSmcLogPath

    @public('end_test')
    def end_test(self, *args, **kwargs):


        self.zynq.reset()
        self.zynq.LogAndPsReset()
        self.zynq.cmd_raw_send("datalogger close(ALL)")
        self.zynq.cmd_raw_send("power sequence monitoring stop()")
        self.objDataLog.StopDataLog()
        self.zynq.stop_ps_thread()

        return ""

    @public('totaltime')
    def totaltime(self, *args, **kwargs):
        # a = ZYNQ()
        totaltime = self.m_objTimer.Stop_n()
        strResult="%0.03f"%(float(totaltime)/1000)
        return strResult


    @public('_my_rpc_server_is_ready')
    def sequencerRigister(self, *args, **kwargs):
        print("sequencerRigister")
        return "--PASS--"
