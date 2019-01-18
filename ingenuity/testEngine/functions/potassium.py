# Version: v1.0
# Authur: Shen Jiang

#from ingenuity.driver import LibCallPy
from ingenuity.tinyrpc.dispatch import public
from ingenuity.testEngine.functions.shell import Shell
import time, os


class Potassium(object):
    def __init__(self,potassiumurl=None, nanohippo=None):
        self.nanohippo = nanohippo
        self.state = -1
        self.potassium = potassiumurl
        self.potassiumfinder = PotassiumIdFinder()

    @public
    def potassium(self, *args, **kwargs):
        if args[0]:
            self.state = self.nanohippo.connect()
        else:
            self.state = self.nanohippo.disconnect()

        if not self.state:
            return "--PASS--"
        else:
            self.potassium_reset()
            if args[0]:
                self.state = self.nanohippo.Connect_b()
            else:
                self.state = self.nanohippo.Close()

            if not self.state:
                return "--PASS--"
            else:
                return "--FAIL--"

    def reconnect(self):
        self.nanohippo.close()
        self.nanohippo.Connect_b()

    def potassium_reset(self):
        cmd = 'reset'
        self.potassiumfinder.run_cmd(cmd, self.potassium)
        if not self.potassiumfinder.status:
            time.sleep(0.5)
            self.nanohippo.Connect_b()
            time.sleep(1)
            self.nanohippo.DutSendString_n("")
            time.sleep(1)
            self.nanohippo.DutReadString_str()

class PotassiumIdFinder(Shell):
    def __init__(self, cmd=None):
        super(PotassiumIdFinder, self).__init__(cmd=cmd)
        self.potassiumID = {0:32, 1:33, 2:34, 3:35}
        self.ktoolPath = '/usr/local/bin/ktool'
        self.potassiumUrl_list = self._GetAllPotassiumUrl()

    def GetPotassiumUrl(self, nIndex):
        cmd = "read_eeprom 0x2004 1 | grep 'INFO: ' | tr -d [:space:]"
        for potassiumUrl in self.potassiumUrl_list:
            potassiumId = self._KtoolReadEEProm(cmd, potassiumUrl)
            if potassiumId == self.potassiumID[nIndex]:
                return potassiumUrl

    def SetPotassiumID(self, slot_id):
        self.potassiumUrl_list.sort()
        for i in range(4):
            slot_id += 1
            cmd = 'write_eeprom 0x2004 0x' + slot_id
            for potassiumurl in self.potassiumUrl_list:
                self.run_cmd(self, cmd, potassiumurl)

    def _KtoolReadEEProm(self, cmd, dest):
        self.run_cmd(cmd, dest, 2)
        return self.output


    def _GetAllPotassiumUrl(self):
        cmd = '/usr/local/bin/nanocom -s | grep usbmodem'
        self.run_cmd(cmd, dest='', selector=2)
        return self.output

    def run_cmd(self, cmd, dest, selector=1):
        if dest:
            self.cmd = self.ktoolPath + ' ' + dest + ' ' + cmd
        else:
            self.cmd = self.ktoolPath + ' ' + cmd

        if selector == 0:
            self.run_shell()  # create a new process and return status/output
        elif selector == 1:
            self.run_shell_getstatus()  # return status
        elif selector == 2:
            self.run_shell_getoutput()  # return output
        elif selector == 3:
            self.run_shell_getstatusoutput()  # return status and output


