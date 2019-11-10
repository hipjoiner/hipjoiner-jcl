import shlex
import sys

from hipjoiner.jcl.config import config


def entry_point(line=None):
    if line is not None:
        args = normalize_args(line)
    else:
        args = normalize_args(sys.argv)
    process_args(args)


def main_help(args):
    help_text = """
Usage:  jcl [<command>] [args] [options]

    // General
    help                    Show help
    tail                    Watch master log of process events

    // Configuration
    config                  Show config information
    set <tag>=<value>       Set config tag
    unset tag               Remove config tag

    // JCL Master management
    master status           Show whether jcl master is running (& other info)
    master start            Start jcl master running
    master stop             Stop master
    master install          Install master as Windows service
    master uninstall        Uninstall Windows service
    
    // All processes
    list                    Show status of all processes
    
    // Process creation/editing
    add <proc>              Create a process by name
    edit <proc>             Edit process by name
    remove <proc>           Remove process by name
    
    // Run management
    run <proc>              Kick off process
    redo <proc>             Restart failed process
    cancel <proc>           Cancel process (for today)
    kill <proc>             Kill running process and mark as failed
    reset <proc>            Reset process status for today
    
    // Options
    --date <yyyymmdd>|-<n>  Address process run for specific date (default: today)
    --tail                  Watch master log of process events
"""
    print(help_text)


def normalize_args(cmd_line_args):
    """Normalize input command.
      Whether expressed as single line of text or array, return array of arguments.
      """
    if not cmd_line_args:
        return ['help']
    if isinstance(cmd_line_args, list):
        args = cmd_line_args
    elif isinstance(cmd_line_args, tuple):
        args = list(cmd_line_args)
    elif isinstance(cmd_line_args, str):
        args = shlex.split(cmd_line_args)
    else:
        raise ValueError('Bad datatype "%s" passed to normalize_args; must be string, list or tuple' % type(cmd_line_args))
    return args[1:]


fn_map = {
    'help':     main_help,
    'tail':     None,
    'config':   None,
    'set':      None,
    'unset':    None,
    'master':   None,
    'list':     None,
    'add':      None,
    'edit':     None,
    'remove':   None,
    'run':      None,
    'redo':     None,
    'cancel':   None,
    'kill':     None,
    'reset':    None,
}


def process_args(args):
    if not args:
        main_help(args)
        exit(0)
    verb = args[0]
    if verb not in fn_map:
        print('Unrecognized verb: "%s"' % verb)
        main_help(args)
    elif fn_map[verb] is None:
        print('Verb: "%s" -- not implemented yet' % verb)
    else:
        fn_map[verb](args)


if __name__ == '__main__':
    entry_point('jcl help')
