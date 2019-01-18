from core import *
import core
from ingenuity import zmqports
import time
from datetime import datetime
from ingenuity.tinyrpc.dispatch import RPCDispatcher, public
from sm_interface import *
from ingenuity.fixture.FixtureClient import FixtureClient
from ingenuity.loggers.publisher import ZmqPublisher
import zmq
from ingenuity.tinyrpc.protocols.jsonrpc import JSONRPCRequest

from functools import wraps
import os

class TesterStateMachine(RPCDispatcher):

    states = ['idle', 'ready_to_load', 'testing', 'done', 'ok_to_unload']

    def __init__(self,sequencers):
        super(TesterStateMachine, self).__init__()
        self.log_handler = ZMQHandler('tcp://*:' + str(zmqports.SM_PUB))
        core.logger.handlers = []  #clear out the old handlers
        core.logger.addHandler(self.log_handler)
        core.logger.setLevel(logging.DEBUG)

        self.fixture = FixtureClient().proxy

        self.sequencers = sequencers

        # Initialize the state machine
        self.machine = Machine(model=self, states=TesterStateMachine.states, initial='idle')

        self.dispatcher = RPCDispatcher()
        interface = SM_Interface(self.sequencers)
        self.dispatcher.register_instance(interface,interface.__class__.__name__+'.')

        # At some point, every superhero must rise and shine.
        self.machine.add_transition('dut_ready', 'idle', 'ready_to_load', before=['load_sequence'])
        self.machine.add_transition('abort', 'ready_to_load', 'idle', before='close',after='ledSwitch')
        self.machine.add_transition('start', 'ready_to_load', 'testing', before=['close','engage'], after=['start_test'], conditions=['dut_status'])
        self.machine.add_transition('start', 'testing', 'testing', after='start_test')  #for looping test
        self.machine.add_transition('start', 'done', 'testing', after=['start_test','close','engage'])
        self.machine.add_transition('abort', 'testing', 'done', before='abort_test',after='ledSwitch', conditions=['are_all_finished'])
        self.machine.add_transition('finish', 'testing', 'done', after=['disengage','open'],conditions=['are_all_finished'])
        self.machine.add_transition('will_unload', 'done', 'ok_to_unload', before='disengage',after='ledSwitch')
        self.machine.add_transition('abort', 'ok_to_unload', 'done', before='close',after='ledSwitch')
        self.machine.add_transition('dut_removed', 'ok_to_unload', 'idle', before='close',after='ledSwitch')
        #give the zmq publisher some time
        time.sleep(2)
        self.register_triggers()#this adds the trigger to the dispatcher event map

    #before and after actions, these are not the public events
    def open(self, *args):
        logger.info('open fixutre')
        self.fixture.open()

    def close(self,*args):
        logger.info('fixture close')
        self.fixture.close()

    def abort_test(self, site):
        if site:
            self.site = int(site)
            reply = self.sequencers[self.site].abort().result
        else:
            reply = all(s.abort() for s in self.sequencers)
        return reply

    def engage(self, *args):
        logger.info('engage fixture')
        return self.fixture.engage()

    def start_test(self, e_travelers):
        #send request to sequencer to start test
        logger.info('start to test')
        if e_travelers != None:
            for s_site in e_travelers.keys():
                site = int(s_site)
                self.sequencers[site].run(e_travelers[s_site])
        else:
            self.sequencers[0].run()

    def disengage(self,*args):
        self.fixture.disengage()

        #conditions
    def are_all_finished(self, *args):
        test_states = [s.status().result != "RUNNING" for s in self.sequencers]
        return all(test_states)

    def ledSwitch(self,*args):
        #statemachine sends request to fixture to set the LED status
        logger.info('switch fixture led')
        state = self.get_fixture_state()
        self.fixture.led_switch(state)
        return True

    #check dut presence by sensor
    def dut_status(self, *args):
        self.fixture.dut_status()
        return True

    def load_sequence(self, sequence_db):
        """
        Usage: load [sequence_db_name]
        load a sequencer database. Default loads a randomly generated database
        """
        logger.info('load sequence: '+ sequence_db)
        if not sequence_db:
            return 'you must specify a sequence database name'
        rep = [s.load(sequence_db).result for s in self.sequencers]
        return rep

    def get_fixture_state(self):
        state = ''
        rep = self.fixture.get_state()
        if(hasattr(rep,'result')):
            state = rep.result
            logger.info('get fixture state: {0}'.format(state))
        elif(hasattr(rep,'error')):
            print rep.error
        return state

    def set_fixture_state(self,state):
        logger.info('set fixture state: {0}'.format(state))
        self.fixture.set_state(state)

    def __del__(self):
        self.log_handler.close()

    #register the triggers to be publicly callable RPC methods
    def register_triggers(self):
        for event_name in self.machine.events.keys():
            self.add_method(self.machine.events[event_name].trigger, event_name)
        #add the function to get states
        self.add_method(lambda : self.machine.current_state.name, 'get_state')
        self.add_method(self.load_sequence,'load')
        self.add_method(self.get_fixture_state,'get_fixture_state')
        self.add_method(self.set_fixture_state,'set_fixture_state')
        self.add_subdispatch(self.dispatcher)
