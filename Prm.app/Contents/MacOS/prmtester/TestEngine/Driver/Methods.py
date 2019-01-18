from Common.tinyrpc.dispatch import public


class Command(object):
    def __init__(self):
        super(Command, self).__init__()

    @public('vendorid')
    def vendorid(self):
        return "prmeasure"
