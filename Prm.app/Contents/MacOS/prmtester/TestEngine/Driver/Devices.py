# -*- coding: utf-8 -*-
import json
from .Functions import *
from DriverManager import DriverManager


class DriverObjs(object):
    def __init__(self, uut_num=0, publisher=None,lock=None,nano=None,sdev=None,psw=None):
        # set current uut index
        print "Check Create Driver Objsis UUT{}".format(uut_num)
        self.objNano = nano
        self.objSdev = sdev
        self.objPsw = psw
        self.g_lock =lock
        self.device_dict = {}
        self.driver_configs = {}
        self.uut_num = 'uut' + str(uut_num)
        # create a DriverManager


        self.DriverMgr = DriverManager(uut_num,self.g_lock, self.objNano,self.objSdev,self.objPsw)
        self.DriverMgr.pub = publisher
        # load current UUT Config
        self.load_config()
        self.DriverMgr.loadConfig(self.driver_configs[self.uut_num])

        #self.cbObj = CallBack(self.DriverMgr.list_drivers().get('ZYNQ'))
        self.dummyObj = Dummy()
        self.generalObj = General()
        self.fixtureObj = Fixture(publisher)

        #self.device_list.setdefault('callback', self.cbObj)
        self.device_dict.setdefault('dummy', self.dummyObj)
        self.device_dict.setdefault('general', self.generalObj)
        self.device_dict.setdefault('fixture', self.fixtureObj)
        drives = self.DriverMgr.list_drivers()
        for key in drives.keys():
            self.device_dict.setdefault(str(key).lower(), drives[key])

    def load_config(self):
        config_file = '/'.join(__file__.split('/')[:-2]) + '/DriverConfig.json'
        print("driver config locate at: %s" % config_file)
        # load driver configs
        f = open(config_file, 'r')
        self.driver_configs = json.load(f)
        f.close()

    def getDeviceList(self):
        return self.device_dict

