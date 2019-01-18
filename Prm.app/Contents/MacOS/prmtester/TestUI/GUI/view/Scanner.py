# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Scanner.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Scanner(object):
    def setupUi(self, Scanner):
        Scanner.setObjectName("Scanner")
        Scanner.resize(400, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Scanner)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 10, -1, 10)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Scanner)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.sn1 = QtWidgets.QLineEdit(Scanner)
        self.sn1.setObjectName("sn1")
        self.gridLayout.addWidget(self.sn1, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(Scanner)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)
        self.sn2 = QtWidgets.QLineEdit(Scanner)
        self.sn2.setObjectName("sn2")
        self.gridLayout.addWidget(self.sn2, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(Scanner)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)
        self.sn3 = QtWidgets.QLineEdit(Scanner)
        self.sn3.setObjectName("sn3")
        self.gridLayout.addWidget(self.sn3, 2, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(Scanner)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 3, 1, 1, 1)
        self.sn4 = QtWidgets.QLineEdit(Scanner)
        self.sn4.setObjectName("sn4")
        self.gridLayout.addWidget(self.sn4, 3, 2, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 7)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Scanner)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Scanner)
        self.buttonBox.accepted.connect(Scanner.accept)
        self.buttonBox.rejected.connect(Scanner.reject)
        QtCore.QMetaObject.connectSlotsByName(Scanner)

    def retranslateUi(self, Scanner):
        _translate = QtCore.QCoreApplication.translate
        Scanner.setWindowTitle(_translate("Scanner", "Scanner"))
        self.label.setText(_translate("Scanner", "MLB1："))
        self.label_2.setText(_translate("Scanner", "MLB2："))
        self.label_3.setText(_translate("Scanner", "MLB3："))
        self.label_4.setText(_translate("Scanner", "MLB4："))

