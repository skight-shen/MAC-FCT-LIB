#  Created by Ming Yin on 2018/5/27.
from  SOC.iEFI import SWD
from Fixture.vendor import vendor

def hello(args,kwargs):
	return "Hello World"

# def addobject(_dispatcher,):
# 	for name, f in inspect.getmembers(
# 		obj, lambda f: callable(f) and hasattr(f, '_rpc_public_name')
# 	):
# 		dispatch.add_method(f, f._rpc_public_name)


def register(_dispatcher):
	_dispatcher.add_method(hello)
	
	soc = SWD()
	_dispatcher.register_instance(soc,'')
	
	fixture = vendor()
	print "add object vendor"
	_dispatcher.register_instance(fixture,'')
