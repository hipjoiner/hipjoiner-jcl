import os
import sys

from hipjoiner.jcl.config import config


def entry():
    process_command(sys.argv[1:])


def task_help():
    return '\n'.join([
        'Usage: jcl <command> [<args>]',
        '',
        'Commands:',
        '    config        Configure jcl operation on this host',
        '    help          Show this help',
        '    list          Show tasks & info',
    ])


def normalize_entry(args):
    """Normalize input command.
      Whether expressed as single line of text or array, return array of arguments.
      """
    if not args:
        args = []
    elif type(args) == str:
        args = args.split()
    while len(args) > 0 and not args[0]:
        args = args[1:]
    return args


def process_command(args=''):
    args = normalize_entry(args)
    if len(args) == 0:
        print(task_help())
    elif args[0] == 'config':
        config.process(args[1:])
    elif args[0] == 'help':
        print(task_help())
    elif args[0] == 'list':
        print('jcl list [not yet implemented]')
    else:
        print('Unrecognized subcommand "%s"' % args[0])
        print(task_help())


def show(args):
    """For documentation-- show exact command line input"""
    fname = __file__
    print('Command: %s %s' % (fname, ' '.join(args)))
    print('')


if __name__ == '__main__':
    tests = [
        '',
        'config',
        'gurgle',
        'config list',
        'config gurgle',
        'config set',
        'config set xyz',
        'config set xyz 123',
        'config list',
    ]
    cwd = os.getcwd()
    for i, test in enumerate(tests):
        print('-' * 130)
        print('Test %d' % (i + 1))
        print('')
        print(' '.join([cwd + '>', 'task', test]))
        process_command(test)
        print('')
