import shlex
import sys

from hipjoiner.jcl.config import config


def cli_help(args):
    help_text = """
Usage:  jcl [<command>] [args] [options]

    // General
    help                        Show help
    tail                        Watch master log of process events

    // Configuration
    config list                 Show config information
    config set <tag>=<value>    Set config tag
    config unset tag            Remove config tag

    // JCL Master management
    master status               Show whether jcl master is running (& other info)
    master start                Start jcl master running
    master stop                 Stop master
    master install              Install master as Windows service
    master uninstall            Uninstall Windows service
    
    // All processes
    list                        Show status of all processes
    
    // Process creation/editing
    add <proc>                  Create a process by name
    edit <proc>                 Edit process by name
    remove <proc>               Remove process by name
    
    // Run management
    run <proc>                  Kick off process
    redo <proc>                 Restart failed process
    cancel <proc>               Cancel process (for today)
    kill <proc>                 Kill running process and mark as failed
    reset <proc>                Reset process status for today
    
    // Options
    --date <yyyymmdd>|-<n>      Address process run for specific date (default: today)
    --tail                      Watch master log of process events
"""
    print(help_text)


def entry_point(cmd_line=sys.argv):
    args = normalize_args(cmd_line)
    process_args(args)


fn_map = {
    'config':   config.process_args,
    'help':     cli_help,
    'list':     None,
    'master':   None,
    'tail':     None,

    'add':      None,
    'edit':     None,
    'remove':   None,
    'run':      None,
    'redo':     None,
    'cancel':   None,
    'kill':     None,
    'reset':    None,
}


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
        raise ValueError('Bad datatype "%s" passed to normalize_args; must be string, list or tuple' % type(cmd_line_args))
    return args[1:]


def process_args(args):
    if not args:
        cli_help(args)
        exit(0)
    verb = args[0]
    if verb not in fn_map:
        print('Unrecognized verb: "%s"' % verb)
        cli_help(args)
    elif fn_map[verb] is None:
        print('Verb: "%s" -- not implemented yet' % verb)
    else:
        fn_map[verb](args[1:])


if __name__ == '__main__':
    # entry_point('jcl help')
    entry_point('jcl config')
