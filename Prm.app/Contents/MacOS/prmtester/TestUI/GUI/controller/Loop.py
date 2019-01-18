from TestUI.GUI.view.Loop import Ui_LoopTest
from PyQt5.QtWidgets import QApplication, QDialog, QDesktopWidget, QMessageBox
from Common.tinyrpc.protocols.StateMachineRpc import StateMachineRPCProtocol

import sys
from PyQt5.QtCore import QThread
import time
import PyQt5.QtCore
from PyQt5 import QtCore,QtGui


from Common.BBase import  *

class LoopTest(QThread):

    def __init__(self, sm, show, mg,nFrequence=20):
        super(LoopTest, self).__init__()
        self.sm = sm
        self.show = show
        self.mg = mg
        self.count = 1
        self.nFrequence = nFrequence
        self.e_travels = None
        self.running = True

        self.LogLocal = cLocalLogs("/vault/Loop.txt")

    def run(self):
        assert isinstance(self.count, int)
        for i in range(self.count):

            self.LogLocal.Trace("Loop {} Start".format(self.count))
            if not self.running:
                self.LogLocal.Trace("1 Runing:{} Break Loop".format(self.running))
                break

            self.LogLocal.Trace("Loop Send Start Message To StateMachine Start >>")
            req = StateMachineRPCProtocol()
            t = req.create_request('start', self.e_travels)
            strRet= self.sm.client.transport.send_reply(t.serialize())
            self.show.display(i+1)
            self.LogLocal.Trace("Loop Send Start Message In While Wait For Finish >> {}".format(strRet))
            # time.sleep(3)
            while self.running:

                #self.LogLocal.Trace("Check For Finish {} {}".format(self.mg.sn.getAllFinishStatus()))
                #if self.mg.sn.getAllFinishStatus():
                #    self.mg.mg.set_all_start(False)
                #    self.LogLocal.Trace("Break While Finish >>")
                #    break
                self.LogLocal.Trace("Check For Finish {} {}".format(self.mg.mg.get_status() ,self.mg.mg.get_start()))
                if self.mg.mg.get_status() and self.mg.mg.get_start():
                    self.mg.mg.set_all_start(False)
                    self.LogLocal.Trace("Break While Finish >>")
                    break
                time.sleep(1)
            if not self.running:
                self.LogLocal.Trace("2 Runing:{} Break Loop".format(self.running))
                break
            self.LogLocal.Trace("Sleep {} Start".format(self.nFrequence))
            time.sleep(self.nFrequence)
            self.LogLocal.Trace("Sleep {} Finish".format(self.nFrequence))


class Loop_Frame(QDialog, Ui_LoopTest):

    def __init__(self, parent=None, UpdateUI=None, DeleteUI=None, sm_remote=None):
        super(Loop_Frame, self).__init__(parent=None)
        self.setWindowFlags(PyQt5.QtCore.Qt.WindowStaysOnTopHint)
        self.par = parent
        self.UpdateUI = UpdateUI
        self.DeleteUI = DeleteUI
        self.setupUi(self)

        reNumber = QtCore.QRegExp("[0-9]+")
        self.total.setValidator(QtGui.QRegExpValidator(reNumber, self))
        self.frequence.setValidator(QtGui.QRegExpValidator(reNumber, self))


        self.total.setText("100")
        self.frequence.setText("20")
        self.loop_in.clicked.connect(self.loopIn)
        self.loop_out.clicked.connect(self.loopOut)
        self.loopThread = LoopTest(sm_remote, self.remain, self.par,nFrequence =int(self.frequence.text()))
        self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def loopIn(self):
        e_travelers = self.par.sn.getMLBSN()
        if not e_travelers:
            return
        try:
            total = int(self.total.text())
        except ValueError:
            QMessageBox.warning(self, "Warnig!", "ValueError!")
            return None
        time = total

        self.loopThread.nFrequence = int(self.frequence.text())

        self.loopThread.e_travels = e_travelers
        self.loopThread.running = True
        self.loopThread.count = time
        self.loopThread.start()



    def loopOut(self):
        self.loopThread.running = False

    def stoploop(self):
        pass
        #self.loopThread.running = False

    def closeEvent(self, QCloseEvent):
        self.remain.display(0)
        self.par.loop = False


    def showEvent(self, QShowEvent):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    labelDemo = Loop_Frame()
    labelDemo.show()
    sys.exit(app.exec_())
