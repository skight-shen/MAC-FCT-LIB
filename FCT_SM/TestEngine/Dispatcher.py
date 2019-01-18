#  Created by Ming Yin on 2018/5/27.
import argparse
import cmd
import csv
import time
import inspect
from threading import Thread
import sys
import re
import zmq
import logging
from x527 import zmqports
from x527.loggers import StdOutPublisher, ZmqPublisher
from x527.rpc_client import RPCClientWrapper
from x527.rpc_server import RPCServerWrapper
from x527.tinyrpc.dispatch import RPCDispatcher
from x527.tinyrpc.protocols import jsonrpc


class Dispatcher(RPCDispatcher):
	default_ret = '6000'
	
	def __init__(self, publisher):
		super(Dispatcher,self).__init__()
		self.publisher = publisher
		#self.add_method(self.vendor_id)
		self.add_method(self.end_test)
		self.add_method(self.start_test)
		print 'init dispatcher'

	def dispatch(self, request):
		self.publisher.publish(request.serialize(), 'Dispatcher received request')
        #self.func_list.append(request.method)
#         time.sleep(0.05)  # slow down the response a bit to avoid flooding ZMQ queue
		print('call dispatch '+request.method)
		if request.method == jsonrpc.SERVER_READY:
			return request.respond('--PASS--')
		if request.method == '::stop::':
			self.server.stop_server()  # this will stop the RPC server but console continues
		elif request.method == 'error':
			from x527.tinyrpc.protocols.jsonrpc import JSONRPCInvalidRequestError
			e = JSONRPCInvalidRequestError('fake error')
			return request.error_respond(e)
		else:
			f=self.get_method(request.method)
			print request.args
			print request.kwargs
			return request.respond(f(request.args,request.kwargs))
			#return request.respond(self.default_ret)
			#return f()

	def register_instance(self, obj, prefix=''):
		dispatch = self.__class__(self.publisher)
		for name, f in inspect.getmembers(
			obj, lambda f: callable(f) and hasattr(f, '_rpc_public_name')
		):
			dispatch.add_method(f, f._rpc_public_name)
			print "Dispatch add method {0}".format(f._rpc_public_name)

		# add to dispatchers
		print "call add subdispaters 222222222"
		self.add_subdispatch(dispatch, prefix)

	def end_test(self,args,kwargs):
		return ''
		
	def start_test(self,args,kwargs):
		return ''
		

class siteobj(object):
 	def __init__(self):
 		super(siteobj, self).__init__()
 		self.logger = logging.getLogger("engine_log")
 		self.logger.setLevel(logging.DEBUG)  #CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET
 		formatter = logging.Formatter("%(asctime)s [{0}] [%(levelname)s] - %(message)s".format(self.__class__.__name__))
 		self.logHandle = logging.FileHandler("/Volumes/Documents/Download/FCT_log/Engine.log")
 		#self.logHandle = logging.StreamHandler(stream=sys.stdout)
 		self.logHandle.setFormatter(formatter)
 		self.logger.addHandler(self.logHandle)

	def isnumber(self,o):
		if isinstance(o,int) or isinstance(o,float):
			return True
		p = re.compile('[+-]?\d+(\.\d+)?')
		if self.isstring(o) and p.match(cc[3]) != None:
			return True
		
		self.logger.debug("{0} is not a number".format(o))
		return False
	
	def isstring(self,o):
		if isinstance(o,basestring):
			if len(o.strip())>0:
				return True
			else:
				self.logger.debug("arg:{0} is empty".format(o))
				return False
		else:	
			self.logger.debug("{0} is not a string".format(o))
			return True
	
	def tostring(self,arg):
		if self.isstring(arg):
			return arg
		elif self.isnumber(arg):
			return str(arg)
		else:
			self.logger.debug("{0} is not a string".format(arg))
			return "ERROR"	
			
	def tofloat(self,arg):
		if self.isnumber(arg):
			return float(arg)
		else:
			self.logger.debug("{0} is not a number".format(arg))
			return -99999
	
	def get_timeout(self,kargs):
		if kargs.has_key('timeout') and self.isnumber(kargs['timeout']):
			return kargs['timeout']
		else:
			self.logger.debug("{0} don't have valid timeout value, return default 5000ms".format(kargs))
			return 5000
		
	def get_unit(self,kargs):
		if kargs.has_key('unit'):
			return kargs['unit']
		else:
			self.logger.debug("cant' find unit in {0}".format(kargs))
			return ''
			
	# logger.debug("debug message")
	# logger.info("info message")
	# logger.warn("warn message")
	# logger.error("error message")
	# logger.critical("critical message")

