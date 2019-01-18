import sys
import os
sys.path.append(os.getcwd())
import time
from Common.BBase import cShell
from ThirdParty.LibCallPy import *
if __name__ == "__main__":
    objPotassiumFinder = cPotassiumIdFinder()
    # SlotSize = 4
    # for i in range(0,SlotSize):
    #     objPotassiumFinder.SetPotassiumId(i+1)

    dictPotassiumUrl={1:"/dev/cu.usbmodem14122",2:"/dev/cu.usbmodem14222",3:"/dev/cu.usbmodem14622",4:"/dev/cu.usbmodem14722"}


    objShell= cShell()
    for nIndex in dictPotassiumUrl.keys():
        objPotassiumFinder.ManualSetPotassiumId(dictPotassiumUrl[nIndex],nIndex)

        strCMD = "ktool {} update ./potassium_main-00001701.bin".format(dictPotassiumUrl[nIndex])
        print ""
        objShell.RunShell_n(strCMD)
        time.sleep(1)
        objShell.RunShell_n("ktool {} setenv charge 0x01".format(dictPotassiumUrl[nIndex]))
        time.sleep(1)
        objShell.RunShell_n("ktool {} setenv default_current 0".format(dictPotassiumUrl[nIndex]))
        time.sleep(1)
        print objShell.RunShell_b_str("ktool {} version | grep FW".format(dictPotassiumUrl[nIndex]))




