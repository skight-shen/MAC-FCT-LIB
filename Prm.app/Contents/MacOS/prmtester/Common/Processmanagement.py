import json
import os
from multiprocessing import Process
from subprocess import call, Popen
import signal
import time
import sys
import re

#from TestEngine.TestEngine import *

#from BBase import *

#from ThirdParty.LibCallPy import *


pwd = os.path.dirname(__file__)
config_file = os.path.join(pwd, 'ProcessConfig.json')
f = open(config_file, 'rU')
config = json.load(f)
f.close()
for i in ['/Users/gdlocal/Public/PRMeasurement/python-sequencer', '/Library/TestSW/python-sequencer']:
    if os.path.isdir(i):
        os.putenv("PYTHONPATH",
                  i + ':/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/PyObjC')
        seqDir = i

prmDir = '/'.join(pwd.split('/')[:-1])


class ProcessManagement(object):
    def __init__(self):
        self.process = [item for item in config.get("processes")]
        self.pid = {}

        self.pdca = config.get("pdca")
        self.fixture = config.get("fixture")

        self.dictPrmLog = config.get("prmlog")
        self.dictPrmLock = config.get("prmlock")

        self.dictTestEngine={}

    def killPid(self, pid):
        try:
            a = os.kill(pid, signal.SIGKILL)
            print ('killed the {0} process and the return is {1}'.format(pid, a))
        except OSError, e:
            print ("have no {0} process".format(pid))

    def killAll(self):
        try:
            for index, value in self.pid.iteritems():
                print index, value
                self.killPid(value)
        except OSError, e:
            print OSError

    def callSingleProcess(self, *args):
        if len(args) < 2:
            p = Popen(['python', args[0]])
        # elif len(args) == 2:
        #     p = Popen(['python', args[0], args[1]])
        else:
            list_cmd = ["python"]
            for  i in args:
                if type(i)==type([]):
                    for j in i:
                        list_cmd.append(j)
                else:
                    list_cmd.append(i)
            print "Cmd : {}".format(list_cmd)
            p = Popen(list_cmd)



        return p.pid
    def BcallSingleProcess(self,*args):
        pass
    def startupAllProcess(self):
        for item in self.process:
            time.sleep(0.2)
            if item.get('args'):
                p = item.get('path')
                print "Check --->{} {}".format(prmDir,seqDir)
                try:
                    targetPath = p.format(prm=prmDir, pySeq=seqDir)
                except Exception as e:
                    print "heck -----??>>>>{}".format(e)
                    raise Exception('config error')
                path = targetPath + item.get('bin')
                print('process path is ' + path)
                para = item.get('args')

                paranew = re.split(" ",para)



                if item.get("name").find("engi")>=0:
                    self.pid[item.get('name')] = self.BcallSingleProcess(para)
                else:
                    self.pid[item.get('name')] = self.callSingleProcess(path, paranew)
            else:
                print(item)
                p = item.get('path')
                try:
                    targetPath = p.format(prm=prmDir, pySeq=seqDir)
                except:
                    raise Exception('config error')
                path = targetPath + item.get('bin')
                print(path)
                para = item.get('args')
                self.pid[item.get('name')] = self.callSingleProcess(path)


    def startPrmLogSever(self, switch=True):
        targetPath = self.dictPrmLog.get('path').format(prm=prmDir, pySeq=seqDir)
        path = targetPath + self.dictPrmLog.get('bin')

        self.pid['prmlog'] = self.callSingleProcess(path)

    def startPrmLockSever(self, switch=True):
        targetPath = self.dictPrmLock.get('path').format(prm=prmDir, pySeq=seqDir)
        path = targetPath + self.dictPrmLock.get('bin')

        self.pid['prmlock'] = self.callSingleProcess(path)

    def startPdcaSever(self, switch=True):
        if self.pid.get('pdca'):
            self.killPid(self.pid.get('pdca'))
        targetPath = self.pdca.get('path').format(prm=prmDir, pySeq=seqDir)
        path = targetPath + self.pdca.get('bin')
        print('pdca path is ' + path)
        if switch == False:
            self.pid['pdca'] = self.callSingleProcess(path, '-p')
        else:
            self.pid['pdca'] = self.callSingleProcess(path)

    def start_fixture_server(self, switch=False):
        if self.pid.get('fixture'):
            self.killPid(self.pid.get('fixture'))
        targetPath = self.fixture.get('path').format(prm=prmDir, pySeq=seqDir)
        path = targetPath + self.fixture.get('bin')
        print('fixture  path is ' + path)
        if switch == False:
            self.pid['fixture'] = self.callSingleProcess(path)
        else:
            self.pid['fixture'] = self.callSingleProcess(path)
    def myprintProcessID(self):
        for key, value in self.pid.iteritems():
            print value

class PasswordManagement(object):
    def __init__(self):
        self._pd = config.get("Password")
        self._op = self._pd.get("op")
        self._sp = self._pd.get("sp")

    def getOppassword(self):
        return self._op

    def getSppassword(self):
        return self._sp

    def setOppassword(self, pd):
        self._pd["op"] = pd
        config["Password"] = self._pd
        self.saveToJosn(config)

    def setSppassword(self, pd):
        self._pd["op"] = pd
        config["Password"] = self._pd
        self.saveToJosn(config)

    def saveToJosn(self, file1):
        with open(file1, "w") as f:
            json.dump(file1, f)


class Singleton(type):
    """
    This is a meta class to access singleton
    """
    __instance = None

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(Singleton, self).__call__(*args, **kwargs)
        return self.__instance


class OpenScript(object):
    __metaclass__ = Singleton

    def __init__(self):
        self._path = config.get("scriptpath")

    def getpath(self):
        return self._path

    def savepath(self, path):
        config["scriptpath"] = path
        with open(config_file, "w") as f:
            f.write(json.dumps(config, sort_keys=True, indent=4, separators=(',', ':')))
            # f.write(json.dumps(config))
