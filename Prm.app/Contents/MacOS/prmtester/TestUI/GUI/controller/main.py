# coding=utf-8
import sys
import time
import os

from TestUI.GUI.view.mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QMessageBox, QFileDialog, \
    QHeaderView,QHBoxLayout,QStatusBar,QLabel
from PyQt5.QtCore import QTimer, QModelIndex

from PyQt5.QtCore import QThread
from TestUI.GUI.module.model import TableViewModel, CheckBoxHeader, QColor, MyDelegate
from PyQt5 import QtGui
from Common.tinyrpc.protocols.StateMachineRpc import StateMachineRPCProtocol
import Common.zmqports as zmqports
from TestUI.Net.myzmq import SubcribeManagement, SmFixture
from Common.Processmanagement import ProcessManagement, OpenScript
import Common.events as events
from TestUI.GUI.module.Treemodel import TreeModel, TreeViewDelegate
from PyQt5 import QtCore
from TestUI.GUI.view.HBmodule import HBModule
from tidconfig import TID_CFG



FRAMWIDTH = 0.8
FRAMHEIGHT = 0.8

pwd = os.path.dirname(__file__)
sys.path.append(os.path.abspath("./Core"))
profile = "/Users/gdlocal/Public/PRMeasurement/Profile"


qssTree = """
QTreeView {
    show-decoration-selected: 1;
    font: "Timers" ;
    font-size:  13px;
}

QTreeView::item {
    border: 1px solid #d9d9d9;
    border-top-color: transparent;
    border-bottom-color: transparent;
}

QTreeView::item:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
    border: 1px solid #bfcde4;
}

QTreeView::item:selected {
    border: 1px solid #567dbc;
}

QTreeView::item:selected:active{
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
}

QTreeView::item:selected:!active {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);
}




"""
# padding-left: 4px;
header = """

    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
    stop:0 rgba(230, 230, 230, 255),
    stop:1 rgba(250, 250, 250, 255));


    border: 1px solid #E6E6E6;
    min-height: 25px;

    font-size:  14px;
    font: bold large "Timers" ;
"""

verticalscrollbar = """
QScrollBar:vertical
{
    width:8px;
    background:rgba(0,0,0,0%);
    margin:0px,0px,0px,0px;
    padding-top:9px;
    padding-bottom:9px;
}
QScrollBar::handle:vertical
{
    width:8px;
    background:rgba(0,0,0,25%);
    border-radius:4px;
    min-height:20;
}
QScrollBar::handle:vertical:hover
{
    width:8px;
    background:rgba(0,0,0,50%);
    border-radius:4px;
    min-height:20;
}

"""

horizontalscrollbar = """
QScrollBar:horizontal
{
    width:8px;
    background:rgba(0,0,0,0%);
    margin:0px,0px,0px,0px;
    padding-top:9px;
    padding-bottom:9px;
}
QScrollBar::handle:horizontal
{
    width:8px;
    background:rgba(0,0,0,25%);
    border-radius:4px;
    min-height:20;
}
QScrollBar::handle:horizontal:hover
{
    width:8px;
    background:rgba(0,0,0,50%);
    border-radius:4px;
    min-height:20;
}

"""


class Position():

    def __init__(self):
        self.x = 0
        self.y = 0


class UutPosition():

    def __init__(self):
        self.position = dict()
        self.positionInit()

    def positionInit(self):
        self.position.setdefault(5, Position())
        self.position.setdefault(6, Position())
        self.position.setdefault(7, Position())
        self.position.setdefault(8, Position())

    def setPosition(self, col, x, y):
        self.position.get(col).x = x
        self.position.get(col).y = y

    def getPosition(self, col):
        return self.position.get(col)






from Common.BBase import *
from FixtureCtl.FixtureClient import FixtureClient
import Universal
import CoreAPI
import threading
#from Log.LogClient import LogClient




class cPLCThreadSend(QThread):
    def __init__(self,Main =None,Frequence=2000):
        super(cPLCThreadSend, self).__init__()
        self.objTimer = cBruceTime()
        self.objSta = Main
        self.nFrequence = Frequence


    def Stop(self):
        self.bRun = False


    def run(self):
        self.bRun = True
        while self.bRun:
            self.objTimer.Delay(self.nFrequence)
            #self.objSta.objPlcArmLog.Trace(self.objSta.PlcArmMeesageFormat())
            self.objSta.objUniverDriver.Send(self.objSta.PlcArmMeesageFormat())
