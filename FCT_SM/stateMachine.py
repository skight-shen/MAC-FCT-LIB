#!/usr/bin/python
import os, sys
#os.system("export PYTHONPATH='/Library/python-sequencer'")
#os.sys.path.append()

import argparse
import cmd
import csv
import time
from threading import Thread
#import thread
import zmq
from x527 import zmqports
from x527.loggers import StdOutPublisher, ZmqPublisher
from x527.rpc_client import RPCClientWrapper
from x527.rpc_server import RPCServerWrapper
from x527.tinyrpc.protocols import jsonrpc
from TestEngine.Engine import *

site=1

cwd = os.path.split(__file__)[0]
TestPlan = os.path.join(cwd, 'TestEngine/Engine.py')


te = TestEngine(site) #site 1
te.start()
print "start TestEngine_{0}".format(site)
time.sleep(1)

def seq():
	print "starting sequencer_{0}".format(site)
	os.system("python /Library/python-sequencer/x527/sequencer/sequencer.py -c -s {0} -f 1".format(1)) #site
	print "Quit sequencer_{0}".format(site)

# def logger():
# 	print "starting Logger with Pudding disabled"
# 	os.system("python /Library/python-sequencer/x527/loggers/logger.py --disable_pudding")
# 	print "Quit Logger with Pudding disabled"
# 	




#thread.start_new_thread(logger,())
#logger_thread = Thread(target=logger,'Logger')
#logger_thread.start()

time.sleep(1)

#thread.start_new_thread(seq,())
seq_thread = Thread(target=seq)
seq_thread.start()
