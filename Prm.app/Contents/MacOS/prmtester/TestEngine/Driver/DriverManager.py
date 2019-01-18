#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'jinhui.huang'

import os
import fcntl
from Common.publisher import ZmqPublisher
import json
import time
from Common.tinyrpc.transports.zmq import ZmqServerTransport
from TestEngine.Driver.TcpDriver import TcpDriver
from TestEngine.Driver.zynqdriver import ZYNQ
from TestEngine.Driver.zynqdriver_dummy import ZYNQ_DUMMY
from TestEngine.Driver.dut import dut

from TestEngine.Driver.Functions.Callback import *

def read_json(path):
    f = open(path, 'r')
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)

    json_data = json.load(f)
    f.close()
    return json_data


class Singleton(type):
    """
    This is a meta class to access singleton
    """
    __instance = None

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(Singleton, self).__call__(*args, **kwargs)
        return self.__instance


class DriverManager(object):
    """
    DriverManager is a singleton class, it only has one instance
    -------------------------------------------------------------------
    Args :
        driverId : every board card should has unique Id to be
        identified

        driverObj : this arg must be TcpDriver or SerialDriver instance.
        and
    """
    #__metaclass__ = Singleton

    # TODO: add transport to heartbeat
    def __init__(self, uut_num=0,lock=None,nano=None,sdev=None,psw=None):
        self.g_lock = lock
        self.objNano=nano
        self.objSdev=sdev
        self.objPsw = psw

        self.bCallBack = False
        self.__driverDict = {}
        self.pub = None
        self.checkConnetion()
        self.transport = None
        self.uut = uut_num

        self.configs=None
        print "Create in DriverManager {}".format(self.uut)
    def checkheartbeat(self):
        assert isinstance(self.transport, ZmqServerTransport)
        self.transport.check_heartbeat()
    def load_config(self):
        config_file = '/'.join(__file__.split('/')[:-2]) + '/DriverConfig.json'
        print("driver config locate at: %s" % config_file)
        # load driver configs
        f = open(config_file, 'r')
        configs = json.load(f)
        f.close()
        return configs
    def CreateZynqDrivers(self):
        if self.configs==None:
            self.configs = self.load_config()
        listZynqs=[]
        for i in range(0,len(self.configs)):
            cfg=self.configs.get("uut{}".format(i)).get("ZYNQ")
            listZynqs.append(ZYNQ_DUMMY(cfg, publisher=self.pub, uut=i, psw=None))
        return listZynqs

    def log(self, msg):
        # assert isinstance(self.pub, ZmqPublisher)
        self.pub.publish(msg)

    def loadConfig(self, cfgs):
        """
        load drivers config
        recommand to use this method to start driver
        ---------------------------------------------
        Args:
            cfg(dict):
                contain drivers config, config format
                can refer addDriver help
        """
        if type(cfgs) == str:
            cfgs = read_json(cfgs)
        if type(cfgs) != dict:
            cfgs = dict(cfgs)
        for driverName in cfgs.keys():
            self.add_driver(driverName, cfgs[driverName])

    def add_driver(self, name, cfg):
        #try:

        if cfg['type'] == 'tcp':
            driver_obj = TcpDriver(cfg)
        # add tcp_zynq type
        elif cfg['type'] == 'tcp_zynq':
            driver_obj = ZYNQ(cfg, publisher=self.pub, uut=self.uut,psw=self.objPsw)
        elif cfg['type'] == 'dut':
            driver_obj = dut(cfg,self.pub, self.uut,self.g_lock,self.__driverDict["ZYNQ"],self.objNano,self.objSdev)
            if self.bCallBack == False:

                dictArgs={}
                dictArgs["zynq"]=self.__driverDict["ZYNQ"]
                dictArgs["dut"] = driver_obj
                driver_obj_callback = CallBack(dictArgs)
                self.__driverDict.setdefault("callback", driver_obj_callback)

                self.__driverDict["ZYNQ"].SetDut(dictArgs["dut"])
                self.__driverDict["ZYNQ"].reset()
                self.bCallBack = True
        else:
            return
            # raise Exception('check driver type')
        self.__driverDict.setdefault(name, driver_obj)
        #except Exception as e:
        #    raise e

    def list_drivers(self):
        print "Driver Check {}:{}".format(self.uut,self.__driverDict)
        return self.__driverDict

    def __getitem__(self, item):
        if item in self.__driverDict:
            try:
                return self.__driverDict[item]
            except:
                raise Exception(KeyError)

    def getDriver(self, item):
        try:
            driver = self.__driverDict[item]
            assert isinstance(driver, TcpDriver)
            return driver
        except Exception as e:
            raise e

    def checkValue(self, result):
        assert isinstance(result, str)
        result = str(result)
        result = result.lower()
        # print(result)
        if 'ok' in result:
            s = result

            if '=' in s:
                s = result.split('=')[1]
                s = s.split('ok')[0]
                return s
            else:
                print(s)
                return '--PASS--'
        else:
            return '--FAIL--'

    def beryCheckValue(self, result):
        assert isinstance(result, str)
        # print(result)
        result = result.split('\r')[0]
        result = result.split(' OK')[1]
        return result

    def sendCMD(self, method, prams, netName):
        catchResult = None
        getValue = False
        try:
            cmdName, staticPrams = self.nameMap[netName][method]
            cmdList = self.cmdMap[cmdName]
        except Exception as e:
            try:
                print(cmdName)
                print(staticPrams)
                print(cmdName)
            except:
                pass
            return 'Miss netName or cmd'
            # raise Exception('get value error')
        cmdStr = ''
        portStr = ''
        for pc in cmdList:
            cmdStr += pc[1]
            portStr += pc[0]
            cmdStr += ';'
            portStr += ';'
        # print(method, netName, cmdStr, staticPrams, prams)

        try:
            if '{seq}' in cmdStr:
                if prams != '':
                    if '{}' in cmdStr:
                        cmdStr = cmdStr.format(*staticPrams, seq=prams)
                    else:
                        cmdStr = cmdStr.format(seq=prams)
                else:
                    raise Exception('need seq prams')
        except:
            raise Exception('step 1 error')
        try:
            if staticPrams:
                cmdStr = cmdStr.format(*staticPrams)
        except:
            raise Exception('step 2 error')
        ports = portStr[:-1].split(';')
        cmds = cmdStr[:-1].split(';')
        # logging.info('\r' + method)
        # logging.info(netName)
        for i in range(len(cmds)):
            try:
                p, c = ports[i], cmds[i]
            except:
                raise Exception('get port and cmd error ' + p + c)
            try:
                if p[0] == '*':
                    getValue = True
                    p = p[1:]
            except:
                raise Exception('format error' + p + c)
            # logging.info(p+':'+c)
            try:
                driver = self.getDriver(p)
                # print(p)
            except Exception as e:
                raise e
            result = driver.req_recv(c)
            # self.log(p + ':' + c)
            # print(result)
            # self.log(result)
            if 'ok' not in result.lower():
                return '--FAIL--'
            # logging.info(result)
            # aftercheck = self.checkValue(result, c)
            if getValue:
                catchResult = self.checkValue(result)
                getValue = False
        # print('sent')
        if catchResult:
            return catchResult
        else:
            return '--PASS--'

    # TODO:  add the special send CMD
    def send_spec_CMD(self, port, cmd, timeout=1000, flag='\r'):
        result = None
        driver = self.getDriver(port)
        try:
            driver.connect()
            time.sleep(0.05)
            driver.sendMCU(cmd + "\r\n")
            result = driver.recvData(timeout, flag, self.transport)
            driver.disconnect()
        except Exception as e:
            print('cmd:' + cmd + 'error')
            if cmd == 'beryl pwr mode get':
                return 'No Response'
            else:
                raise e
        # print(result)
        # self.log(port+':'+cmd)
        # self.log(result)
        return result

        # TODO:  add the special send CMD

    def send_spec_CMD_no_rep(self, port, cmd):
        result = None
        driver = self.getDriver(port)
        try:
            driver.connect()
            time.sleep(0.05)
            driver.sendMCU(cmd + "\r\n")
            driver.disconnect()
            # self.log(port + ':' + cmd)
        except Exception as e:
            print('cmd:' + cmd + 'error')
            raise e
        return "--PASS--"

    def closeAll(self):
        """
        Close all TcpDriver connection in manager
        -----------------------------------------
        """
        for driver in self.__driverDict.values():
            driver.close()
            # print('Driver %s has closed' % driver)

    def checkConnetion(self):
        l = []
        for driver in self.__driverDict.values():
            l.append(driver.status)
        return l

    def send_recv_by_driver(self, funcname, param, port):
        driver = self.getDriver(port)
        driver.sendMsg(param, funcname=funcname)
        try:
            result = driver.recvMsg()
        except:
            raise Exception('cmd:' + ' error')
        if result != None:
            return result
        if result == '':
            raise Exception('no result')

    def send_recv(self, cmd, port):
        driver = self.getDriver(port)
        return driver.req_recv(cmd)
