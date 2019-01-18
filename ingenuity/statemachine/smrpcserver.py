from ingenuity.loggers import ZmqPublisher
from ingenuity.rpc_server import RPCServerWrapper
from ingenuity.rpc_client import RPCClientWrapper
from ingenuity.loggers.subscriberManager import Subscriber
from ingenuity.fixture.FixtureClient import FixtureClient
from threading import Thread
import zmq
from ingenuity import zmqports
from statemachine import TesterStateMachine
import time
import traceback
import argparse
from ingenuity.loggers import levels

class StatemachineServer(Thread):
    def __init__(self, sequencers=None, publisher=None, count=0):
        super(StatemachineServer, self).__init__()

        self.site_count = count
        self.sequencers = sequencers

        if publisher:
            self.publisher = publisher
        else:
            ctx = zmq.Context().instance()
            self.publisher = ZmqPublisher(ctx, "tcp://*:" + str(zmqports.SM_RPC_PUB), "SM_RPC_SERVER")
            time.sleep(1)#give the publisher sometime

        if sequencers is None:
            self.sequencers = self.connect_to_sequencers(self.site_count)

        self.sm = TesterStateMachine(self.sequencers)
        self.dispatcher = self.sm
        self.rpc_server = RPCServerWrapper(
            zmqports.SM_PORT,
            self.publisher,
            dispatcher=self.dispatcher
        ).rpc_server


    #@staticmethod
    def connect_to_sequencers(self,site_count):
        '''
        This is a helper method to connect to sequencers
        '''
        ctx = zmq.Context().instance()
        sites = range(site_count)
        url = "127.0.0.1"
        sequencers = [RPCClientWrapper("tcp://" + url + ':' + str(zmqports.SEQUENCER_PORT + site),
                                       ZmqPublisher(ctx, "tcp://*:" + str(zmqports.SEQUENCER_PROXY_PUB),
                                                    "SEQUENCER_PROXY")).remote_server() for site in sites]
        return sequencers

    def stop_sequencers(self):
        for sequencer in self.sequencers:
            sequencer.client.transport.shutdown()
            sequencer.client.publisher.stop()


    def run(self):
        self.publisher.publish('Sequencer Starting...')
        print 'statemachine server starting\n'
        try:
            self.rpc_server.serve_forever()
            self.publisher.publish('Sequencer Stopped...')
            self.stop_sequencers()
            self.sm.log_handler.close() #since the thread can not be started again, I am not bothering to reset SM to a usable state.
        except Exception as e:
            print 'error running the state machine rpc server: ' + e.message
            print traceback.format_exc()
        print 'state machine server stoping'


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', help='the count of the sequencer thread', type=int, default=1)

    args = parser.parse_args()

#    sequencers = StatemachineServer.connect_to_sequencers(args.count)
    server = StatemachineServer(count=args.count)
    server.start()

    assert server.rpc_server.serving
