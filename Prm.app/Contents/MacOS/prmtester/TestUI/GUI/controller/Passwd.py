from TestUI.GUI.view.Password import Ui_Dialog
from PyQt5.QtWidgets import QApplication,QDialog,QDesktopWidget,QMessageBox
from PyQt5 import QtCore
from Common.Processmanagement import PasswordManagement
import sys

class EnterPwd(QDialog,Ui_Dialog):

    def __init__(self,parent = None,UpdateUI=None,DeleteUI=None):
        super(EnterPwd,self).__init__(parent=None)
        self.UpdateUI=UpdateUI
        self.DeleteUI = DeleteUI
        self.setupUi(self)
        self.par = parent
        self.setFixedSize(self.width(), self.height());
        self.lineEdit.setEchoMode(self.lineEdit.Password)
        self.buttonBox.accepted.connect(self.ok_button)
        #self.buttonBox.rejected.connect(self.cancel_button)
        self.setFixedSize(self.width(), self.height())
        self.pt = PasswordManagement()
        self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


    def ok_button(self):
        text = self.lineEdit.text()
        if len(text) == 0:
            QMessageBox.warning(self,"Warnig!","Password is Empty!")
        # elif len(text) < 6:
        #     QMessageBox.warning(self,"Warning","Password need more than 6!")
        else:
            if text == self.pt.getSppassword():
                self.par.enterIntoSpMode()
                self.DeleteUI(2)
                self.done(1)
            else:
                QMessageBox.warning(self, "Warning", "The Password was wrong!")

    def closeEvent(self, QCloseEvent):
        self.DeleteUI(2)

if __name__=='__main__':
    app = QApplication(sys.argv)
    labelDemo = EnterPwd()
    labelDemo.show()
    sys.exit(app.exec_())