# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget,QLabel,QBoxLayout,QApplication,QCheckBox,QHBoxLayout,QVBoxLayout,QFrame,QSpacerItem,QSizePolicy
from PyQt5.QtCore import Qt,QSize,QObject,QTimer,pyqtSignal
from PyQt5.QtGui import QFont
import time
from Common import zmqports

NORMAL = -1
PASS = 1
FAIL = 0
TESTING = 2
DISABLE = -2
STATUS = ("READY...", "DISABLE...", "PASS", "FAIL","TESTING")

class SerialNumberWidget(QFrame):

    sig = pyqtSignal(bool)
    def __init__(self, parent=None):
        super(SerialNumberWidget,self).__init__(parent)
        self.setFixedSize(300,40)
        self.setFrameShape(self.Box)
        self.setFrameShadow(self.Raised)
        mainlayout = QHBoxLayout()
        leftlayout = QVBoxLayout()
        midlayout = QVBoxLayout()
        rightlayout = QVBoxLayout()

        self._sn = QLabel()
        self._sn.setAlignment(Qt.AlignCenter)
        self._sn.setFont(QFont("Timers", 15))
        self._sn.setStyleSheet("color: rgb(255, 255, 255);")

        self._result = QLabel(STATUS[0])
        self._result.setFont(QFont("Timers", 14))
        self._result.setAlignment(Qt.AlignHCenter)
        self._result.setStyleSheet("color: rgb(255, 255, 255);")

        self.strResult = ""

        self._number = QLabel("1")
        self._number.setFixedSize(36,14)
        #self._number.setStyleSheet("background-color: rgb(255, 255, 255);")
        self._number.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self._number.setFont(QFont("Timers", 14))

        self._cb = QCheckBox()
        self._cb.clicked.connect(self.cbChecked)
        self.setChecked(True)

        leftlayout.addWidget(self._cb)
        leftlayout.setSpacing(0)
        leftlayout.addWidget(self._number)
        leftlayout.setContentsMargins(0,0,0,0)

        midlayout.addWidget(self._sn)
        #midlayout.addWidget(self._result)
        midlayout.setSpacing(0)
        #idlayout.setStretch(4,3)
        midlayout.setContentsMargins(0,0,0,0)


        rightlayout.addWidget(self._cb)
        rightlayout.setSpacing(0)
        rightlayout.setContentsMargins(0, 0, 0, 0)
        self.setResult(NORMAL)

        mainlayout.addLayout(leftlayout,1)
        mainlayout.addLayout(midlayout,12)

        mainlayout.setSpacing(0)
        mainlayout.setContentsMargins(0,0,0,0)
        self.setLayout(mainlayout)

    

    def setResult(self,result):
        if result == NORMAL:
            self.setStyleSheet("background-color: rgb(253, 200, 8);")
            self._sn.setText(STATUS[0])
            self.strResult = ""
        elif result == FAIL:
            self.setStyleSheet("background-color: rgb(255, 40, 40);")
            self._result.setText(STATUS[3])
            self.strResult = "FAIL"
        elif result == DISABLE:
            self.setStyleSheet("background-color: rgb(150, 150, 150);")
            self._sn.setText(STATUS[1])
            self.strResult = ""
        elif result == PASS:
            self.setStyleSheet("background-color: rgb(50, 255, 50);")
            self._result.setText(STATUS[2])
            self.strResult = "PASS"
        elif result == TESTING:
            self.setStyleSheet("background-color: rgb(70, 70, 255);")
            self._sn.setText(STATUS[4])
            self.strResult = ""

    def getResult2(self):
        return self.strResult 
    def getResult(self):
        return self._result.text()


    # def sizeHint(self):
    #     return QSize(300,65)

    def setSn(self,sn):
        if isinstance(sn,str):
            self._sn.setText(sn)
            return True
        else:
            return False

    def getSn(self):
        return self._sn.text()


    def setNumber(self,nb):
        self._number.setText(nb)

    def getNumber(self):
        return self._number.text()

    def isChecked(self):
        print self._cb.isChecked()
        return self._cb.isChecked()


    def cbChecked(self):
        if self._cb.isChecked():
            self.setResult(NORMAL)
        else:
            self.setResult(DISABLE)
        self.sig.emit(self.isChecked())

    def setChecked(self,bl):
        assert isinstance(bl,bool)
        if bool:
            self._cb.setChecked(bl)
            #self.setResult(NORMAL)
        else:
            self._cb.setChecked(bl)
            #self.setResult(DISABLE)

    def setCheckBox(self,bl):
        self._cb.setDisable(bl)





