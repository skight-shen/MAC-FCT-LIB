import argparse
import time
import os
import sys
import zmq
from ingenuity.tinyrpc.protocols.jsonrpc import RPCError
from ingenuity.loggers.publisher import ZmqPublisher
from ingenuity.rpc_client import RPCClientWrapper
from ingenuity import zmqports
import cmd
from functools import wraps
import readline
import traceback

readline.parse_and_bind("bind ^I rl_complete")

CLASSNAME = 'SM_Interface.'

def handle_response(afunc):

    @wraps(afunc)
    def _(*args, **kwargs):
        try:
            reply = afunc(*args, **kwargs)
            if reply is not None:
                if hasattr(reply,'result'):
                    print reply.result
                elif hasattr(reply,'error'):
                    print reply.error
                else:
                    print reply
        except Exception as e:
            print e.message, os.linesep, traceback.format_exc()
    _.__doc__ = afunc.__doc__
    return _

class StateMachineCmdline(cmd.Cmd):
    prompt = 'sm>'
    intro = 'state machine'

    def __init__(self, sm):
        cmd.Cmd.__init__(self)
        self.sm = sm
        self.stat =''
        self.site = '0'

    def do_EOF(self, line):
        '''Ctrl-D to quit sm_porxy without stopping the sm server'''
        return True

    @handle_response
    def do_abort(self, site):
        '''abort the current running sequence'''
        self.site = site
        return self.sm.__getattr__(CLASSNAME+'abort')(site).result

    @handle_response
    def do_run(self, site):
        '''run the whole sequence without regard for any breakpoint'''
        self.site = site
        return self.sm.__getattr__(CLASSNAME+'run')(site)

    @handle_response
    def do_start(self, line):
        '''start'''
        run_config = {'loop_count':1,'stop_count':-1,'tests_to_run':[]}
        e_travelers = {0:{'attributes':{'sn':000}}}
        start_msg={0:(e_travelers,run_config)}
        return self.sm.start(e_travelers)

    @handle_response
    def do_finish(self, seq):
        '''finish'''
        return self.sm.finish(seq)

    @handle_response
    def do_state(self, line):
        '''get current state'''
        return self.sm.__getattr__('get_state')()

    @handle_response
    def do_load(self, sequence_db):
        """
        Usage: load [sequence_db_name]
        load a sequencer database. Default loads a randomly generated database
        """
        if not sequence_db:
            return 'you must specify a sequence database name'
        return self.sm.load(sequence_db)


    @handle_response
    def do_status(self, site):
        """return the current running status of the sequence"""
        self.site = site
        self.stat = self.sm.__getattr__(CLASSNAME+'status')(site)
        return self.stat

    @handle_response
    def do_next(self,site):
        """show the next line that will be executed"""
        self.site = site
        return self.sm.__getattr__(CLASSNAME+'next')(site)

    @handle_response
    def do_list(self,lines):
        reply = self.sm.__getattr__(CLASSNAME+'list')(lines)
        if hasattr(reply,'result'):
            pc, start, stop = reply.result[0]
            listings = reply.result[1:]
            for item in listings:
                self._show_sequence_item(item, pc)
        return

    def _show_sequence_item(self, item, pc):
        print 'enter to show:'
        line_no = int(item[0])
        if line_no == pc+1:
            sys.stdout.write('-> ')
        else:
            sys.stdout.write('   ')
        test = eval(item[1])
        sys.stdout.write(str(item[0]) + ': ')
        sys.stdout.write('%s  | %s | %s | %s' % (test['GROUP'], test['TID'], test['FUNCTION'], test['DESCRIPTION']))
        if 'PARAM1' in test:
            sys.stdout.write(' | ' + test['PARAM1'])
        sys.stdout.write(os.linesep)
        if 'PARAM2' in test:
            sys.stdout.write(' | ' + test['PARAM2'])
        sys.stdout.write(
            ' | %s | %s | %s | %s | %s ' %
            (test['UNIT'], test['LOW'], test['HIGH'], test['KEY'], test['VAL'])
        )
        sys.stdout.write(os.linesep)

    @handle_response
    def do_break(self,line):
        self.sm.__getattr__(CLASSNAME+'break')(line)

    @handle_response
    def do_all(self,line):
        reply = self.sm.__getattr__(CLASSNAME+'all')(line)
        if hasattr(reply,'result'):
            breakpoints = reply.result
            for point in breakpoints:
                print point

    @handle_response
    def do_continue(self,site):
        """continue execution from the current position,
        if you run continue, breakpoints are honored.
        If you use run, breakpoints are not honored"""
        self.site = site
        reply = self.sm.__getattr__(CLASSNAME+'continue')(site)
        if hasattr(reply,'result'):
            print reply.result
            sys.stdout.write('BREAK: ')
            pc, start, stop = reply.result[0]
            listings = reply.result[1:]
            for item in listings:
                self._show_sequence_item(item, pc)
        elif hasattr(reply,'error'):
            print reply.error
        else:
            return None


    @handle_response
    def do_print(self,var_name):
        reply = self.sm.__getattr__(CLASSNAME+'print')(var_name)
        if reply is not None:
            if hasattr(reply, 'result'):
                return reply.result
            else:
                return reply.error

    @handle_response
    def do_skip(self,line):
        reply = self.sm.__getattr__(CLASSNAME+'skip')(line)
        if hasattr(reply,'result'):
            self._show_sequence_item(reply.result, -100)
        else:
            print 'skip failed'

    @handle_response
    def do_jump(self, dest):
        """jump to the destination. Destination can be line number, group name or TID"""
        reply = self.sm.__getattr__(CLASSNAME+'jump')(dest)
        if hasattr(reply, 'result'):
            self._show_sequence_item(reply.result, -100)
        elif hasattr(reply, 'error'):
            print reply.error

    @handle_response
    def do_wait(self,timeout):
        return self.sm.__getattr__(CLASSNAME+'wait')(timeout)

    @handle_response
    def do_step(self,line):
        self.sm.__getattr__(CLASSNAME+'step')(line)

    @handle_response
    def do_loop(self, count):
        if count == '':
            count = '1'
        count = int(count)
        for i in range(count):
            self.do_run(self.site)
            start = time.time()
            time.sleep(3)
            while True:
                self.do_status(self.site)
                print 'Loop {0} of {1} running, time elapsed={2}s'.format(i+1, count, int(time.time()-start))
                if 'READY' in self.stat.result:
                    print 'loop {0} of {1} finished'.format(i+1, count)
                    break
                time.sleep(5)

    def do_quit(self, site):
        '''quit sm and stop the sequencer server. If you just want to quit sm_proxy without stopping
        the sequencer server you shoudl use ctrl-D'''
        self.site = site
        self.sm.__getattr__(CLASSNAME+'quit')(site)
        self.sm.__getattr__('::stop::')()
        return True


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--site', help='the site of the sequencer to connect to', type=int, default=0)

    args = parser.parse_args()

    SM_proxy = RPCClientWrapper('tcp://localhost' + ':' + str(zmqports.STATEMACHINE_PORT + args.site),
                                ZmqPublisher(zmq.Context().instance(), "tcp://*:" + str(zmqports.SM_PROXY_PUB + args.site),
                                             'SMProxy_'+str(args.site)))

    sm = StateMachineCmdline(SM_proxy.remote_server())
    SM_proxy.remote_server().dut_ready('/Users/admin/PycharmProjects/Repository/MAC-FCT-LIB/ingenuity/j213_Test__Plan.csv')
    time.sleep(1)
    sm.cmdloop()

