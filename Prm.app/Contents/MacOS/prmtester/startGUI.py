from PyQt5.QtWidgets import QApplication
import os
import sys
import signal
import subprocess
from Common.BBase import *
from  threading import Thread

for osPath in ['/Users/gdlocal/Public/PRMeasurement/python-sequencer','/Users/prmeasure/python-sequencer', '/Library/TestSW/python-sequencer']:
    if os.path.isdir(osPath):
        os.putenv("PYTHONPATH", osPath)

from TestUI.GUI.controller.guiManager import GuiManager


class MainApp(QApplication):
    def __init__(self):
        super(MainApp, self).__init__(sys.argv)
        self.manager = GuiManager(self.UpdateUI, self.DeleteUI)
        self.mainf = self.manager.GetFrame(0)
        self.mainf.show()
    def UpdateUI(self, tp):
        self.frame = self.manager.GetFrame(tp)
        self.frame.show()
    def DeleteUI(self, tp):
        self.manager.DeleateFrame(tp)

def main():
    app = MainApp()
    sys.exit(app.exec_())

class StartEngine(Thread):
    def __init__(self):
        super(StartEngine, self).__init__()
        self.objShell = cShell()

    def run(self):
        self.objShell.RunShell_n("sh ./StartEngine.sh")

if __name__ == '__main__':

    import sys
    sys.path.append(os.path.abspath("./Core"))
    import CoreAPI

    CoreAPI.CleanPlatform()
    

    Engine=StartEngine()
    Engine.start()
    print "Shell Finish !"
    main()
