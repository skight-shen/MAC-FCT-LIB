#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from ThirdParty.LibCallPy import *

for osPath in ['/Users/prmeasure/python-sequencer','/Users/gdlocal/Public/PRMeasurement/prmtester', '/Library/TestSW/python-sequencer',"/Library/Python/2.7/site-packages"]:
    if os.path.isdir(osPath):
        os.putenv("PYTHONPATH", osPath)


sys.path.append(os.getcwd())
sys.path.append("./Core")


import zmq
import argparse
import traceback
import logging
from logging.handlers import RotatingFileHandler
from TestEngine.Driver.Methods import Command



if not __package__:
    path = os.path.join(os.path.dirname(__file__), os.pardir)
    sys.path.insert(0, path)

from Common import zmqports
from Common.publisher import ZmqPublisher
from Common.tinyrpc.dispatch import RPCDispatcher, public
from Common.tinyrpc.server import RPCServer
from Common.tinyrpc.protocols.terpc import TERPCProtocol
from Common.tinyrpc.protocols.jsonrpc import *
from Common.tinyrpc.transports.zmq import ZmqServerTransport

from TestEngine.Driver.Functions.Calibration import Calibration
from TestEngine.Driver import Devices

VERSION = "%s %s" % ("0.0.1", "updated on 2018-02-01")
import inspect
from Common.BBase import *

class TestEngine(RPCDispatcher):
    def __init__(self, publisher, args):
        super(TestEngine, self).__init__()
        self.g_lock = args["lock"]
        self.dispatcher = RPCDispatcher()

        self.objNano= args["nano"]
        self.objSdev= args["sdev"]
        self.objPws = args["psw"]

        self.publisher = publisher

        self.DriverObj = None

        self.objEngineLog= LogClient(args["uut"],"Engine.log")#cBruceLogs("/vault/PRM_log/Dut{}_Engine.txt".format(args["uut"]))
        self.objFuncConfig =cBruceConfig("./Config/FunctionTable.json")
        self.dictFunctionTable = self.objFuncConfig.GetDict()

    def getModuleName(self, uut_num, publisher):
        if self.DriverObj==None:
            self.DriverObj =Devices.DriverObjs(uut_num, publisher, self.g_lock, self.objNano, self.objSdev,self.objPws)
        return self.DriverObj.getDeviceList()

    def register_modules_public_methods(self, uut_num, publisher):

        modules = self.getModuleName(uut_num, publisher)
        if modules:
            for moduleName in modules:
                self.dispatcher.register_instance(modules[moduleName], moduleName + ".")
            self.add_subdispatch(self.dispatcher,"")
    def _dispatch(self, request):
        Ret=request.respond("--FAIL-- Didn't Run")
        try:
            self.objEngineLog.Trace("<<<<<<<< Engine Start Request:{}".format(request))
            method=None
            result=None
            try:
                if request.method.startswith("start_test") or request.method.startswith(
                        "end_test") or request.method.startswith("_my_rpc_server_is_ready"):
                    request.method = "callback" + "." + request.method
                else:
                    strAcMethod =self.dictFunctionTable.get(request.method)
                    if strAcMethod!=None:
                        request.method = strAcMethod


                method = self.get_method(request.method)
            except JSONRPCMethodNotFoundError as e:
                return request.error_respond(e)

            Timer=cBruceTime()
            Timer.Start()
            self.objEngineLog.Trace("Engine Start Call  Func :{}".format(method))
            if method:
                try:

                    result = method(*request.args, **request.kwargs)


                    self.objEngineLog.Trace("Engine Func Result:{}".format(result))
                except Exception as e:
                    # an error occured within the method, return it
                    self.objEngineLog.Trace("Engine Func Result Except:{}".format(e))
                    Ret= request.error_respond(e)

                # respond with result

                self.objEngineLog.Trace("Engine Return Result:{}".format(result))

                Ret= request.respond(result)
            else:
                self.objEngineLog.Trace("Engine Func Get Fail:{}".format(method))
        except Exception as e:

            Ret= request.error_respond(JSONRPCServerError(e.message + os.linesep + traceback.format_exc()))
            self.objEngineLog.Trace("Engine Return Result:{}".format(Ret))
        self.objEngineLog.Trace(">>>>>>>> Engine End Request:{} Time:{}".format(Ret,Timer.Stop_n()))
        return Ret

