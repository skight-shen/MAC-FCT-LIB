from ingenuity.tinyrpc.dispatch import public
from datetime import datetime


class SM_Interface(object):

    def __init__(self, sequencers):
        self.sequencers = sequencers
        self.break_points = []
        self.this_run = None
        self.site = 0

    def do_EOF(self, line):
        """Ctrl-D to quit sdb without stopping the sequencer server"""
        return True

    @public('abort')
    def do_abort(self, site):
        """abort the current running sequence"""
        if site:
            self.site = int(site)
            reply = self.sequencers[self.site].abort().result
        else:
            reply = all(s.abort() for s in self.sequencers)
        return reply

    @public('run')
    def do_run(self, site):
        """run the whole sequence without regard for any breakpoint"""
        if site:
            self.site = int(site)
            return self.sequencers[self.site].run().result
        else:
            return all(s.run() for s in self.sequencers)

    @public('list')
    def do_list(self, lines):
        """list [lines] around the current sequence item"""
        if len(lines) == 0:
            lines = '10'
        reply = self.sequencers[self.site].list(lines)
        if hasattr(reply, 'result'):
            return reply.result
        elif hasattr(reply,'error'):
            return reply.error
        else:
            return None

    @public('break')
    def do_break(self, line):
        """set break point at [line]"""
        if line == '':
            line = '1'
        self.break_points.append(int(line))

    @public('all')
    def do_all(self, line):
        """show all the breakpoints"""
        return ['  ' + str(b) for b in self.break_points]
        for b in self.break_points:
            print '  ' + str(b)

    @public('next')
    def do_next(self, site):
        """show the next line that will be executed"""
        if site:
            self.site = int(site)
            resp = self.sequencers[int(site)].s_next().result
        else:
            resp = [s.s_next().result for s in self.sequencers]

        return resp

    @public('skip')
    def do_skip(self, line):
        """skip the right next test, equal to jump N+1"""
        reply = self.sequencers[self.site].skip()
        if hasattr(reply,'result'):
            return reply.result
        elif hasattr(reply,'error'):
            return reply.error
        else:
            print 'skip failed'
            return None

    @public('continue')
    def do_continue(self, site):
        """continue execution from the current position,
        if you run continue, breakpoints are honored.
        If you use run, breakpoints are not honored"""
        if site:
            self.site = int(site)

        reply = ' '
        if self.this_run is None:
            self.this_run = [b for b in self.break_points]

        while reply is not None:
            next_p = self.sequencers[int(self.site)].s_next().result
            if next_p in self.this_run:
                #                sys.stdout.write('BREAK: ')
                self.this_run.remove(next_p)
                return self.do_list('1')
            reply = self.step_op()

        # we reached the end of the run
        self.this_run = None

    @public('jump')
    def do_jump(self, dest):
        """jump to the destination. Destination can be line number, group name or TID"""
        reply = self.sequencers[self.site].jump(dest)
        if hasattr(reply, 'result'):
            return reply.result
        else:
            print 'fail to jump'

    @public('print')
    def do_print(self, var_name):
        """show the value of [var_name]"""
        ret = self.sequencer.show(var_name)
        if hasattr(ret, 'result'):
            return ret.result
        elif hasattr(ret, 'error'):
            return ret.error
        else:
            return None

    @public('status')
    def do_status(self, site):
        """return the current running status of the sequence"""
        if site:
            self.site = int(site)
            stat = self.sequencers[self.site].status().result
        else:
            stat = [s.status().result for s in self.sequencers]

        return stat

    def step_op(self):
        self.do_list('1')
        t1 = datetime.now()
        reply = self.sequencers[self.site].step()
        if reply is None:
            print 'reached the end of sequence'
        else:
            t2 = datetime.now()
            print 'execution time: ' + str((t2-t1).total_seconds()) + ' seconds'
        return reply

    @public('step')
    def do_step(self, site):
        """execute the current line, move PC to the next line"""
        if site:
            self.site = int(site)
        self.step_op()

    @public('wait')
    def do_wait(self, timeout):
        """wait [timeout] seconds for the test sequence to finish"""
        if timeout == '':
            timeout = '0'
        return self.sequencers[self.site].wait(timeout=int(timeout)).result

    @public('quit')
    def do_quit(self, site):
        """stop the sequencer server. If you just want to quit sdb without stopping
        the sequencer server you should use ctrl-D"""
        if site:
            self.site = int(site)
            self.sequencers[self.site].__getattr__('::stop::')()
        else:
            for s in self.sequencers:
                s.__getattr__('::stop::')()

        return True