class cPLCQsmcThreadRecv(QThread):
    def __init__(self,Main =None,Frequence=2000):
        super(cPLCQsmcThreadRecv, self).__init__()
        self.objTimer = cBruceTime()
        self.objSta = Main
        self.nFrequence = Frequence


    def Stop(self):
        self.bRun = False


    def run(self):
        self.bRun = True
        while self.bRun:
            self.objTimer.Delay(self.nFrequence)
            bRet,strCmd = self.objSta.objUniverDriver.Recv()

            if bRet:
                print "PLC Get {}".format(strCmd)
    
                if "CLOSE" in strCmd:
                    for i in range (0,3):
                        if self.objSta.fixture.StartWithDutCheck()==0:
                            break
                        else:
                            print "StartWithDutCheck Fail {}".format(i)
                elif "OPEN" in strCmd:
                    for i in range(0,3):                      
                        if self.objSta.fixture.EndWithOUT()==0:
                            break
                        else:
                            print "EndWithOUT Fail {}".format(i)



class cPLCFxcnThreadFile(QThread):
    def __init__(self,fixture,Main =None,Frequence=2000):
        super(cPLCFxcnThreadFile, self).__init__()
        self.m_strCmdPath    = "CMD.txt"
        self.m_strStatusPath = "Status.txt"
        self.m_strResultPath = "Result.txt"
        self.m_strFolder     = "/vault/AUTO"
        self.objTimer        = cBruceTime()
        self.objSta          = Main
        self.nFrequence      = Frequence
        self.m_objShell      = cShell()
        self.fixture = fixture
        self.FxcdArm = cAutoFoxArm(self.m_strFolder,self.m_strResultPath,self.m_strCmdPath,self.m_strStatusPath,4)

        self.FinishFlag =1
        self.listSn = []
        self.listResult = []
    def SetResult(self,listSn,listResult):
        if self.FinishFlag==1:
            self.listSn = listSn
            self.listResult = listResult
            self.FinishFlag = 0

    def Stop(self):
        self.bRun = False

    def run(self):
        self.bRun = True
        strFirstStatus = "CLOSE" if (self.fixture.CheckMotion(self.fixture.send_cmd("IN STATUS"))) else "OPEN"

        self.FxcdArm.StatusFile(strFirstStatus)

        while self.bRun:
            self.objTimer.Delay(self.nFrequence)
            nRet = self.FxcdArm.CheckCMDFileExist()
            print "[][][][][][][][][][][][] Check CMD exit {}".format(nRet)

            if  nRet==0 :
                strCmd = self.FxcdArm.CMDFile()
                if "CLOSE" in strCmd:
    
                    print "Run Cmd Close"
                    for i in range (0,3):
                        if self.fixture.StartWithDutCheck()==0:
                            self.FxcdArm.deleteCMDFile()
                            self.FxcdArm.StatusFile("CLOSE")
                            break
                        else:
                            print "StartWithDutCheck Fail {}".format(i)
    
                elif "OPEN" in strCmd:
                    print "Run Cmd Open"
                    for i in range(0,3):                      
                        if self.fixture.EndWithOUT()==0:
                            self.FxcdArm.deleteCMDFile()
                            self.FxcdArm.StatusFile("OPEN")
                            break
                        else:
                            print "EndWithOUT Fail {}".format(i)                   
            else:
                if self.FinishFlag ==0:
                    self.FxcdArm.ResultFile(self.listSn,self.listResult)
                    self.listSn=[]
                    self.listResult = []
                    self.FinishFlag =1

#FXCN cBruceConfig(strConfigPath)

