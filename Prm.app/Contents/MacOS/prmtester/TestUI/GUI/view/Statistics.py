# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget,QLabel,QBoxLayout,QApplication,QGroupBox,QTableWidget,\
    QVBoxLayout,QTableWidgetItem,QPushButton,QAbstractItemView
from PyQt5.QtCore import Qt,QSize,QObject,QTimer,QModelIndex,pyqtSignal
from PyQt5.QtGui import QFont
import time

#设置字体
NORMAL_FONT = QFont("Timers", 14)

BOLD_FONT = QFont("Timers", 14,QFont.Bold)

#设置字体颜色
FONT_RED = "color: rgb(252, 1, 7);"
FONT_GREEN = "color: rgb(33, 255, 6);"
FONT_BLUE = "color: rgb(0, 0, 255);"



class Labell2(QWidget):
    def __init__(self,parent = None,position = "RIGHT"):

        super(Labell2,self).__init__(parent)
        self.name = QLabel()
        self.name.setFont(NORMAL_FONT)
        self.value = QLabel()
        self.value.setFont(BOLD_FONT)
        self.name.setBuddy(self.value)
        layout = QBoxLayout(QBoxLayout.LeftToRight if position == "LEFT" else QBoxLayout.TopToBottom)
        #layout.setStretch(1,2)
        layout.setSpacing(10)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.name,1)
        layout.addWidget(self.value,1)
        self.setLayout(layout)

    def setName(self,name):
        self.name.setText(str(name))

    def setValue(self,value):
        self.value.setText(str(value))

    def setFontColor(self,color):
        try:
            self.name.setStyleSheet(color)
            self.value.setStyleSheet(color)
        except Exception as e:
            raise e




class StatisticsBox(QGroupBox):

    ROW = 3
    COLUMN = 2
    FAILCOUNT = 0
    PASSCOUNT = 0
    sig = pyqtSignal()
    def __init__(self,parent=None):
        super(StatisticsBox,self).__init__(parent)
        self.setTitle("Statistics")
        self.setMinimumHeight(150)
        mainlayout = QVBoxLayout()
        self.tb = QTableWidget(self.ROW,self.COLUMN)
        self.tb.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tb.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tb.horizontalHeader().setStretchLastSection(True)
        self.tb.setVerticalHeaderLabels(["Pass","Fail","Total"])
        self.tb.verticalHeader().setStretchLastSection(True)
        self.tb.setHorizontalHeaderLabels(["Times", "Rate"])
        self.bt = QPushButton("Clear")
        self.tb.setCellWidget(2,1,self.bt)
        self.bt.setStyleSheet("QPushButton{margin:3px};")
        self.bt.clicked.connect(self.clearAll)

        mainlayout.addWidget(self.tb)
        mainlayout.setContentsMargins(0,0,0,0)
        self.setLayout(mainlayout)
        self.initTable()


    def initTable(self):
        self.tb.setMaximumSize(300,90)
        item = QTableWidgetItem("0")
        self.tb.setItem(0,0,item)

        item = QTableWidgetItem("0")
        self.tb.setItem(1, 0, item)

        item = QTableWidgetItem("0")
        self.tb.setItem(2, 0, item)

        wd = self.tb.width()
        hg = self.tb.height()
        for item in range(self.COLUMN):
            self.tb.setColumnWidth(item,wd/3)

        for item in range(self.ROW):
            self.tb.setRowHeight(item,hg/4)
        self.clearTable()


    def clearTable(self):
        self.PASSCOUNT = 0
        self.FAILCOUNT = 0
        self.setPassValue(0)
        self.setFailValue(0)
        pItem = QTableWidgetItem("0%")
        pItem.setTextAlignment(Qt.AlignCenter)
        pItem.setForeground(Qt.darkGreen)

        self.tb.setItem(0,1,pItem)
        pItem = QTableWidgetItem("0%")
        pItem.setTextAlignment(Qt.AlignCenter)
        pItem.setForeground(Qt.red)
        self.tb.setItem(1, 1,pItem)



    def setPassValue(self,value):
        try:
            zItem = QTableWidgetItem(str(value))
            zItem.setTextAlignment(Qt.AlignCenter)
            zItem.setForeground(Qt.darkGreen)
            self.tb.setItem(0, 0, zItem)
            fv = self.getFailValue()
            self.setTotalValue(int(fv)+int(value))
        except Exception as e:
            raise e
        self.__calPersent()



    def getPassValue(self):
        try:
            return self.tb.item(0,0).text()
        except Exception as e:
            self.setPassValue(0)
            return self.tb.item(0,0).text()

    def setFailValue(self,value):
        try:
            zItem = QTableWidgetItem(str(value))
            zItem.setTextAlignment(Qt.AlignCenter)
            zItem.setForeground(Qt.red)
            self.tb.setItem(1, 0, zItem)
            pv = self.getPassValue()
            self.setTotalValue(int(pv) + int(value))
        except Exception as e:
            raise e
        self.__calPersent()

    def getFailValue(self):
        try:
            return self.tb.item(1, 0).text()
        except Exception as e:
            self.setFailValue(0)
            return self.tb.item(1,0).text()

    def setTotalValue(self,value):
        try:
            zItem = QTableWidgetItem(str(value))
            zItem.setTextAlignment(Qt.AlignCenter)
            zItem.setForeground(Qt.black)
            self.tb.setItem(2, 0, zItem)
        except Exception as e:
            raise e

    def getTotalValue(self):
        try:
            return self.tb.item(2,0).text()
        except Exception as e:
            self.setTotalValue(0)
            return self.tb.item(2,0).text()

    def __calPersent(self):
        try:
            total = int(self.getTotalValue())
        except Exception as e:
            raise e
        if total==0:
            pp = QTableWidgetItem("0%")
            pp.setTextAlignment(Qt.AlignCenter)
            pp.setForeground(Qt.darkGreen)
            self.tb.setItem(0,1,pp)
            fp = QTableWidgetItem("0%")
            fp.setTextAlignment(Qt.AlignCenter)
            fp.setForeground(Qt.red)
            self.tb.setItem(1,1,fp)
        else:
            try:
                ptimes = float(self.getPassValue())
                pp = ptimes/total
                p = QTableWidgetItem("{}%".format(str(pp*100)))
                p.setTextAlignment(Qt.AlignCenter)
                p.setForeground(Qt.darkGreen)
                self.tb.setItem(0, 1, p)
                fp = (1 - pp)*100
                f = QTableWidgetItem("{}%".format(str(fp)))
                f.setTextAlignment(Qt.AlignCenter)
                f.setForeground(Qt.red)
                self.tb.setItem(1,1,f)
            except Exception as e:
                raise e

    def resultPass(self):
        self.PASSCOUNT += 1
        self.setPassValue(self.PASSCOUNT)

    def resultFail(self):
        self.FAILCOUNT += 1
        self.setFailValue(self.FAILCOUNT)

    def clearAll(self):
        self.clearTable()













import sys
if __name__=='__main__':
    app = QApplication(sys.argv)
    sn = StatisticsBox()
    sn.setPassValue(2)
    sn.setFailValue(3)

    sn.show()
    sys.exit(app.exec_())
