# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(975, 706)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(343, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(538, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 0, 1, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.group_slotinfo = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.group_slotinfo.sizePolicy().hasHeightForWidth())
        self.group_slotinfo.setSizePolicy(sizePolicy)
        self.group_slotinfo.setObjectName("group_slotinfo")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.group_slotinfo)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_slot3 = QtWidgets.QLabel(self.group_slotinfo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_slot3.sizePolicy().hasHeightForWidth())
        self.label_slot3.setSizePolicy(sizePolicy)
        self.label_slot3.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_slot3.setObjectName("label_slot3")
        self.gridLayout_2.addWidget(self.label_slot3, 2, 0, 1, 1)
        self.label_slot4 = QtWidgets.QLabel(self.group_slotinfo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_slot4.sizePolicy().hasHeightForWidth())
        self.label_slot4.setSizePolicy(sizePolicy)
        self.label_slot4.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_slot4.setObjectName("label_slot4")
        self.gridLayout_2.addWidget(self.label_slot4, 3, 0, 1, 1)
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.group_slotinfo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser_4.sizePolicy().hasHeightForWidth())
        self.textBrowser_4.setSizePolicy(sizePolicy)
        self.textBrowser_4.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.gridLayout_2.addWidget(self.textBrowser_4, 3, 1, 1, 1)
        self.label_slot1 = QtWidgets.QLabel(self.group_slotinfo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_slot1.sizePolicy().hasHeightForWidth())
        self.label_slot1.setSizePolicy(sizePolicy)
        self.label_slot1.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_slot1.setObjectName("label_slot1")
        self.gridLayout_2.addWidget(self.label_slot1, 0, 0, 1, 1)
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.group_slotinfo)
        self.textBrowser_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.gridLayout_2.addWidget(self.textBrowser_2, 1, 1, 1, 1)
        self.label_slot2 = QtWidgets.QLabel(self.group_slotinfo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_slot2.sizePolicy().hasHeightForWidth())
        self.label_slot2.setSizePolicy(sizePolicy)
        self.label_slot2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_slot2.setObjectName("label_slot2")
        self.gridLayout_2.addWidget(self.label_slot2, 1, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self.group_slotinfo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_2.addWidget(self.textBrowser, 0, 1, 1, 1)
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.group_slotinfo)
        self.textBrowser_3.setMinimumSize(QtCore.QSize(0, 0))
        self.textBrowser_3.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.gridLayout_2.addWidget(self.textBrowser_3, 2, 1, 1, 1)
        self.gridLayout_3.addWidget(self.group_slotinfo, 0, 0, 1, 3)
        self.bt_abort = QtWidgets.QPushButton(self.centralwidget)
        self.bt_abort.setObjectName("bt_abort")
        self.gridLayout_3.addWidget(self.bt_abort, 3, 1, 1, 1)
        self.bt_start = QtWidgets.QPushButton(self.centralwidget)
        self.bt_start.setObjectName("bt_start")
        self.gridLayout_3.addWidget(self.bt_start, 2, 1, 1, 1)
        self.bt_loop = QtWidgets.QPushButton(self.centralwidget)
        self.bt_loop.setObjectName("bt_loop")
        self.gridLayout_3.addWidget(self.bt_loop, 4, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 1, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 2, 2, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_testOverview = QtWidgets.QWidget()
        self.tab_testOverview.setObjectName("tab_testOverview")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_testOverview)
        self.gridLayout.setObjectName("gridLayout")
        self.tableview_test = QtWidgets.QTableView(self.tab_testOverview)
        self.tableview_test.setObjectName("tableview_test")
        self.gridLayout.addWidget(self.tableview_test, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_testOverview, "")
        self.tab_failureOverview = QtWidgets.QWidget()
        self.tab_failureOverview.setObjectName("tab_failureOverview")
        self.tableview_failure = QtWidgets.QTableView(self.tab_failureOverview)
        self.tableview_failure.setGeometry(QtCore.QRect(0, 0, 581, 581))
        self.tableview_failure.setObjectName("tableview_failure")
        self.tabWidget.addTab(self.tab_failureOverview, "")
        self.gridLayout_4.addWidget(self.tabWidget, 2, 0, 1, 2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem3, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 975, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ingenuity"))
        self.label.setText(_translate("MainWindow", "LOGO"))
        self.group_slotinfo.setTitle(_translate("MainWindow", "SN Info"))
        self.label_slot3.setText(_translate("MainWindow", "SLOT3:"))
        self.label_slot4.setText(_translate("MainWindow", "SLOT4:"))
        self.label_slot1.setText(_translate("MainWindow", "SLOT1:"))
        self.label_slot2.setText(_translate("MainWindow", "SLOT2:"))
        self.bt_abort.setText(_translate("MainWindow", "ABORT"))
        self.bt_start.setText(_translate("MainWindow", "START"))
        self.bt_loop.setText(_translate("MainWindow", "LOOP"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_testOverview), _translate("MainWindow", "Test_Overview"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_failureOverview), _translate("MainWindow", "Failure_Overview"))

