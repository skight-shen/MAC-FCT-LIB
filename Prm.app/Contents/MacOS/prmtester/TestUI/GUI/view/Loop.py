# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Loop.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoopTest(object):
    def setupUi(self, LoopTest):
        LoopTest.setObjectName("LoopTest")
        LoopTest.resize(648, 503)

        self.layoutWidget = QtWidgets.QWidget(LoopTest)
        self.layoutWidget.setGeometry(QtCore.QRect(160, 70, 312, 52))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lsn2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lsn2.setMinimumSize(QtCore.QSize(250, 40))
        self.lsn2.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lsn2.setFont(font)
        self.lsn2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lsn2.setStyleSheet("border-image: url(:/picture/sn2.png);")
        self.lsn2.setText("")
        self.lsn2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lsn2.setObjectName("lsn2")
        self.horizontalLayout_2.addWidget(self.lsn2)
        self.lresult2 = QtWidgets.QLabel(self.layoutWidget)
        self.lresult2.setMinimumSize(QtCore.QSize(40, 40))
        self.lresult2.setMaximumSize(QtCore.QSize(40, 40))
        self.lresult2.setStyleSheet("border-image: url(:/picture/idle.png);")
        self.lresult2.setText("")
        self.lresult2.setObjectName("lresult2")
        self.horizontalLayout_2.addWidget(self.lresult2)
        self.layoutWidget_2 = QtWidgets.QWidget(LoopTest)
        self.layoutWidget_2.setGeometry(QtCore.QRect(160, 120, 312, 52))
        self.layoutWidget_2.setObjectName("layoutWidget_2")


        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lsn3 = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.lsn3.setMinimumSize(QtCore.QSize(250, 40))
        self.lsn3.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lsn3.setFont(font)
        self.lsn3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lsn3.setStyleSheet("border-image: url(:/picture/sn3.png);")
        self.lsn3.setText("")
        self.lsn3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lsn3.setObjectName("lsn3")
        self.horizontalLayout_3.addWidget(self.lsn3)
        self.lsult3 = QtWidgets.QLabel(self.layoutWidget_2)
        self.lsult3.setMinimumSize(QtCore.QSize(40, 40))
        self.lsult3.setMaximumSize(QtCore.QSize(40, 40))
        self.lsult3.setStyleSheet("border-image: url(:/picture/idle.png);")
        self.lsult3.setText("")
        self.lsult3.setObjectName("lsult3")
        self.horizontalLayout_3.addWidget(self.lsult3)
        self.layoutWidget_3 = QtWidgets.QWidget(LoopTest)
        self.layoutWidget_3.setGeometry(QtCore.QRect(160, 170, 312, 52))
        self.layoutWidget_3.setObjectName("layoutWidget_3")

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lsn4 = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.lsn4.setMinimumSize(QtCore.QSize(250, 40))
        self.lsn4.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lsn4.setFont(font)
        self.lsn4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lsn4.setStyleSheet("border-image: url(:/picture/sn4.png);")
        self.lsn4.setText("")
        self.lsn4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lsn4.setObjectName("lsn4")
        self.horizontalLayout_4.addWidget(self.lsn4)
        self.lsult4 = QtWidgets.QLabel(self.layoutWidget_3)
        self.lsult4.setMinimumSize(QtCore.QSize(40, 40))
        self.lsult4.setMaximumSize(QtCore.QSize(40, 40))
        self.lsult4.setStyleSheet("border-image: url(:/picture/idle.png);")
        self.lsult4.setText("")
        self.lsult4.setObjectName("lsult4")
        self.horizontalLayout_4.addWidget(self.lsult4)
        self.total = QtWidgets.QLineEdit(LoopTest)
        self.total.setGeometry(QtCore.QRect(280, 230, 60, 31))
        self.total.setObjectName("total")
        self.label = QtWidgets.QLabel(LoopTest)
        self.label.setGeometry(QtCore.QRect(160, 240, 101, 16))

        ps = self.total.pos()



        self.frequence = QtWidgets.QLineEdit(LoopTest)
        self.frequence.setGeometry(QtCore.QRect(180, 230, 60, 31))
        self.frequence.setObjectName("frequence")

        self.label_fre = QtWidgets.QLabel(LoopTest)
        self.label_fre.setGeometry(QtCore.QRect(160, 240, 120, 31))
        self.label_fre.setText("Interval(s):")
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_fre.setFont(font)

        self.label_fre.move(ps.x()+self.total.width()+5,ps.y())
        self.frequence.move(ps.x()+self.total.width()+95,ps.y())


        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(LoopTest)
        self.label_2.setGeometry(QtCore.QRect(160, 310, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.remain = QtWidgets.QLCDNumber(LoopTest)
        self.remain.setGeometry(QtCore.QRect(280, 290, 141, 51))
        self.remain.setObjectName("remain")


        self.loop_in = QtWidgets.QPushButton(LoopTest)
        self.loop_in.setGeometry(QtCore.QRect(150, 370, 121, 51))
        self.loop_in.setFocusPolicy(QtCore.Qt.NoFocus)
        self.loop_in.setObjectName("loop_in")
        self.loop_out = QtWidgets.QPushButton(LoopTest)
        self.loop_out.setGeometry(QtCore.QRect(300, 370, 121, 51))
        self.loop_out.setFocusPolicy(QtCore.Qt.NoFocus)
        self.loop_out.setObjectName("loop_out")
        self.layoutWidget1 = QtWidgets.QWidget(LoopTest)
        self.layoutWidget1.setGeometry(QtCore.QRect(160, 20, 312, 52))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lsn1 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lsn1.setMinimumSize(QtCore.QSize(250, 40))
        self.lsn1.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lsn1.setFont(font)
        self.lsn1.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lsn1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lsn1.setStyleSheet("border-image: url(:/picture/sn1.png);")
        self.lsn1.setText("")
        self.lsn1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lsn1.setObjectName("lsn1")
        self.horizontalLayout.addWidget(self.lsn1)
        self.lresult1 = QtWidgets.QLabel(self.layoutWidget1)
        self.lresult1.setMinimumSize(QtCore.QSize(40, 40))
        self.lresult1.setMaximumSize(QtCore.QSize(40, 40))
        self.lresult1.setStyleSheet("border-image: url(:/picture/idle.png);")
        self.lresult1.setText("")
        self.lresult1.setObjectName("lresult1")
        self.horizontalLayout.addWidget(self.lresult1)

        self.retranslateUi(LoopTest)
        QtCore.QMetaObject.connectSlotsByName(LoopTest)

        self.lsn1.setVisible(False)
        self.lresult1.setVisible(False)

        self.lsn2.setVisible(False)
        self.lresult2.setVisible(False)

        self.lsn3.setVisible(False)
        self.lsult3.setVisible(False)

        self.lsn4.setVisible(False)
        self.lsult4.setVisible(False)


    def retranslateUi(self, LoopTest):
        _translate = QtCore.QCoreApplication.translate
        LoopTest.setWindowTitle(_translate("LoopTest", "Form"))
        self.label.setText(_translate("LoopTest", "LoopCount："))
        self.label_2.setText(_translate("LoopTest", "CurrentLoop："))
        self.loop_in.setText(_translate("LoopTest", "Loop IN"))
        self.loop_out.setText(_translate("LoopTest", "Loop Out"))

import appqrc_rc