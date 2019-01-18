from Common.tinyrpc.dispatch import public
from FixtureCtl.FixtureClient import FixtureClient


class Fixture(object):
    def __init__(self, publisher=None):
        super(Fixture, self).__init__()
        self.fix = FixtureClient()
        self.pub = publisher

    def log(self, msg):
        self.pub.publish(msg)

    @public('open')
    def open(self):
        result = self.fix.open()
        self.log(result)
        if 'OK' in result:
            return '--PASS--'
        else:
            return '--FAIL--'

    @public('fixtureid')
    def fixtureid(self, *args, **kwargs):
        # result = self.fix.send_cmd('')
        return '001'
