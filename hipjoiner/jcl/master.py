from datetime import datetime
from functools import lru_cache
import os
import subprocess
import sys
from time import sleep

from hipjoiner.jcl.config import config


class Master:
    def __init__(self):
        pass

    def help(self, args=None):
        help_text = """
    Usage: master start|stop|status|install|uninstall
    
        jcl master start            Create new job
        jcl master stop             Cancel job run for the day
        jcl master status           Edit job settings
        jcl master install          Kill running job
        jcl master uninstall        Redo failed job
    """
        print(help_text)

    @property
    @lru_cache()
    def home(self):
        home_dir = '/'.join([config.home, 'hosts', self.host])
        os.makedirs(home_dir, exist_ok=True)
        return home_dir

    @property
    def host(self):
        return os.getenv('COMPUTERNAME').lower()

    def log(self, msg):
        print('%s %s' % (datetime.today().strftime('%Y-%m-%d %H:%M:%S'), msg))

    def run(self, args):
        # FIXME: How do we get PID here?  Write it to file
        # FIXME: Redirect stdout/stderr here
        outfpath = '/'.join([self.home, 'master.stdout'])
        self.log('Redirecting stdout to %s...' % outfpath)
        sys.stdout = open(outfpath, mode='w', buffering=1)
        # sys.stderr = open('/'.join([home(), 'master.stderr']), 'w', 0)
        while True:
            self.log('master_loop running...')
            sleep(10)

    def start(self, args):
        print('Master start...')
        # Check status: if running, do nothing

        # Rotate old stdout/stderr files out of the way before launching

        subprocess.Popen(
            'start "Master" /min python -m hipjoiner.jcl.master',
            shell=True,
        )

    def status(self, args):
        print('Checking status...')
        print(self.home)
        # FIXME: Find PID with
        # wmic process where "commandline like '%hipjoiner.jcl.master'" get ProcessId /format:list

    def stop(self, args):
        print('Master stop...')
        # Get PID, send kill instruction, verify dead, and erase PID file
        # NOTE: IIRC, sending kill may not work; may require master to poll for a stop file


master = Master()


fn_map = {
    'install': None,
    'start': master.start,
    'status': master.status,
    'stop': master.stop,
    'uninstall': None,
}


def process_args(args):
    if len(args) < 2:
        return master.help()
    verb = args[1]
    if verb not in fn_map:
        print('JCL master: unrecognized verb "%s"' % verb)
        return master.help()
    if fn_map[verb] is None:
        return print('JCL master: "%s" not implemented yet' % verb)
    fn_map[verb](args[1:])


if __name__ == '__main__':
    master.run(sys.argv)
