from ingenuity.tinyrpc.dispatch import public
from ingenuity.driver.LibCallPy import *
import time


class Callback(object):
    def __init__(self, zynq = None):
        #self.nanohippo = cNanoHippoPy()
        self.zynq = zynq
        self.startTime = None
        #self.armDL = cCArmDLpy()

    @public
    def start_test(self,*argas, **kwargs):
        self.startTime = time.time()
        self.zynq.reset()
        # TODO:Create log folder and debug.log


        # TODO: STOP POWER SEQUENCER
        # TODO: CLOSE DATALOGGER AND STOP PWR SEQ MONITORING
        # TODO: RESET FIXTURE
        return True

    @public
    def end_test(self, *args, **kwargs):
        self.zynq.reset()

        return True

    @public
    def totaltime(self, *args, **kwargs):
        totalTime = "%0.03f"%(time.time() - self.startTime)
        return totalTime