class Counter(QLabel):

    STARTTIME = 0
    def __init__(self, parent=None):
        super(Counter,self).__init__(parent)
        self.setMinimumWidth(50)
        self.setAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
        self.setFont(QFont("Timers", 16))
        #self.setStyleSheet("background-color: rgb(15, 128, 255);")
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.__startTest)
        self.setText("{} s".format(0))
        self.setStyleSheet("color: rgb(15, 128, 255);")
        #self.timer.start(100)
        #self.start()
        self.bTesting = False


    def __startTest(self):
        t = time.time() - self.STARTTIME
        self.setText(str(round(t,1))+"S")

    def start(self):
        self.STARTTIME = time.time()
        self._timer.start(100)
        self.bTesting =True




    def stop(self):
        self._timer.stop()
        self.STARTTIME = 0
        self.bTesting= False
    def GetTestStatus(self):
        return  self.bTesting



class SerialNumber2(QFrame):
    DEFAULTSERIALNUMBER = "READY..."
    def __init__(self,parent=None,num=1):
        super(SerialNumber2,self).__init__(parent)
        mainlayout = QHBoxLayout()
        self.sn = SerialNumberWidget()
        self.ct = Counter()
        self._num = num
        self.sn.setNumber("UUT{}".format(num))
        self.setDefaultSn()
        mainlayout.addWidget(self.sn)
        mainlayout.addWidget(self.ct)
        mainlayout.setStretch(4,1)
        mainlayout.setSpacing(0)
        mainlayout.setContentsMargins(0,0,0,0)
        self.setLayout(mainlayout)

    def setDefaultSn(self):
        #sn = self.DEFAULTSERIALNUMBER.format(self._num)
        self.setSerialNumber(self.DEFAULTSERIALNUMBER)
    def getTestStatus(self):
        return self.ct.GetTestStatus()


    def setSerialNumber(self,sn):
        self.sn.setSn(sn)

    def getSerialNumber(self):
        return self.sn.getSn()

    def setNumber(self,number):
        self.sn.setNumber(number)

    def getNumber(self):
        self.sn.getNumber()

    def setResult(self,result):
        self.sn.setResult(result)

    def getResult(self):
        self.sn.getResult()

    def getResult2(self):
        self.sn.getResult2()

    def setCounter(self,bl):
        assert isinstance(bl,bool)
        if bl:
            self.ct.start()
        else:
            self.ct.stop()

    def isChecked(self):
        return self.sn.isChecked()

    def setCheckBox(self,bl):
        self.sn.setCheckBox(bl)



