from ingenuity.loggers import ZmqPublisher
from ingenuity.rpc_server import RPCServerWrapper
from threading import Thread
import zmq
from ingenuity import zmqports
import time
import argparse
from ingenuity.tinyrpc.dispatch import RPCDispatcher
from ingenuity.driver.LibCallPy import *
from ingenuity.testEngine.functions.Callback import *
from ingenuity.testEngine.functions.potassium import *
from ingenuity.testEngine.functions.dut import *
from ingenuity.testEngine.functions.zynq import Zynq
from ingenuity.testEngine.functions.common import Common
from ingenuity.testEngine.functions.battery_emulator import BatteryEmulator
import json
import six
import inspect

for osPath in ['/Users/admin/PycharmProjects/Repository/MAC-FCT-LIB/ingenuity','/Users/admin/PycharmProjects/Repository/MAC-FCT-LIB/python-sequencer','/Library/python-sequencer']:
    if os.path.isdir(osPath):
        os.putenv("PYTHONPATH", osPath)
        #sys.path.append(osPath)
sys.path.append(os.getcwd())

class TestEngine(RPCDispatcher):

    def __init__(self, slotid):
        super(TestEngine, self).__init__()
        self.funTable = self.load_config('./functionTable.json')
        self.modules = {}   # {module_name : object}
        #self.nanohippo = cNanoHippoPy()
        self.slotID = slotid
        self.dispatcher = RPCDispatcher()


    def register_class(self):
        self.modules = self.get_modules()
        for module in self.modules.values():
            for name, f in inspect.getmembers(
                    module, lambda f: callable(f) and hasattr(f, '_rpc_public_name')
            ):
                self.dispatcher.add_method(f, f.__name__)
            #self.dispatcher.register_instance(module)
        self.add_subdispatch(self.dispatcher)

    def get_modules(self):
        """
        #create instance by class string name:
        class A():
            def __init__(self):print ('A')
        
        eval("A()")
        :return: 
        """
        modules = {}
        for key in self.funTable.keys():
            if self.funTable.has_key('Zynq'):
                modules['Zynq'] = Zynq(addr=('169.254.1.32', 7600))
            if self.funTable.has_key('Callback'):
                modules['Callback'] = Callback(modules.get('Zynq', None))
            #if key == 'Potassium':
            #    modules[key] = globals()[key](self.slotID, None)
            if self.funTable.has_key('Dut'):
                cfg = {
                'port' : '/dev/cu.usbserial-usbvdm32',
                'baudrate' :  115200,
                'parity' : 'N',
                'bytesize' : 8,
                'stopbits' : 1,
                'timeout' : 2,
                'end_str' : '\r\n'
                }
                modules['Dut'] = Dut(self.slotID, None, cfg)
            if key == "BatteryEmulator":
                modules[key] = globals()[key](modules.get('Dut', None),('169.254.1.32', 7600))
            if self.funTable.has_key('Common'):
                modules['Common'] = globals()['Common']()
            '''if key == "Callback":
                #self.funTable.has_key("Callback")
                modules[key] = globals()[key]()
            if key == "BatteryEmulator":
                modules[key] = globals()[key](('169.254.1.32', 7600))
            if key == 'Potassium':
                modules[key] = globals()[key](self.slotID, None)
            if key == 'Dut':
                modules[key] = globals()[key](self.slotID, None)
            if key == 'Zynq':
                modules[key] = globals()[key](('169.254.1.32', 7600))
            if self.funTable.has_key('Common'):
                modules['Common'] = globals()['Common']()
'''
        return modules

    def load_config(self,config_file):
        with open(config_file, 'rU') as f:
            config = json.load(f)
        return config



class TestEngineServer(Thread):
    def __init__(self, site):
        super(TestEngineServer, self).__init__()
        self.site = site

        ctx = zmq.Context().instance()
        # Ensure subscriber connection has time to complete
        time.sleep(1)
        self.publisher = ZmqPublisher(
            ctx,
            "tcp://*:" + str(zmqports.TEST_ENGINE_PUB + site),
            "TestEngine_{}".format(site)
        )
        time.sleep(0.5)  # give time for the subscribers to connect to this publisher
        self.dispatcher = TestEngine(self.site)
        self.dispatcher.register_class()

        self.wrapper = RPCServerWrapper(
            zmqports.TEST_ENGINE_PORT + site,
            self.publisher,
            dispatcher=self.dispatcher
        )
        self.rpc_server = self.wrapper.rpc_server

    def run(self):
        print "Starting test engine ..."
        self.publisher.publish('Test Engine {} Starting...'.format(self.site))
        self.rpc_server.serve_forever()
        self.publisher.publish('Test Engine {} Stopped...'.format(self.site))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--site', help='the site of the sequencer to connect to', type=int, default=0)
    args = parser.parse_args()

    server = TestEngineServer(args.site)
    server.start()

    assert server.rpc_server.serving
