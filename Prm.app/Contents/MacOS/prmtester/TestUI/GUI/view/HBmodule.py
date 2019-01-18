# -*- coding: utf-8 -*-
"""
fractionsliderPyside.py
Annotated PySide port of fractionslider.py from Chapter 11
of Mark Summerfield's 'Rapid GUI Programming with Python and Qt' (2008)
Book's web site: http://www.qtrac.eu/pyqtbook.html

Notes on translation:
 segColor = QtGui.QColor(QtCore.Qt.green).dark(120)--> darker
------
This script is part of the PySideSummer repository at GitHub:
https://github.com/EricThomson/PySideSummer
Code is under the GPL license: http://www.gnu.org/copyleft/gpl.html
"""
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt,QRect,QSize,QTimer
from PyQt5.QtGui import QPainter,QFont,QColor,QBrush,QPalette,QLinearGradient,QFontMetrics
import sys



class HeartBeate(QLabel):

    time = 0
    def __init__(self,num=2,ft="Microsoft YaHei"):
        super(HeartBeate,self).__init__()
        #self.resize(100,20)
        self.ft = ft
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.changeColor)
        self.timer.start(1000)
        self._text = "Sequencer:"
        self.lenth = num
        self.clor = (QPalette().window(),Qt.blue)
        self.fc = list()
        self._status = list()
        self.initStatus()
        self.setFixedWidth(40* self.lenth + len(self._text)*5)
        #self.setMinimumWidth(250)


    def initStatus(self):
        self._status = [False for i in range(self.lenth)]
        self.fc = [QPalette().window() for i in range(self.lenth)]

    def clearStatus(self):
        self._status = [False for i in range(self.lenth)]



    def setText(self,text):
        self._text = text

    def getText(self):
        return self._text

    def setStatus(self,index,status):
        if index<0 or index> self.lenth-1:
            print "out of index"
            return None
        else:
            try:
                self._status[index] = status
            except Exception as e:
                raise e
                return False
            return True

    def getStatus(self,index):
        if index < 0 or index > self.lenth - 1:
            print "out of index"
            return None
        else:
            return self._status[index]




    def changeColor(self):
        if self.time == 0:
            for i in range(self.lenth):
                if self._status[i] == False:
                    self.fc[i] = self.clor[0]
                elif self._status[i] == True:
                    self.fc[i] = self.clor[1]
            self.clearStatus()
        elif self.time == 1:
            self.fc = [QPalette().window() for i in range(self.lenth)]
        self.time += 1
        self.update()
        if self.time == 2:
            self.time = 0
            #self.clearStatus()




    def paintEvent(self, QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()


    def drawPoints(self,qp):
        size = self.size()

        #字体大小
        font = QFont(self.ft,14,QFont.Bold)
        qp.setFont(font)
        fm = QFontMetrics(font)
        wd = fm.width(self._text)
        hg = fm.height()
        textrect = QRect(0,0,wd+10,size.height())
        qp.setPen(Qt.black)
        qp.drawText(textrect, Qt.AlignCenter, self._text)

        space = 10

        #c = QPalette().window()
        #方块大小
        if self._status:
            for i in range(self.lenth):
                f = QRect(wd+space,size.height()/2-10,20,20)

                qp.setPen(Qt.NoPen)
                qp.setBrush(self.fc[i])
                qp.drawRect(f)
                font = QFont(self.ft, 14, QFont.Bold)
                qp.setFont(font)
                qp.setPen(Qt.white)
                qp.drawText(f, Qt.AlignCenter, str(i+1))


                space += 30
        else:
            for i in range(self.lenth):
                f = QRect(wd+space,size.height()/2-10,20,20)

                qp.setPen(Qt.NoPen)
                qp.setBrush(self.clor[0])
                qp.drawRect(f)

                font = QFont(self.ft, 14, QFont.Bold)
                qp.setFont(font)
                qp.setPen(Qt.white)
                qp.drawText(f, Qt.AlignCenter, str(i+1))

                space += 30


class HBModule(QFrame):
    def __init__(self,parent = None,num = 2):
        super(HBModule,self).__init__(parent)
        mainlayout = QHBoxLayout()
        self._num = num
        self.seq = self.getOneHB(self._num,"Sequencer:")
        self.eng = self.getOneHB(self._num,"Engine:")
        self.logg = self.getOneHB(1,"Logger:")
        self.pdcalable = QLabel("PDCA:")
        ft = QFont("Microsoft YaHei", 14, QFont.Bold)
        self.pdcalable.setFont(ft)
        self.pdca = QLabel()

        self.pdca.setFixedSize(20, 20)
        self.pdca.setAlignment(QtCore.Qt.AlignCenter)





        self.dictFans = {}
        self.dictFans["fans"]  = self.getOneHB(4, "Fans:")
        self.dictFans["fansR"] = self.getOneHB(4, "FansR:")
        self.dictFans["fansL"] = self.getOneHB(4, "FansL:")
        self.dictFans["fansB"] = self.getOneHB(2, "FansB:")
        mainlayout.addWidget(self.seq)
        mainlayout.addWidget(self.eng)
        mainlayout.addWidget(self.logg)
        mainlayout.addWidget(self.pdcalable)
        mainlayout.addWidget(self.pdca)

        mainlayout.addWidget(self.dictFans["fans"])

        mainlayout.addWidget(self.dictFans["fansL"])
        mainlayout.addWidget(self.dictFans["fansR"])
        mainlayout.addWidget(self.dictFans["fansB"])










        mainlayout.setContentsMargins(0,0,0,0)
        self.setLayout(mainlayout)

    def getOneHB(self,num,name):
        b = HeartBeate(num)
        b.setText(name)
        return b

    def setPdca(self,bl):
        assert isinstance(bl,bool)
        if bl:
            self.pdca.setText("T")
            self.pdca.setStyleSheet("background-color: rgb(15, 128, 255);")
        else:
            self.pdca.setText("F")
            self.pdca.setStyleSheet("background-color: rgb(252, 1, 7);")

    def SetFansStatus(self,strKey,nIndex,nResult):
        self.dictFans[strKey].setStatus(nIndex,nResult)
    def setHartBeat(self,name):
        if 0<=int(name)-6250<=3:
            self.seq.setStatus(int(name)-6250,True)
        elif 0<=int(name)-6150<=3:
            self.eng.setStatus(int(name)-6150,True)
        elif int(name)-6900==0:
            self.logg.setStatus(0,True)





if __name__=='__main__':
    app = QApplication(sys.argv)
    hb = HeartBeate()

    hb.show()
    sys.exit(app.exec_())