'''
    try:
        sm_proxy = SM_proxy.remote_server()
        s = sm_proxy.get_state().result
        print ('the initial sate is: {0}'.format(s))

        sm_proxy.dut_ready()
        assert 'ready_to_load'==sm_proxy.get_state().result

        sm_proxy.abort(0)
        assert 'idle'==sm_proxy.get_state().result

        sm_proxy.dut_ready()
        assert 'ready_to_load'==sm_proxy.get_state().result

        #start testing
        e_travelers ={0:{'attributes':{'sn':'000'}}}
#        e_travelers ={0:{'attributes':{'sn':'001'}}, 2:{'attributes':{'sn':'002'}}, 3:{'attributes':{'sn':'003'}}}
        sm_proxy.start(e_travelers)
        response = sm_proxy.get_state()
        if response is None:
            print "empty resposne"
        elif hasattr(response,'result'):
            assert 'testing'== sm_proxy.get_state().result
        elif hasattr(response,'error'):
            print response.error
        else:
            print response
        sm_proxy.finish()
#        assert 'done'== sm_proxy.get_state().result

        e_travelers ={0:{'attributes':{'sn':'000'}}}
        sm_proxy.start()
#        assert 'testing' == sm_proxy.get_state().result

        sm_proxy.abort(0)
#        assert 'done'== sm_proxy.get_state().result

        sm_proxy.will_unload()
#        assert 'ok_to_unload' == sm_proxy.get_state().result

        sm_proxy.abort()
#        assert 'done' == sm_proxy.get_state().result

        sm_proxy.will_unload()
#        assert 'ok_to_unload' == sm_proxy.get_state().result

        sm_proxy.dut_removed()
#        assert 'idle'== sm_proxy.get_state().result

    except Exception as e:
        error_msg = e.message + os.linesep + traceback.format_exc()
        print error_msg

    finally:
#        sm_proxy.__getattr__('::stop::')()
        sm.cmdloop()
'''