class cPlcArm:
    def __init__(self):
        self.dictStationConfig = cBruceConfig("/vault/data_collection/test_station_config/gh_station_info.json")
        #self.dictStationConfig = cBruceConfig("/vault/AUTO/gh_station_info.json")
        self.strFactory = self.dictStationConfig.GetDict().get("ghinfo").get("SITE")

        self.fixture = FixtureClient()
        if self.strFactory=="QSMC":

            self.dictRack = {"rackid": "01", "drawerid": "01"}

            self.dictConfig = {"ip": "127.0.0.1", "port": 9009, "timeout": -1, "prefix": "", "postfix": ""}
            self.objUniverDriver =Universal.cUniversalDriver(Universal.DRIVERTYPE.TCP_CLIENT, self.dictConfig)

            print "PLC Connect {}".format(self.objUniverDriver.Connect())

            self.objPlcArmRecvThread = cPLCQsmcThreadRecv(self, 2000)
            self.objPlcArmSendThread = cPLCThreadSend(self,5000)
        elif self.strFactory=="FXCD":
            self.FXCDThread = cPLCFxcnThreadFile(self.fixture)

        self.nFirstTest = 0

        self.dictSlotStauts={}

        

        self.InitSlot(4)

        


    def InitSlot(self,nSize):
        for  i  in range(0,nSize):
            self.dictSlotStauts[i]={}
    def SetSlotStatus(self,nIndex,strStatus):
        if nIndex in self.dictSlotStauts.keys():
            self.dictSlotStauts[nIndex]["status"]=strStatus
        #self.objPlcArmLog.Trace("SetStatus {}:{} {}".format(nIndex,self.dictSlotStauts,self.PlcArmMeesageFormat()))
    def SetSlotResult(self,nIndex,strStatus):
        if nIndex in self.dictSlotStauts.keys():
            self.dictSlotStauts[nIndex]["result"]=strStatus
    def SetResult(self,listSn,listResult):
        if self.strFactory=="FXCD":
            self.FXCDThread.SetResult(listSn,listResult)
        #self.objPlcArmLog.Trace("SetResults {}:{} {}".format(nIndex,self.dictSlotStauts,self.PlcArmMeesageFormat()))

    def PlcArmMeesageFormat(self):
        strLastMessage = ""
        for i in range(0, 4):
            nDrawerStatus = 1 if (self.fixture.CheckMotion(self.fixture.send_cmd("IN STATUS"))) else 0
            nMaterialStatus = 1 if self.fixture.CheckMotion(self.fixture.send_cmd("DUT{} STATUS".format(i + 1))) else 0
            nEngagedStatus = 1 if (self.dictSlotStauts.get(i) and self.dictSlotStauts.get(i).get("status") and  self.dictSlotStauts.get(i).get("status")== "TESTING") else 0
            nFixtureStatus = 0 
            nResultStatus = 1 if (self.dictSlotStauts.get(i) and self.dictSlotStauts.get(i).get("result") and  self.dictSlotStauts.get(i).get("result")== "PASS")  else 0
            if nEngagedStatus==1:
                nResultStatus="*"

            if self.nFirstTest==0:
                nResultStatus="*"
                if nEngagedStatus ==1:
                    self.nFirstTest = -1

            if nMaterialStatus==0:
                nResultStatus="*"

            strLastMessage +="{}:{}:0{}:{}{}{}{}{}".format(self.dictRack["rackid"],self.dictRack["drawerid"],i+1,nDrawerStatus, nMaterialStatus,nEngagedStatus,nFixtureStatus,nResultStatus)
        print "PLC CMD:{}".format(strLastMessage)
        return strLastMessage
        #return "01:01:00:1100001:01:01:1100001:01:02:1100001:01:03:11000"

    def StartPlcArm(self):
        if self.strFactory == "FXCD":
            self.FXCDThread.start()
        elif self.strFactory == "QSMC":
            self.objPlcArmSendThread.start()
            self.objPlcArmRecvThread.start()

    def StopPlcArm(self):
        if self.strFactory == "FXCD":
            self.FXCDThread.Stop()
        elif self.strFactory == "QSMC":
            self.objPlcArmSendThread.Stop()
            self.objPlcArmRecvThread.Stop()

