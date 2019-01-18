from x527.tinyrpc.dispatch import public
from .. Dispatcher import siteobj
class SWD(siteobj):
 	def __init__(self):
 		super(SWD, self).__init__()
 		
	@public('diag') 
	def send(self,args,kwargs):
		arg0=self.tostring(args[0])
		arg1=self.tostring(args[1])
		unit=self.get_unit(kwargs)
		timeout=self.get_timeout(kwargs)
		self.logger.info("arg0={0}, arg1={1},timeout={2}ms, unit={3}".format(arg0,arg1,timeout,unit))
		return timeout
	
	