from TestUI.GUI.view.SetPwd import Ui_Dialog
from PyQt5.QtWidgets import QApplication,QDialog,QDesktopWidget,QMessageBox
from Common.Processmanagement import PasswordManagement
from PyQt5 import QtCore
import sys

class SetPwd(QDialog,Ui_Dialog):

    def __init__(self,parent = None,UpdateUI=None,DeleteUI=None):
        super(SetPwd,self).__init__(parent=None)
        self.UpdateUI=UpdateUI
        self.par = parent
        self.DeleteUI = DeleteUI
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.ok_button)
        self.pt = PasswordManagement()
        self.setFixedSize(self.width(), self.height())
        self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def ok_button(self):
        text1 = self.sp.text()
        text2 = self.spa.text()
        if len(text1) == 0 or len(text2)==0:
            QMessageBox.warning(self, "Warnig!", "Password is Empty!")
        elif len(text1) < 6 or len(text2)<6:
            QMessageBox.warning(self, "Warning", "Password need more than 6!")
        elif text1!=text2:
            QMessageBox.warning(self, "Warning", "Please enter the same password")
        else:
            self.pt.setSppassword(text1)
            self.DeleteUI(4)
            self.done(1)




if __name__=='__main__':
    app = QApplication(sys.argv)
    labelDemo = SetPwd()
    labelDemo.show()
    sys.exit(app.exec_())
