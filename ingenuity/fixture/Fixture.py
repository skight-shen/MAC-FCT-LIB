from ingenuity.tinyrpc.dispatch import public
from ingenuity.driver.dataDriver import TcpClient
import time

'''
fixture here has a specific meaning. It means that mechanism to put the DUT in place for testing. In a CRC sense its responsibility
is to make the DUT mechanically ready. This is obvious from the minimal functions it needs to implement
'''
class Fixture(object):
    '''this is a dummy fixture implmentation.
    real fixtures dont' need to necessarily inherit from this class but they should implment the same functions
    '''

    def __init__(self):
        self.is_open = False
        self.is_close = True
        self.is_engaged = False
        self.is_disengaged = False
        self.state = 'READY'

        self.fixture = TcpClient(('169.254.1.32', 7643))
        self.serving = self.fixture.connect()
        if not self.serving:
            print 'Failed to connect tcp server'
        else:
            print 'Successfully connect to tcp server'

    #These should be a non-blocking calls if it takes a while. Client should use the is_XXX for the status
    @public('open')
    def open(self):
        #in a real implementation, on_open may not be called here because we don't want open() to be a blocking call
        while 1:
            recv = self.fixture.req_recv("S:OUT")
            if 'OK' in recv:
                self.is_open = True
                self.is_engaged = False
                self.is_disengaged = True
                self.is_close = False
                time.sleep(3)
                return True
            else:
                print "Open:"+recv

    @public('close')
    def close(self):
        while 1:
            recv = self.fixture.req_recv("S:IN")
            if 'OK' in recv:
                self.is_open = False
                self.is_engaged = False
                self.is_disengaged = False
                self.is_close = True
                time.sleep(3)
                return True
            else:
                print "CLOSE:"+recv

    @public('engage')
    def engage(self):
        while 1:
            recv = self.fixture.req_recv('S:DOWN')
            if 'OK' in recv:
                self.is_engaged = True
                self.is_disengaged = False
                self.is_close = True
                self.is_open = False
                self.state = 'READY'
                time.sleep(3)   #why need to delay 3s ?
                return True
            else:
                print "Engage:"+recv

    @public('disengage')
    def disengage(self):
        while 1:
            recv = self.fixture.req_recv('S:UP')
            if 'OK' in recv:
                self.is_engaged = False
                self.is_disengaged = True
                self.is_close = False
                self.is_open = False
                self.state = 'NONLOADED'
                time.sleep(3)
                return True
            else:
                print "Disenage:"+recv

    def is_open(self):
        return self.is_open

    def is_close(self):
        return self.is_close

    def is_engaged(self):
        return self.is_engaged

    def is_disengaged(self):
        return self.is_disengaged

    @public
    def led_switch(self, *args):
        state = args[0]
        self.fixture.sendMsg(state)
        result = self.fixture.recvMsg()
        return result

    @public
    def dut_status(self, *args):
        self.fixture.sendMsg('DUT STATUS')
        result = self.fixture.recvMsg()
        if 'OK' in result:
            return True
        else:
            return False

    @public("get_state")
    def get_state(self):
        return self.state

    @public("set_state")
    def set_state(self, stat):
        self.state = stat

    #listeners = []
    #the fixture implment these events. Implement the listener interface
    #and add yourself to the listener list if you want to subscriber to the events
