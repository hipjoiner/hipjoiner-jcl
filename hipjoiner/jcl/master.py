import os
import subprocess

from hipjoiner.jcl.config import config


def master_help(args=None):
    help_text = """
Usage: master start|stop|status|install|uninstall

    jcl master start            Create new job
    jcl master stop             Cancel job run for the day
    jcl master status           Edit job settings
    jcl master install          Kill running job
    jcl master uninstall        Redo failed job
"""
    print(help_text)


def home():
    return '/'.join([config.home, 'hosts', host()])


def host():
    return os.getenv('COMPUTERNAME').lower()


def master_loop():
    print('Hello, master loop.')


def master_start(args):
    print('Master start...')
    subprocess.Popen('python -m hipjoiner.jcl.master.master_loop')


def master_status(args):
    print('Checking status...')
    print(home())


def master_stop(args):
    print('Master stop...')


fn_map = {
    'install': None,
    'start': master_start,
    'status': master_status,
    'stop': master_stop,
    'uninstall': None,
}


def process_args(args):
    if len(args) < 2:
        return master_help()
    verb = args[1]
    if verb not in fn_map:
        print('JCL master: unrecognized verb "%s"' % verb)
        return master_help()
    if fn_map[verb] is None:
        return print('JCL master: "%s" not implemented yet' % verb)
    fn_map[verb](args[1:])
