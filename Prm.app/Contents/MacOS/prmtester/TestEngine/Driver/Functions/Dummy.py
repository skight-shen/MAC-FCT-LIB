from Common.tinyrpc.dispatch import public


class Dummy(object):
    def __init__(self):
        super(Dummy, self).__init__()

    @public('skip')
    def skip(self, *args, **kwargs):
        return True

    @public('add')
    def add(self, *args, **kwargs):
        return float(args[0]) + float(args[1])

    @public('sub')
    def sub(self, *args, **kwargs):
        return float(args[0]) - float(args[1])

    @public('div')
    def dev(self, *args, **kwargs):
        return float(args[0]) / float(args[1])

    @public('mul')
    def mul(self, *args, **kwargs):
        return float(args[0]) * float(args[1])
