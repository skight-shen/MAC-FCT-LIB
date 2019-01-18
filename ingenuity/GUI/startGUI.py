from threading import Thread
import os, sys, time, datetime
from common.shell import Shell
from os import path

for osPath in ['/Users/admin/PycharmProjects/Repository/MAC-FCT-LIB/ingenuity','/Users/admin/PycharmProjects/Repository/MAC-FCT-LIB/python-sequencer','/Library/python-sequencer']:
    if os.path.isdir(osPath):
        #os.putenv("PYTHONPATH", osPath)
        sys.path.append(osPath)


class StartGui(object):
    def __init__(self, site=1):
        self.killalL()
        self.objShell = Shell()
        self.site = site
        self.sm = None
        self.pid ={}
        self.pwd = path.dirname(os.getcwd())
        pass

    def launchProcess(self,processName='ALL'):
        #start engine, sequencer, fixture_server, logger and statemachine
        for i in range(self.site):
            #run engine
            self.objShell.run_shell('python ../testEngine/testEngine.py -s %d'%i)
            time.sleep(1)
            self.objShell.run_shell('python %s/../python-sequencer/x527/sequencer/sequencer.py -s %d -c -f 1'%(self.pwd,i))
            time.sleep(1)

        self.objShell.run_shell('python ../fixture/FixtureServer.py')
        self.objShell.run_shell('python %s/../python-sequencer/x527/loggers/logger.py'%self.pwd)
        self.objShell.run_shell('python ../statemachine/smrpcserver.py -c %d'%self.site)

    def loadMainUI(self):
        while 1:
            pass

    def killalL(self):
        pass

if __name__ == "__main__":

    starter = StartGui()
    starter.launchProcess()
    starter.loadMainUI()