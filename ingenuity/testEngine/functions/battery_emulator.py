# Driver for Apple battery emulator
# Version: v1.0
# Authur: Shen Jiang
# Note: Assume the charging current sense resistor is 5mohm
from ingenuity.tinyrpc.dispatch import public
from ingenuity.driver.dataDriver import TcpClient
import os, sys, time, datetime, re


# Define I2C communication address/bus number
MLB_I2C_PWR_BUS_NUMBER = 11
CHG_IC_7_BIT_ADDR = 0x09
EMU_SET_VOLT_7_BIT_ADDR = 0x0D
EMU_READ_VOLT_CURR_7_BIT_ADDR = 0x4A

# I2C operation table
OPS_TBL = {'-w','-v','-r','d'}
WRITE = 1
DEV_WRITE = 2
READ = 3
DEV_READ = 4

_last_diags_response_ = ""


class BatteryEmulator(TcpClient):
    def __init__(self, objDut = None, addr=('169.254.1.32', 7600)):
        super(BatteryEmulator, self).__init__(addr)
        self._Batt_Max = 12800   # mv
        self._Batt_Min = 7200    # mv
        self._dut = objDut
        if self.connect():
            print 'BatEmulator connected successfully.'
        else:
            print 'BatEmulator failed to connected'
        return

    @public
    def emulator_selfcheck(self,*args,**kwargs):
        try:
            strCmd = "[]io set(2,bit115=1,bit70=1)"  #close relay[]io set(2,bit115=1,bit70=0)
            self.req_recv(strCmd)
            #time.sleep(0.1)
            self.req_recv("[]i2c write(smbus,0d,3,31,FF,FF)")
            #time.sleep(0.1)
            fMin =float(self.zynq_read_voltage())

            self.req_recv("[]i2c write(smbus,0d,3,31,00,00)")
            #time.sleep(0.1)
            fMax =float(self.zynq_read_voltage())

            self.req_recv("[]io set(2,bit115=0,bit70=0)") #disconnect relay

            if fMin <=7 or fMin >=7.4:
                return "--FAIL--, Minimum voltage error, voltage value: {} V".format(fMin)
            if fMax <=12.7 or fMax >=13:
                return "--FAIL--, Maximum voltage error, voltage value: {} V".format(fMax)

        except Exception as e:
            return "--FAIL--, EXCEPTION: %s" % e.message

        return "--PASS--"

    @public
    def zynq_read_voltage(self, *args, **kwargs):
        strVolts = ''
        try:
            self.req_recv("[]i2c write(smbus,4a,1,4c)")
            time.sleep(0.2)
            strRet = self.req_recv("[]i2c read(smbus,4a,3)")
            strRet = re.findall("ACK\((.+),0x4c;",strRet)[0]
            strRet = re.sub(",|0x", "", strRet)
            strValue = int(strRet, 16)
            strVolts = str(7.8 * 2.048 * strValue / 32768)
        except Exception as e:
            return "--FAIL--, %s" % e.message
        return strVolts

    @public
    def zynq_set_sink_current(self, *args, **kwargs):
        return "--PASS--"

    @public
    def zynq_read_sink_current(self, *args, **kwargs):
        return "--PASS--"

    @public
    def zynq_set_voltage(self, *args, **kwargs):
        str_cmd = '[]'+args[0]
        strRet = self.req_recv(str_cmd)
        if 'DONE' in strRet:
            return "--PASS--"
        else:
            return "--FAIL--"


##############################################################
################ Controll battery by diags cmd #############
##############################################################
    @public
    def init_emulator_zynq(self, *args, **kwargs):
        cmd_str = "i2c -w 11 0x22 0x00 0x08 multiple"
        result_1 = self._dut.diags(cmd_str, timeout=20000)
        cmd_str = "i2c -w 11 0x22 0x09 0x80 multiple"
        result_2 = self._dut.diags(cmd_str, timeout=20000)
        return "--PASS--" if 'PASS' in result_1 and 'PASS' in result_2 else '--FAIL--'

    @public
    def trim_battery_output(self, *args, **kwargs):
        return

    @public
    def set_voltage(self, *args, **kwargs):
        fVolt = args[0]
        try:
            if "MV" == kwargs["unit"].upper():
                fVolt = fVolt
            elif "V" == kwargs["unit"].upper():
                fVolt = fVolt * 1000

            if fVolt > self._Batt_Max:
                fVolt = self._Batt_Max
            elif fVolt < self._Batt_Min:
                fVolt = self._Batt_Min
        except Exception as e:
            return "--FAIL--, %s" %e.message
        return "--PASS--"
