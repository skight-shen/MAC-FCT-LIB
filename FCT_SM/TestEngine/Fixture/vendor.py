from x527.tinyrpc.dispatch import public
from .. Dispatcher import siteobj
class vendor(siteobj):
 	def __init__(self):
 		super(vendor, self).__init__()
 		
	@public('vendor_id') 
	def myName(self,args,kwargs):
		unit=self.get_unit(kwargs)
		timeout=self.get_timeout(kwargs)
		self.logger.info("timeout={0}ms, unit={1}".format(timeout,unit))
		return "My BRAND"
	
	