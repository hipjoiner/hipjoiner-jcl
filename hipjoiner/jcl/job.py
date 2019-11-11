import json
import os

from hipjoiner.jcl.config import config


def job_help(args=None):
    help_text = """
Usage: jcl [add|cancel|edit|kill|redo|remove|reset|run|show] <job_name>

    jcl add <job_name>          Create new job
    jcl cancel <job_name>       Cancel job run for the day
    jcl edit <job_name>         Edit job settings
    jcl kill <job_name>         Kill running job
    jcl redo <job_name>         Redo failed job
    jcl remove <job_name>       Remove/delete job
    jcl reset <job_name>        Reset job status for the day
    jcl run <job_name>          Run job for the day
    jcl show <job_name>         Show job settings
"""
    print(help_text)


class Job:
    def __init__(self, name, create=False):
        self.name = name
        if create:
            if os.path.exists(self.fpath):
                raise ValueError('"%s" already exists (%s)' % (name, self.fpath))
        else:
            if not os.path.exists(self.fpath):
                raise ValueError('"%s" not found (%s)' % (name, self.fpath))
        self._settings = None

    @property
    def command(self):
        return self.settings['command']

    @command.setter
    def command(self, new_val):
        self.settings['command'] = new_val

    @property
    def fpath(self):
        return '/'.join([config.home, 'procs', self.name + '.json'])

    def remove(self):
        os.remove(self.fpath)

    def save(self):
        d = os.path.dirname(self.fpath)
        os.makedirs(d, exist_ok=True)
        with open(self.fpath, 'w') as fp:
            fp.write(json.dumps(self.settings, indent=4))

    @property
    def settings(self):
        if self._settings is None:
            if not os.path.exists(self.fpath):
                d = os.path.dirname(self.fpath)
                os.makedirs(d, exist_ok=True)
                with open(self.fpath, 'w') as fp:
                    fp.write(json.dumps({}))
            with open(self.fpath, 'r') as fp:
                self._settings = json.load(fp)
        return self._settings

    @settings.setter
    def settings(self, new_val):
        self._settings = new_val


def job_add(args):
    if not args:
        print('Missing job name')
        return job_help()
    name = args[0]
    print('JCL add: "%s"' % name)
    job = Job(name, create=True)
    job.command = input('Command: ')
    job.save()
    print('Added: %s' % job.fpath)


def job_remove(args):
    if not args:
        print('Missing job name')
        return job_help()
    name = args[0]
    print('JCL remove: "%s"' % name)
    job = Job(name)
    job.remove()
    print('Removed: %s' % job.fpath)


def job_show(args):
    if not args:
        print('Missing job name')
        return job_help()
    name = args[0]
    print('JCL show: "%s"' % name)
    job = Job(name)
    print('File path: %s' % job.fpath)
    print(json.dumps(job.settings, indent=4))


fn_map = {
    'add': job_add,
    'cancel': None,
    'edit': None,
    'help': job_help,
    'kill': None,
    'redo': None,
    'remove': job_remove,
    'reset': None,
    'run': None,
    'show': job_show,
}


def process_args(args):
    if not args:
        return job_help()
    verb = args[0]
    if verb not in fn_map:
        print('JCL job: unrecognized verb "%s"' % verb)
        return job_help()
    if fn_map[verb] is None:
        return print('JCL job: "%s" not implemented yet' % verb)
    fn_map[verb](args[1:])