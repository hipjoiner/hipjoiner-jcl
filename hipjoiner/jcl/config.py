import json
import os


class Config:
    def __init__(self):
        self._file_data = None
        self.fn_map = {
            'list': self.info,
            'set': None,
            'unset': None,
        }

    @property
    def appdata(self):
        return os.path.sep.join([self.user_appdata, 'jcl'])

    @property
    def config_fpath(self):
        return os.path.sep.join([self.appdata, 'config.json'])

    def config_help(self, args):
        help_text = """
            Some help.
        """
        print(help_text)

    @property
    def defaults(self):
        return {
            'home': os.path.sep.join([self.user_home, 'jcl']),
        }

    @property
    def file_data(self):
        if not self._file_data:
            if not os.path.isfile(self.config_fpath):
                os.makedirs(self.appdata, exist_ok=True)
                self._file_data = self.defaults
                self.save()
            with open(self.config_fpath, 'r') as fp:
                self._file_data = json.load(fp)
        return self._file_data

    @file_data.setter
    def file_data(self, val):
        self._file_data = val

    @property
    def home(self):
        return self.file_data['home']

    def info(self):
        lines = ['Settings:']
        lines += ['  %s: %s' % (tag, val) for tag, val in self.file_data.items()]
        lines += [
            '',
            'Immutables:',
            '  Config file:     %s' % self.config_fpath,
            '  User home:       %s' % self.user_home,
            '  User appdata:    %s' % self.user_appdata,
        ]
        info_text = '\n'.join(lines)
        print(info_text)

    def process_args(self, args):
        if not args:
            self.config_help(args)
            return
        verb = args[0]
        if verb not in self.fn_map:
            print('Unrecognized verb: "%s"' % verb)
            self.config_help(args)
        elif self.fn_map[verb] is None:
            print('Verb: "%s" -- not implemented yet' % verb)
        else:
            self.fn_map[verb](args)

    def save(self):
        with open(self.config_fpath, 'w') as fp:
            json.dump(self.file_data, fp, indent=4)

    def set(self, tag, value):
        self.file_data[tag] = value
        self.save()

    def unset(self, tag):
        self.file_data.pop(tag)
        self.save()

    @property
    def user_appdata(self):
        if os.name == 'nt':
            return os.environ.get('APPDATA')
        raise OSError('Bad OS "%s"; not yet implemented' % os.name)

    @property
    def user_home(self):
        if os.name == 'nt':
            return os.environ.get('USERPROFILE')
        raise OSError('Bad OS "%s"; not yet implemented' % os.name)


config = Config()


if __name__ == '__main__':
    config.process_args()
