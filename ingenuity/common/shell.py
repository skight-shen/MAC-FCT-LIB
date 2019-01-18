import os, commands, subprocess

class Shell(object):
    def __init__(self, cmd=None):
        self.output = []
        self.status = -1
        self.cmd = cmd

    def run_shell_getstatus(self):
        self.status = os.system(self.cmd)
        if self.status:
            return 0
        else:
            return 1

    def run_shell_getoutput(self):
        file = os.popen(self.cmd)
        ret = file.read()
        self.output = ret.splitlines()

        return self.output

    def run_shell_getstatusoutput(self):
        self.status, ret = commands.getstatusoutput(self.cmd)
        self.output = ret.splitlines()
        return self.status, self.output

    #creat a new process to run shell cmd
    def run_shell(self,cmd):
        self.cmd = cmd
        self.status = subprocess.Popen(self.cmd, shell=True)

