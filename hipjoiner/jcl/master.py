import msvcrt
from datetime import datetime, date
from functools import lru_cache
import os
from shutil import copyfile
import subprocess
import sys
from time import sleep

from hipjoiner.jcl.config import config
from hipjoiner.jcl.job import all_jobs


class Master:
    def __init__(self):
        self.current_day = date.today()
        self.stdout_save = sys.stdout
        self.stderr_save = sys.stderr
        self.stdout_fp = None
        self.stderr_fp = None

    def change_date(self, today):
        self.log('Date change; rotating output files...')
        self.output_stop_redirect()
        self.output_files_rotate()
        self.current_day = today
        self.output_redirect()
        self.log('Today is %s' % today)
        # Create relevant procs copies, log directory
        dated_jobs_dir = '/'.join([config.log_dir(today), 'jobs'])
        os.makedirs(dated_jobs_dir, exist_ok=True)
        for job, fpath in all_jobs():
            dated_fpath = '/'.join([dated_jobs_dir, job + '.json'])
            copyfile(fpath, dated_fpath)
        os.makedirs(config.queue_dir(today), exist_ok=True)

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
        home_dir = '/'.join([config.home, 'hosts', config.host])
        os.makedirs(home_dir, exist_ok=True)
        return home_dir

    def log(self, msg):
        print('%s %s' % (datetime.today().strftime('%Y-%m-%d %H:%M:%S'), msg))

    def loop(self):
        new_date = self.new_date()
        if new_date:
            self.change_date(new_date)
        self.log('Master loop...')

    @property
    def master_pid(self):
        # We trust wmic for true PID/process status; we only write file PID for audit purposes
        pid = self.pid_from_wmic
        if pid:
            if pid != self.pid_from_file:
                self.write_pid_file(pid)
        else:
            if os.path.isfile(self.pid_fpath):
                os.remove(self.pid_fpath)
        return pid

    def new_date(self):
        today = date.today()
        if self.current_day != today:
            return today
        return None

    def output_files_rotate(self):
        stamp = datetime.now().strftime('%Y-%m-%d-at-%H-%M-%S')
        outfpath = self.stdout_fpath
        if os.path.isfile(outfpath) and os.stat(outfpath).st_size:
            out_stamped = '/'.join([config.host_dir(self.current_day), 'master-%s.out' % stamp])
            self.log('Renaming %s to %s...' % (outfpath, out_stamped))
            os.rename(outfpath, out_stamped)
        errfpath = self.stderr_fpath
        if os.path.isfile(errfpath) and os.stat(errfpath).st_size:
            err_stamped = '/'.join([config.host_dir(self.current_day), 'master-%s.err' % stamp])
            self.log('Renaming %s to %s...' % (errfpath, err_stamped))
            os.rename(errfpath, err_stamped)

    def output_redirect(self):
        self.log('Redirecting stdout to %s...' % self.stdout_fpath)
        self.log('Redirecting stderr to %s...' % self.stderr_fpath)
        self.stdout_fp = open(self.stdout_fpath, mode='w', buffering=1)
        self.stderr_fp = open(self.stderr_fpath, mode='w', buffering=1)
        sys.stdout = self.stdout_fp
        sys.stderr = self.stderr_fp

    def output_stop_redirect(self):
        self.log('Stopping redirects...')
        if self.stdout_fp:
            self.stdout_fp.close()
            sys.stdout = self.stdout_save
            self.log('Closed stdout file %s...' % self.stdout_fpath)
        if self.stderr_fp:
            self.stderr_fp.close()
            sys.stderr = self.stderr_save
            self.log('Closed stderr file %s...' % self.stderr_fpath)

    @property
    def pid_fpath(self):
        return '/'.join([self.home, 'master.pid'])

    @property
    def pid_from_file(self):
        if os.path.isfile(self.pid_fpath):
            pid = ''.join(open(self.pid_fpath, 'r').readlines())
            return pid
        return None

    @property
    def pid_from_wmic(self):
        wmic = subprocess.run(
            'wmic process where "commandline like \'%hipjoiner.jcl.master\'" get ProcessId /format:list',
            capture_output=True
        )
        output = wmic.stdout.decode().strip().split('\n')
        if len(output) > 1:
            raise RuntimeError('Too many masters running:\n%s' % '\n'.join(['  %s' % line for line in output]))
        if len(output):
            return output[0].replace('ProcessId=', '')
        return None

    def run(self):
        pid = os.getpid()
        self.log('Master started as PID %s; saving to %s...' % (pid, self.pid_fpath))
        self.write_pid_file(pid)
        self.output_redirect()
        while True:
            self.loop()
            secs = 60
            self.log('Sleep %d sec...' % secs)
            sleep(secs)

    def start(self, args):
        self.log('Master start...')
        # Check status: if running, do nothing
        pid = self.master_pid
        if pid:
            return self.log('WARNING: Master is already running, PID %s; taking no action' % pid)
        self.output_files_rotate()
        self.log('Launching Master...')
        subprocess.Popen(
            'start "Master" /min python -m hipjoiner.jcl.master',
            shell=True,
        )
        pid = self.master_pid
        if pid:
            self.log('Master is running, PID %s' % pid)
        else:
            self.log('ERROR, Master is not running; no PID found')

    def status(self, args=None):
        self.log('Checking Master status...')
        pid = self.master_pid
        fpid = self.pid_from_file
        if fpid:
            self.log('PID file %s says Master PID is %s' % (self.pid_fpath, fpid))
        else:
            self.log('PID file %s not found' % self.pid_fpath)
        if pid:
            self.log('WMIC says Master PID is %s' % pid)
            self.log('Master is running.')
        else:
            self.log('WMIC says no Master PID')
            self.log('Master is not running.')
        return pid

    @property
    def stderr_fpath(self):
        return '/'.join([config.host_dir(self.current_day), 'master.err'])

    @property
    def stdout_fpath(self):
        return '/'.join([config.host_dir(self.current_day), 'master.out'])

    def stop(self, args=None):
        self.log('Master stop...')
        # Get PID, send kill instruction, verify dead, and erase PID file
        pid = self.pid_from_file
        stopped = False
        if not pid:
            self.log('File says no PID; not killing anything.')
            stopped = True
        else:
            result = subprocess.run('taskkill /F /PID %s' % pid, capture_output=True)
            output = result.stdout.decode().strip()
            expected = 'SUCCESS: The process with PID %s has been terminated.' % pid
            if output == expected:
                self.log('Master (was PID %s) has stopped.' % pid)
                stopped = True
            else:
                self.log('FAILED: Master (PID %s) was not terminated.' % pid)
        if os.path.isfile(self.pid_fpath) and stopped:
            os.remove(self.pid_fpath)
            self.log('PID file %s removed.' % self.pid_fpath)

    def tail(self, args=None):
        n = 10
        if args:
            n = abs(int(args[0]))
        self.log('Tailing master log %s...' % self.stdout_fpath)
        with open(self.stdout_fpath, 'r') as fp:
            for line in fp.readlines()[-n:]:
                print(line, end='')
            pos = fp.tell()
        try:
            while True:
                with open(self.stdout_fpath, 'r') as fp:
                    fp.seek(pos)
                    data = fp.read()
                    if data:
                        print(data, end='')
                        pos = fp.tell()
                if keypressed():
                    return
                sleep(1)
        except KeyboardInterrupt:
            return

    def write_pid_file(self, pid):
        with open(self.pid_fpath, 'w') as fp:
            fp.write(str(pid))


def keypressed():
    if msvcrt.kbhit():
        msvcrt.getch()
        return True
    return False


master = Master()


fn_map = {
    'install': None,
    'start': master.start,
    'status': master.status,
    'stop': master.stop,
    'tail': master.tail,
    'uninstall': None,
}


def process_args(args):
    if args == ['tail']:
        return master.tail()
    if len(args) < 2:
        return master.help()
    verb = args[1]
    if verb not in fn_map:
        print('JCL master: unrecognized verb "%s"' % verb)
        return master.help()
    if fn_map[verb] is None:
        return print('JCL master: "%s" not implemented yet' % verb)
    fn_map[verb](args[1:])


def run():
    master.run()


if __name__ == '__main__':
    run()