class cFansThread(QThread):
    def __init__(self,Main =None,Frequence=2000):
        super(cFansThread, self).__init__()
        self.objTimer = cBruceTime()
        self.objHb = Main
        self.nFrequence = Frequence

        self.fixture = FixtureClient()


    def Stop(self):
        self.bRun = False


    def run(self):
        self.bRun = True
        while self.bRun:
            self.objTimer.Delay(self.nFrequence)
            strInfos = self.fixture.send_cmd("READ FAN")
            print strInfos


            for i in range(0,4):
                if  self.fixture.CheckFans(i,strInfos) == "OK":
                    self.objHb.SetFansStatus("fans",i, 1)
            for i in range(0,4):
                if  self.fixture.CheckFansR(i,strInfos) == "OK":
                    self.objHb.SetFansStatus("fansR",i, 1)
            for i in range(0,4):
                if  self.fixture.CheckFansL(i,strInfos) == "OK":
                    self.objHb.SetFansStatus("fansL",i, 1)
            for i in range(0,2):
                if  self.fixture.CheckFansB(i,strInfos) == "OK":
                    self.objHb.SetFansStatus("fansB",i, 1)

class UiMainWindow(QMainWindow, Ui_MainWindow):
    laststate = dict()
    screen = False
    cltimes = 1
    loop = False
    ps = UutPosition()
    lastscrool = 0
    alinfo = list()
    cleanflag = True

    def __init__(self, parent=None, UpdateUI=None, sm_remote=None):
        super(UiMainWindow, self).__init__(parent)
        # setup the process of the other module

        self.UpdateUI = UpdateUI
        self.setupUi(self)


        self.p = ProcessManagement()

        self.p.startPrmLogSever()
        self.p.startPrmLockSever()

        self.p.start_fixture_server()

        self.p.startupAllProcess()

        # add start fixture server   --jinhui.huang
        

        # open PDCA
        self.p.startPdcaSever(switch=True)


        self.sm_remote = sm_remote

        self.mymodule = TreeModel()
        self.treeView.setModel(self.mymodule)
        self.treeView.header().setStyleSheet(header)
        self.treeView.verticalScrollBar().setStyleSheet(verticalscrollbar)
        self.treeView.horizontalScrollBar().setStyleSheet(verticalscrollbar)

        # self.mydelegate = TreeViewDelegate()
        # self.treeView.setItemDelegate(self.mydelegate)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setStyleSheet(qssTree)

        self.failmodule = None
        #self.failmodule.rootItem.insertChildren(0,1,self.failmodule.rootItem.columnCount())

        self.ftreeView.header().setStyleSheet(header)
        self.ftreeView.verticalScrollBar().setStyleSheet(verticalscrollbar)
        self.ftreeView.horizontalScrollBar().setStyleSheet(verticalscrollbar)
        self.ftreeView.setAlternatingRowColors(True)
        self.ftreeView.setStyleSheet(qssTree)



        self.start.clicked.connect(self.startButton)
        self.abort.clicked.connect(self.stopButton)

        self.enterIntoOpMode()
        self.actionsupervisor.triggered.connect(self.enterIntoPassWord)
        self.actionOperator.triggered.connect(self.enterIntoOpMode)
        self.actionPdcaclose.triggered.connect(self.closePdca)
        self.actionPdcaopen.triggered.connect(self.openPdca)
        self.actionOpen.triggered.connect(self.getfile)
        self.actionLoopTest.triggered.connect(self.openLoopTest)
        # self.actionScriptEditorTool.triggered.connect(self.openScriptEditor)
        self.actionSet_Password.triggered.connect(self.setPassWord)

        self.actionClean.triggered.connect(self.cleanMode)

        self.mg = SubcribeManagement()
        self.mg.start_all_threading()
        self.mg.connect_all_signal(self.updateQtableView)


        self.sm = SmFixture()
        self.sm.start()
        self.sm.sig.connect(self.smStartMessage)


        self.hb = HBModule(num=4)
        self.statusBar = QStatusBar(parent=self)
        self.statusBar.addWidget(self.hb)
        self.setStatusBar(self.statusBar)





        self.scanSn.textChanged.connect(self.snChanged)
        self.hb.setPdca(True)

        self.center()
        time.sleep(6)
        self.loadCSV()

        self.objPlcArm = cPlcArm()
        self.objPlcArm.StartPlcArm()

        self.objFansThread = cFansThread(Main =self.hb)
        self.objFansThread.start()

        self.abort.setDisabled(False)


        for key,value in self.sn.sndict.iteritems():
            value.sn.sig.connect(self.CheckChange)

        self.sn.clickCheckBox()

    def GetSnList(self):
        return self.sn.getSnList()
    def GetResultList(self):
        return self.sn.getResultList()

    def closeEvent(self,Event):
        reply = QMessageBox.question(self,'PrmTester',"you want to quit ？",
                                               QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.No)
        if reply == QMessageBox.Yes:
            Event.accept()
            self.closeProcess()
        else:
            Event.ignore()
    def closeProcess(self):
        # self.p.killAll()
        #self.p.killPid(os.getpid())
        #cShell().RunShell_n("Python ../kill/KillPRM.py")
        CoreAPI.killPlatform()


    def keyPressEvent(self, QKeyEvent):
        try:
            if QKeyEvent.key() == QtCore.Qt.Key_F2:
                self.startButton()
        except Exception as e:
            print (e)

    # 屏幕剧中显示
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        wd = screen.width()
        hg = screen.height()
        self.resize(wd*FRAMWIDTH,hg*FRAMHEIGHT)
        size = self.geometry()
        self.move((wd - size.width()) / 2,
                  (hg - size.height()) / 2)
        self.show()

    # 打开LoopTest的UI
    def openLoopTest(self):
        self.loop = True
        self.UpdateUI(1)

    def updateQtableView(self, data):

        print "Check MESSAGE update{}".format(data)
        if not isinstance(data, dict):
            return None
        event = data.get("event")
        if event == events.LIST_ALL:
            self.showData(data.get("result"))
        elif event == events.ITEM_FINISH:
            self.showResult(data)
        elif event == events.ITEM_START:
            self.module_position(data)
        elif event == events.SEQUENCE_END:
            self.sn.setResult(data.get("name"),data.get("result"))
            if data.get("result") < 1:
                self.pst.resultFail()
            else:
                self.pst.resultPass()
            self.sn.stop(data.get("name"))

            self.objPlcArm.SetSlotStatus(data.get("name") - zmqports.SEQUENCER_PUB, "FNISH")


            self.objPlcArm.SetSlotResult(data.get("name") - zmqports.SEQUENCER_PUB, "PASS" if data.get("result") else "FAIL")

            self.sn.SetSlotResult(data.get("name") - zmqports.SEQUENCER_PUB, "PASS" if data.get("result") else "FAIL")


            self.scanSn.setDisabled(False)
            self.cleanflag = True
            self.start.setDisabled(False)
            #self.abort.setDisabled(True)


            if self.sn.getAllFinishStatus():
                self.failmodule = None
                self.objPlcArm.SetResult(self.sn.getSnList(),self.sn.getResultList())

        elif event == events.UOP_DETECT:
            print "UOP MESSAGE EVENT COMING"
            self.uopError(data.get("result"))
            #self.start.setDisabled(False)
            #self.abort.setDisabled(True)
        elif event == events.HEATBEAT:
            self.hb.setHartBeat(data.get("name"))
        elif event == events.SEQUENCE_START:
            self.scanSn.setDisabled(True)
            self.sn.InitInfos()
            self.sn.setResult(data.get("name"),2)


            self.objPlcArm.SetSlotStatus(data.get("name") - zmqports.SEQUENCER_PUB,"TESTING")
            self.sn.start(data.get("name"))
            self.lastscrool = 0
            self.startTestInit(data.get("col"),data.get("name"))


            if self.failmodule == None:
                self.alinfo = []
                self.failmodule = TreeModel()
                self.ftreeView.setModel(self.failmodule)
                #self.failmodule.rootItem.insertChildren(0,1,self.failmodule.rootItem.columnCount())

    def snChanged(self):
        serN = self.scanSn.text().strip()
        if len(serN)==17:
            result = self.sn.scanSn(str(serN))
            print serN
            self.scanSn.setText("")


    def getfile(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select test plan',
                                                  profile,
                                                  options=QFileDialog.DontUseNativeDialog)

        if 'csv' in filename:
            self.mg.set_level(False)
            self.loadScipt(filename)
            self.listAll()
            self.parse_csv(str(filename).split("/")[-1])



    def reFlash(self):
        for index, value in self.state.iteritems():
            if value == False:
                self.hblabel[index].setPixmap(QtGui.QPixmap(":/picture/disconnect.png"))
            else:
                self.hblabel[index].setPixmap(QtGui.QPixmap(":/picture/connect.png"))
        for index in self.state:
            self.state[index] = False


    def showData(self, data):
        print "Show Data Call"
        self.mymodule.beginResetModel()
        self.mymodule.setupModelData(rowdata=data, parent=self.mymodule.rootItem)
        self.mymodule.endResetModel()
        self.treeView.expandAll()
        width = self.treeView.width()
        wd = (width - 250-250) / 4
        self.treeView.setColumnWidth(0, 100)
        self.treeView.setColumnWidth(1, 250)
        self.treeView.setColumnWidth(2, 50)
        self.treeView.setColumnWidth(3, 50)
        self.treeView.setColumnWidth(4, 50)
        self.treeView.setColumnWidth(5, wd)
        self.treeView.setColumnWidth(6, wd)
        self.treeView.setColumnWidth(7, wd)
        self.treeView.setColumnWidth(8, wd)
        self.treeView.hideColumn(9)
        self.treeView.hideColumn(10)
        self.treeView.hideColumn(11)
        self.treeView.hideColumn(12)

        self.mg.set_level(True)


    def showResult(self, data):
        col = data.get("col")
        if data.get("error") == None:
            if data.get("tid") == TID_CFG:
                self.sn.setSerialNumberByUut(col-5,data.get("value"))
            self.mymodule.rootItem.child(self.ps.getPosition(col).x).child(self.ps.getPosition(col).y).setData(col,data.get("value"))
            self.mymodule.rootItem.child(self.ps.getPosition(col).x).child(self.ps.getPosition(col).y).setData(col + 4,data.get("result"))
            parent = self.mymodule.index(self.ps.getPosition(col).x, 0)
            index = self.mymodule.index(self.ps.getPosition(col).y, 5, parent)
            index1 = self.mymodule.index(self.ps.getPosition(col).y, 8, parent)
            # index1 = self.mymodule.index(self.ps.getPosition(col).y,8)
            self.treeView.dataChanged(index, index1)
            a = int(self.mymodule.rootItem.child(self.ps.getPosition(col).x).child(self.ps.getPosition(col).y).data(0))
            if a > self.lastscrool:
                # self.treeView.scrollTo(index)
                self.treeView.setCurrentIndex(index)
                self.lastscrool = a

            #if not data.get("result"):
            if self.failmodule:
                self.failmodule.beginResetModel()
                width = self.ftreeView.width()
                wd = (width - 250-250) / 4
                self.ftreeView.setColumnWidth(0, 100)
                self.ftreeView.setColumnWidth(1, 250)
                self.ftreeView.setColumnWidth(2, 50)
                self.ftreeView.setColumnWidth(3, 50)
                self.ftreeView.setColumnWidth(4, 50)
                self.ftreeView.setColumnWidth(5, wd)
                self.ftreeView.setColumnWidth(6, wd)
                self.ftreeView.setColumnWidth(7, wd)
                self.ftreeView.setColumnWidth(8, wd)
                self.ftreeView.hideColumn(9)
                self.ftreeView.hideColumn(10)
                self.ftreeView.hideColumn(11)
                self.ftreeView.hideColumn(12)
                temp = list()
                group = self.mymodule.rootItem.child(self.ps.getPosition(col).x).data(0)
                temp.append(group)
                print "faile module",self.failmodule.rootItem.childCount(),self.failmodule.rootItem.columnCount()
                for i in range(9):
                    temp.append(self.mymodule.rootItem.child(self.ps.getPosition(col).x).child(self.ps.getPosition(col).y).data(i))


                bAllFinish = True
                bPassFlag = True
                nRow = self.ps.getPosition(col).x
                for j in range(5,9):
                    if not self.sn.getStatus(j) or self.sn.getCheckStatus(j) == False:
                        continue
                    if self.mymodule.rootItem.child(self.ps.getPosition(col).x).child(self.ps.getPosition(col).y).data(j) =="":
                        bAllFinish = False

                if bAllFinish:
                    for j in range(9,13):
                        print "Check Result is :{} {}".format(j,self.mymodule.rootItem.child(self.ps.getPosition(col).x).child(self.ps.getPosition(col).y).data(j))
                        if self.sn.getCheckStatus(j-4)==False:
                            continue
                        if not self.mymodule.rootItem.child(self.ps.getPosition(col).x).child(self.ps.getPosition(col).y).data(j) and self.mymodule.rootItem.child(self.ps.getPosition(col).x).child(self.ps.getPosition(col).y).data(j-4) !="":
                            bPassFlag = False

                    if bPassFlag==False:
                        self.alinfo.append(temp)
                        self.failmodule.rootItem.insertChildren(self.failmodule.rootItem.childCount(), 1, self.failmodule.rootItem.columnCount())
                        for i in range(13):
                            self.failmodule.rootItem.child(self.failmodule.rootItem.childCount()-1).setData(i, self.mymodule.rootItem.child(self.ps.getPosition(col).x).child(self.ps.getPosition(col).y).data(i))
                self.failmodule.endResetModel()
        else:
            # print data.get("error")
            QMessageBox.critical(self, "Error", data.get('error'))

    def module_position(self, data):
        group = data.get("group")
        tid = data.get("tid")
        # col = data.get("col")
        for i in range(self.mymodule.rootItem.childCount()):
            if self.mymodule.rootItem.child(i).data(0) == group:
                for j in range(self.mymodule.rootItem.child(i).childCount()):
                    if self.mymodule.rootItem.child(i).child(j).data(1) == tid:
                        self.ps.setPosition(data.get("col"), i, j)
                        return True
        return False

    def loadCSV(self):
        ph = OpenScript()
        dirfiles = os.listdir(profile)
        fn = ""
        try:
            for item in dirfiles:
                filename, extention  = os.path.splitext(item)
                print filename,extention
                if extention == ".csv":
                    path = str(profile + '/' + filename + extention)
                    fn = filename
                    print "Load Csv :{}".format(path)
                    self.mg.set_level(False)
                    self.loadScipt(path)
                    self.listAll()
                    self.parse_csv(str(path).split("/")[-1])
                    break
                else:
                    continue
        except Exception as e:
            pass

    def loadScipt(self, path=None):
        ph = OpenScript()
        if path is None:
            path = ph.getpath()
        req = StateMachineRPCProtocol()
        msg = req.create_request('load', path).serialize()
        print "Send To Sm :{}".format(path)
        self.sm_remote.client.transport.send_reply(msg)
        ph.savepath(path)

    def listAll(self):
        req = StateMachineRPCProtocol()
        msg = req.create_request('list', "all").serialize()
        self.sm_remote.client.transport.send_reply(msg)
        print "Send To Sm ListAll:{}".format(msg)

    def parse_csv(self,csv):
        try:
            t = str(csv).split("__")
            self.lb_staticon.setText(t[0])
            self.lb_version.setText(t[1])
        except Exception as e:
            return False

    def abortMessage(self):
        req = StateMachineRPCProtocol()
        msg = req.create_request('abort').serialize()
        self.sm_remote.client.transport.send_reply(msg)

    def cleanResult(self, col):
        index = self.mymodule.index(0, 5)
        index1 = self.mymodule.index(self.mymodule.rootItem.childCount() - 1, 8)
        for i in range(self.mymodule.rootItem.childCount()):
            for j in range(self.mymodule.rootItem.child(i).childCount()):
                self.mymodule.rootItem.child(i).child(j).setData(col, "")
                # self.mymodule.rootItem.child(i).child(j).setData(6, "")
                # self.mymodule.rootItem.child(i).child(j).setData(7, "")
                # self.mymodule.rootItem.child(i).child(j).setData(8, "")
        self.treeView.dataChanged(index, index1)

    def cleanMode(self):
        for i in range(4):
            self.cleanResult(i + 5)
        index = self.mymodule.index(0, 5)
        self.treeView.setCurrentIndex(index)

        # self.mymodule.beginResetModel()
        # # if self.mymodule.mylist:
        # #     for item in self.mymodule.mylist:
        # #         item[col]=""
        # self.mymodule.endResetModel()

    def startTestInit(self, col, name):
        if self.cleanflag:
            self.cleanflag = False
            self.cleanResult(5)
            self.cleanResult(6)
            self.cleanResult(7)
            self.cleanResult(8)
    def CheckChange(self):
        self.sn.clickCheckBox()
        e_travelers = self.sn.getMLBSN()
        if e_travelers:
            req = StateMachineRPCProtocol()
            t = req.create_request('checkchange', e_travelers)
            self.sm_remote.client.transport.send_reply(t.serialize())


    def startButton(self):
        e_travelers = self.sn.getMLBSN()
        if e_travelers:
            req = StateMachineRPCProtocol()
            t = req.create_request('start', e_travelers)
            self.sm_remote.client.transport.send_reply(t.serialize())
            #self.start.setDisabled(True)
            #self.abort.setDisabled(False)

    def stopButton(self):
        if not self.mg.get_status():
            req = StateMachineRPCProtocol()
            msg = req.create_request('abort').serialize()
            self.sm_remote.client.transport.send_reply(msg)


    def enterIntoOpMode(self):
        self.actionOpen.setDisabled(False)
        self.actionSet_Password.setDisabled(True)
        self.actionScriptEditorTool.setDisabled(True)
        self.actionLoopTest.setDisabled(True)
        self.actionPdcaopen.setDisabled(True)
        self.actionPdcaclose.setDisabled(True)
        self.abort.hide()

    def getStatus(self, name):
        try:
            cmd = str(name - 6250)
            req = StateMachineRPCProtocol()
            msg = req.create_request('status', cmd).serialize()
            res = self.sm_remote.client.transport.send_reply(msg)
            # print res
            if "READY" in res:
                return True
            else:
                return False
        except Exception:
            return False

    def smStartMessage(self, msg):
        pass
        # if "error" in msg:
        #     self.t_sm.setTextColor(QColor('red'))
        # else:
        #     self.t_sm.setTextColor(QColor('black'))
        # self.t_sm.append(msg)
        # if "DOWN\r" in msg:
        #     if not self.loop:
        #         self.startButton()
        # elif "OPEN\r" in msg:
        #     self.stopButton()


    def enterIntoSpMode(self):
        self.actionSet_Password.setDisabled(False)
        self.actionOpen.setDisabled(False)
        self.actionScriptEditorTool.setDisabled(False)
        self.actionLoopTest.setDisabled(False)
        self.abort.show()
        if self.actionPdcaclose.isEnabled():
            self.actionPdcaclose.setDisabled(False)
            self.actionPdcaopen.setDisabled(True)
        else:

            self.actionPdcaclose.setDisabled(True)
            self.actionPdcaopen.setDisabled(False)

    def openPdca(self):
        self.p.startPdcaSever(switch=True)
        self.actionPdcaopen.setDisabled(True)
        self.actionPdcaclose.setDisabled(False)
        self.hb.setPdca(True)


    def closePdca(self):
        self.p.startPdcaSever(switch=False)
        self.actionPdcaopen.setDisabled(False)
        self.actionPdcaclose.setDisabled(True)
        self.hb.setPdca(False)


    def mainWindow(self):
        self.stackedWidget.setCurrentIndex(0)


    def enterIntoPassWord(self):
        self.UpdateUI(2)

    def uopError(self, msg):
        print "Call UOPERROR {}".format(msg)
        QMessageBox.critical(self, "Error", msg)


    # def openScriptEditor(self):
    #     self.UpdateUI(3)

    def setPassWord(self):
        self.UpdateUI(4)

    def update_statistic(self, name, flag):
        if flag == 'P':
            self.lbl_pass[name].setText('%d' % (int(self.lbl_pass[name].text()) + 1))
        elif flag == 'F':
            self.lbl_fail[name].setText('%d' % (int(self.lbl_fail[name].text()) + 1))

        self.lbl_total[name].setText('%d' % (int(self.lbl_total[name].text()) + 1))
        rate = float(self.lbl_pass[name].text()) / float(self.lbl_total[name].text()) * 100

        self.lbl_rate[name].setText('%.2f' % rate)

    def reset_statistic(self):
        for i in range(6250, 6252):
            self.lbl_pass[i].setText("0")
            self.lbl_fail[i].setText("0")
            self.lbl_total[i].setText("0")
            self.lbl_rate[i].setText("0")
            self.result_status[i].setText("")
            self.result_status[i].setStyleSheet("background-color: rgb(250, 250, 250);")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    labelDemo = UiMainWindow()
    labelDemo.show()
    labelDemo.setFocus()

    sys.exit(app.exec_())
