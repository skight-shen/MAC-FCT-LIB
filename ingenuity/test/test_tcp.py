from ingenuity.driver.dataDriver import TcpClient
from ingenuity.driver.dataDriver import TcpServer

import threading


class client(threading.Thread):
    def __init__(self):
        super(client, self).__init__()
        self.fixture = TcpClient(('169.254.1.32', 7600))
        self.serving = self.fixture.connect()
        if not self.serving:
            print 'Failed to connect tcp server'
        else:
            print 'connected successfully'

    def send(self, msg):
        self.fixture.sendMsg(msg)

    def recv(self):
        return self.fixture.recvMsg()

    def run(self):
        print 'Start runninng....'
        # self.send('SET CH1:0500')
        # self.send('READ CH1')
        while self.serving:
            data = raw_input("Inputting:")
            self.send(data)
            ret = self.recv()


class server(threading.Thread):
    def __init__(self):
        super(server, self).__init__()
        self.fixture = TcpServer()

    def run(self):
        print "start running...."
        serving = self.fixture.connect()
        if not serving:
            print 'Failed to connect tcp server'
        else:
            print 'connected successfully'


if __name__ == '__main__':
     tcpClient = client()
     tcpClient.start()