class SerialNumberModule(QFrame):

    REPEAT = -1
    ILLEGAL = -2
    OK = 1
    INDEX = 0
    START_FLAG = True
    MLBSNS = list()
    def __init__(self,parent=None,uut=1):
        super(SerialNumberModule,self).__init__(parent)
        self.setMinimumHeight(250)
        mainlayout = QVBoxLayout()
        mainlayout.setContentsMargins(0,0,0,0)
        mainlayout.setSpacing(5)
        self.sndict = dict()
        self._num = uut
        self._e_travelers = dict()
        for item in range(int(self._num)):
            self.sndict.setdefault(item,self.createOneSn(item+1))
            mainlayout.addWidget(self.sndict.get(item))
        spacerItem = QSpacerItem(15, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)
        mainlayout.addItem(spacerItem)
        self.setLayout(mainlayout)
        #for key,value in self.sndict.iteritems():
        #        value.sn.sig.connect(self.clickCheckBox)
        self.all = 2
        self.clickCheckBox()

        self.dictResult = {}
        for item in range(int(self._num)):
            self.dictResult.setdefault(item,"NORMAL")

        self.nReTestFlag = 0
    def InitInfos(self):
        if self.nReTestFlag ==0:
            for key,value in self.sndict.iteritems():
                value.setSerialNumber("")
                value.setResult(NORMAL)
            self.nReTestFlag = 1
        
    def getSnList(self):
        num = 0
        MLBSNS = []
        for key,value in self.sndict.iteritems():
            if value.isChecked():
                MLBSNS.append(value.getSerialNumber())
            else:
                MLBSNS.append(None)

        return MLBSNS
    def getResultList(self):
        num = 0
        Resultslist = []
        for key,value in self.sndict.iteritems():
            if value.isChecked():
                Resultslist.append(self.dictResult[key])
            else:
                Resultslist.append(None)

        return Resultslist

    def createOneSn(self,num):
        return SerialNumber2(num=num)


    def checkSn(self):
        for key,value in self.sndict.items():
            if value.isChecked():
                sn = value.getSerialNumber()
                if sn =="" or len(sn)!=17:
                    return self.ILLEGAL
        dt = self.sndict
        for key,value in dt.items():
            sn = value.getSerialNumber()
            dt.pop(key)

            for k1,v1 in dt.items():
                if v1.isChecked():
                    if sn == v1.getSerialNumber():
                        return self.REPEAT
                else:
                    continue
            dt.setdefault(key,value)
        return self.OK

    def getMLBSN(self,times = 1,Scansn=False):
        if self.START_FLAG:
            self._e_travelers.clear()
            MLBSN=list()
            if Scansn:
                if self.checkSn() == self.OK:
                    with open('/vault/sn.txt', 'w') as f:
                        for key,value in self.sndict.items():
                            if value.isChecked():
                                f.writelines(str(key)+ ':' + value.getSerialNumber() + '\n')
                                MLBSN.append({"SN":value.getSerialNumber(),"uutNum":key})
                    self._e_travelers.setdefault("uutinfo",MLBSN)
                    self._e_travelers.setdefault("times",times)
                    print self._e_travelers
                    self.START_FLAG = False
                    return self._e_travelers
                else:
                    print self._e_travelers
                    return None
            else:
                for key, value in self.sndict.items():
                    if value.isChecked():
                        MLBSN.append({"SN": None, "uutNum": key})
                self._e_travelers.setdefault("uutinfo", MLBSN)
                self._e_travelers.setdefault("times", times)
                return self._e_travelers
        else:
            return False

    def clearAllSN(self):
        for key,value in self.sndict.items():
            value.setDefaultSn()


    def scanSn(self,sn):
        #if self.sndict[self.INDEX].isChecked():
        total = self.all
        print "scanSn ",self.MLBSNS,self.INDEX,self.all
        self.sndict[self.MLBSNS[self.INDEX]].setSerialNumber(sn)
        self.sndict[self.MLBSNS[self.INDEX]].setResult(TESTING)
        self.INDEX += 1        
        if self.INDEX == total:
            self.INDEX = 0
            self.START_FLAG = True
            print self.START_FLAG
            #return True

    def SetSlotResult(self,nSlotIndex,result):
        if nSlotIndex in self.dictResult.keys():
             self.dictResult[nSlotIndex] = result

    def setResult(self,name,result):
        assert isinstance(name, int)
        index = name - zmqports.SEQUENCER_PUB
        self.sndict.get(index).setResult(result)
    def getStatus(self,col):
        index = col - 5
        return self.sndict.get(index).getTestStatus()
    def getCheckStatus(self,col):
        index = col - 5
        return self.sndict.get(index).isChecked()

    def getNumber(self):
        num = 0
        self.MLBSNS = []
        for key,value in self.sndict.iteritems():
               if value.isChecked():
                self.MLBSNS.append(num)
                print "is checked ",num
                num += 1
        return num

    def setSerialNumberByUut(self,num,sn):
        self.sndict.get(int(num)).setSerialNumber(str(sn))


    def getAllFinishStatus(self):
        bFinishAll = True
        for i in self.sndict.values():
            if i.getTestStatus():
                bFinishAll = False
                break
        if bFinishAll:
            self.nReTestFlag = 0
        return bFinishAll

    def start(self,name):
        assert isinstance(name, int)
        index = name - zmqports.SEQUENCER_PUB
        self.sndict.get(index).setCounter(True)


    def stop(self,name):
        assert isinstance(name, int)
        index = name - zmqports.SEQUENCER_PUB
        self.sndict.get(index).setCounter(False)

    def setCheckBox(self,bl):
        assert isinstance(bl, bool)
        for key,value in self.sndict.iteritems():
            value.setCheckBox(bl)

    def clickCheckBox(self):
        self.MLBSNS = []
        #print len(self.sndict)
        # for key,value in self.sndict.iteritems():
        #     if value.isChecked():
        #         self.MLBSNS.append(key)

        listCheckKey =filter(lambda  x:x[1].isChecked(),self.sndict.iteritems())
        map(lambda x:self.MLBSNS.append(x[0]),listCheckKey)
        self.all = len(self.MLBSNS)
        #print self.MLBSNS,self.all


















#
#
#


# import sys
# if __name__=='__main__':
#     app = QApplication(sys.argv)
#     sn = SerialNumberModule(uut=2)
#     sn.scanSn("asdasdasd")

#     # sn.setStatues("READY")
#     # sn.setUUtNumber(6)
#     sn.show()
#     sys.exit(app.exec_())