import threading
class TestEngineServer(threading.Thread):
    def __init__(self, args):
        super(TestEngineServer, self).__init__()


        ctx = zmq.Context()
        pubAddr = "tcp://*:" + str(int(zmqports.TEST_ENGINE_PUB) + int(args["uut"]))
        print("pub_addr: %s" % pubAddr)
        self.publisher = ZmqPublisher(ctx, pubAddr, ("TestEngine_" + str(args["uut"])).encode("utf-8"))


        frontend = ctx.socket(zmq.ROUTER)
        listenAddr = "tcp://*:" + str(int(zmqports.TEST_ENGINE_PORT) +int(args["uut"]))
        frontend.bind(listenAddr)
        transport = ZmqServerTransport(frontend)
        transport.publisher = self.publisher



        self.TE = TestEngine(self.publisher, args)
        self.TE.register_modules_public_methods(int(args["uut"]), self.publisher)

        self.rpc_server = RPCServer(
            transport,
            TERPCProtocol(),
            self.TE,
        )
    def stopENgine(self):
        self.rpc_server.stopsever()

    def initLog(self, logFile):
        pass
        # logPath = os.path.dirname(logFile)
        # if not os.path.exists(logPath):
        #     os.makedirs(logPath)
        #
        # FORMAT = "%(asctime)s %(levelname)s %(filename)s %(message)s"
        #
        # logging.basicConfig(format=FORMAT, level=logging.INFO)
        #
        # Rthandler = RotatingFileHandler(logFile, maxBytes=100 * 1024 * 1024, backupCount=10)
        # Rthandler.setLevel(logging.INFO)
        # formatter = logging.Formatter(FORMAT)
        # Rthandler.setFormatter(formatter)
        # logging.getLogger().addHandler(Rthandler)

    def run(self):
        self.publisher.publish('TestEngine Starting...')
        try:
            self.rpc_server.serve_forever()
        except Exception as e:
            pass

def EngineStart(*args):
    import re
    ditcargs = {}
    listRet = re.findall(".*=(\d*)[\S]*",str(args[1]))
    if len(listRet)>=1:
        ditcargs["uut"] = listRet[0]
    ditcargs["lock"] = args[0]
    ditcargs["nano"]= args[2]
    ditcargs["sdev"] = args[3]
    server = TestEngineServer(ditcargs)

    server.run()
import time
from AynsLock.LockClient import LockClient
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='TestEngine')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s' + "'s version is " + VERSION)
    parser.add_argument('-u', '--uut', help='UUT slot number', type=int, default=0)
    parser.add_argument('-s', '--slots', help='Slots of the fixture', type=int, default=1)
    args = parser.parse_args()

    nUutId =args.uut

    objConfig = cBruceConfig("./Config/potassium.json")
    #listPotassiumUrls = objConfig.GetConfig("potassiumids")

    objEngineStartLog = LogClient(nUutId, "EngineStart.log")

    objEngineLock = LockClient("Engine","{}".format(nUutId))

    objEngineLock.Lock(True)
    objPotassiumFinder =cPotassiumIdFinder()
    PotassiumUrl = objPotassiumFinder.GetPotassiumId(nUutId + 1)
    objEngineLock.Lock(False)
    if PotassiumUrl!="":
        objNano = cNanoHippoPy(nUutId, None,PotassiumUrl)
        for i in range(0,10):
            objSDe = cSocketDev(nUutId)
            if objSDe.bConnectFlag==True:
                objpsw = None  # cPwrSq(nUutId)
                ditcargs = {}
                ditcargs["uut"] = nUutId
                ditcargs["lock"] = None

                ditcargs["nano"] = objNano
                ditcargs["sdev"] = objSDe
                ditcargs["psw"] = objpsw

                objEngineStartLog.Trace("Test Engine {} Start With PotassiumUrl {}".format(ditcargs,PotassiumUrl))

                server = TestEngineServer(ditcargs)

                server.run()
            else:
                del objSDe
                time.sleep(2)
        objEngineStartLog.Trace("TestEngine{} End Check Can't connect with 7603".format(nUutId))
    else:
        objEngineStartLog.Trace("TestEngine{} Didn't Find Potassium ERROR".format(nUutId))


