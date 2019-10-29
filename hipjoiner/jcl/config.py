from functools import lru_cache
import json
import os


class Config:
    def __init__(self):
        pass

    def __str__(self):
        return self.list()

    @property
    def config_fpath(self):
        return os.path.sep.join([self.jcl_appdata, 'config.json'])

    def defaults(self):
        return {
            'home': os.path.sep.join([self.user_home, 'jcl']),
        }

    def delete(self, tag):
        self.file_data.pop(tag)
        self.save()

    @property
    @lru_cache()
    def file_data(self):
        if not os.path.isfile(self.config_fpath):
            os.makedirs(self.jcl_appdata, exist_ok=True)
            data = self.defaults()
            self.save(data)
        with open(self.config_fpath, 'r') as fp:
            data = json.load(fp)
        return data

    def help(self):
        return '\n'.join([
            'Usage: jcl config <command> [args]',
            '',
            'Commands:',
            '    delete <tag>         Remove tag from config info',
            '    list                 Show config info',
            '    set <tag> <value>    Set tag=value in config info',
        ])

    @property
    def jcl_appdata(self):
        return os.path.sep.join([self.user_appdata, 'jcl'])

    @property
    def jcl_home(self):
        return self.file_data['home']

    def list(self):
        lines = ['Config (%s):' % self.config_fpath]
        lines += ['  %s: %s' % (tag, val) for tag, val in self.file_data.items()]
        lines += [
            '',
            'Immutables:',
            '  User home:       %s' % self.user_home,
            '  User appdata:    %s' % self.user_appdata,
            '  Tasknet appdata: %s' % self.jcl_appdata,
            '  Tasknet config:  %s' % self.config_fpath,
        ]
        return '\n'.join(lines)

    def process(self, args=None):
        if not args:
            print(self.help())
        elif args[0] == 'list':
            print(self)
        elif args[0] == 'set':
            if len(args) != 3:
                print('Bad set syntax')
                print(self.help())
            else:
                self.set(args[1], args[2])
        elif args[0] == 'delete':
            if len(args) != 2:
                print('Bad delete syntax')
                print(self.help())
            else:
                self.delete(args[1])
        else:
            print('Unrecognized argument(s) "%s"' % ' '.join(args))
            print(self.help())

    def save(self, data=None):
        if data is None:
            data = self.file_data
        with open(self.config_fpath, 'w') as fp:
            json.dump(data, fp, indent=4)

    def set(self, tag, value):
        self.file_data[tag] = value
        self.save()

    @property
    def user_appdata(self):
        return os.environ.get('APPDATA')

    @property
    def user_home(self):
        return os.environ.get('USERPROFILE')


config = Config()


if __name__ == '__main__':
    config.process()
