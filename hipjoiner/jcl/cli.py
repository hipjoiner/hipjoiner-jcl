import shlex
import sys

from hipjoiner.jcl import config
from hipjoiner.jcl import job
from hipjoiner.jcl import master


def cli_help(args):
    help_text = """
Usage:  jcl [<command>] [args] [options]

    // General
    help                        Show help
    tail                        Watch master log of events

    // Configuration
    config list                 Show config information
    config set <tag>=<value>    Set config tag
    config unset tag            Remove config tag

    // Master management
    master status               Show whether master is running (& other info)
    master start                Start master running
    master stop                 Stop master
    master install              Install master as Windows service
    master uninstall            Uninstall Windows service
    
    // Job info
    list                        Show all jobs
    show <job>                  Show job attributes
    tail <job>                  Watch live job output

    // Job editing
    add <job>                   Create a job by name
    edit <job>                  Edit job by name
    remove <job>                Remove job by name

    // Run management
    run <job>                   Kick off job
    redo <job>                  Restart failed job
    cancel <job>                Cancel job (for today)
    kill <job>                  Kill running job and mark as failed
    reset <job>                 Reset job status for today
    
    // Options
    --date <yyyymmdd>|-<n>      Address job run for specific date (default: today)
    --tail                      Watch master log of job events
"""
    print(help_text)


def entry_point(cmd_line=sys.argv):
    args = normalize_args(cmd_line)
    process_args(args[1:])


def normalize_args(cmd_line_args):
    """Normalize input command.
      Whether expressed as single line of text or array, return array of arguments
      (less first arg, i.e. the executable invoking jcl)
      """
    if not cmd_line_args:
        return []
    if isinstance(cmd_line_args, list):
        args = cmd_line_args
    elif isinstance(cmd_line_args, tuple):
        args = list(cmd_line_args)
    elif isinstance(cmd_line_args, str):
        args = shlex.split(cmd_line_args)
    else:
        raise ValueError('Bad datatype "%s"; must be string, list or tuple' % type(cmd_line_args))
    return args


def tail_route(args):
    if len(args) == 1:
        master.process_args(args)
    else:
        job.process_args(args)


fn_map = {
    'config':   config.process_args,
    'help':     cli_help,
    'list':     job.process_args,
    'master':   master.process_args,
    'add':      job.process_args,
    'edit':     job.process_args,
    'remove':   job.process_args,
    'run':      job.process_args,
    'redo':     job.process_args,
    'cancel':   job.process_args,
    'kill':     job.process_args,
    'reset':    job.process_args,
    'show':     job.process_args,
    'tail':     tail_route,
}


def process_args(args):
    if not args:
        return cli_help(args)
    verb = args[0]
    if verb not in fn_map:
        print('JCL: unrecognized verb "%s"' % verb)
        return cli_help(args)
    fn_map[verb](args)


if __name__ == '__main__':
    # entry_point('jcl help')
    # entry_point('jcl config')
    # entry_point('jcl add')
    entry_point('jcl tail')
