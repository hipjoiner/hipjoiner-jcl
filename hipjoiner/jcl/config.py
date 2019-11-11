import json
import os


class Config:
    @staticmethod
    def config_help():
        help_text = """
Usage: jcl config [list|set|unset] [<args>]

    jcl config list                 Show settings
    jcl config set <tag>=<value>    Set tag/value pair
    jcl config unset <tag>          Remove tag setting
        """
        print(help_text)

    def __init__(self):
        self._settings = None

    @property
    def appdata(self):
        return '/'.join([self.user_appdata, 'jcl'])

    @property
    def config_fpath(self):
        return '/'.join([self.appdata, 'config.json'])

    @property
    def defaults(self):
        return {
            'home': '/'.join([self.user_home, 'jcl']),
        }

    @property
    def home(self):
        return self.settings['home']

    def info(self, args):
        lines = ['Settings:']
        lines += ['  %s: %s' % (tag, val) for tag, val in self.settings.items()]
        lines += [
            '',
            'Config file:',
            '  %s' % self.config_fpath,
        ]
        info_text = '\n'.join(lines)
        print(info_text)

    def save(self):
        with open(self.config_fpath, 'w') as fp:
            json.dump(self.settings, fp, indent=4)

    def set(self, args):
        if not args or len(args) > 2:
            return self.config_help()
        norm_args = args
        if len(args) == 1:
            norm_args = args[0].split('=')
        if len(norm_args) != 2:
            return self.config_help()
        self.settings[norm_args[0]] = norm_args[1]
        print('%s = %s' % (norm_args[0], norm_args[1]))
        self.save()

    @property
    def settings(self):
        if self._settings is None:
            if not os.path.isfile(self.config_fpath):
                os.makedirs(self.appdata, exist_ok=True)
                self._settings = self.defaults
                self.save()
            with open(self.config_fpath, 'r') as fp:
                self._settings = json.load(fp)
        return self._settings

    @settings.setter
    def settings(self, new_val):
        self._settings = new_val

    def unset(self, args):
        if not args or len(args) > 1:
            return self.config_help()
        self.settings.pop(args[0])
        print('"%s" removed ' % args[0])
        self.save()

    @property
    def user_appdata(self):
        if os.name == 'nt':
            return os.environ.get('APPDATA').replace('\\', '/')
        raise OSError('Bad OS "%s"; not yet implemented' % os.name)

    @property
    def user_home(self):
        if os.name == 'nt':
            return os.environ.get('USERPROFILE').replace('\\', '/')
        raise OSError('Bad OS "%s"; not yet implemented' % os.name)


config = Config()


fn_map = {
    'list': config.info,
    'set': config.set,
    'unset': config.unset,
}


def process_args(args):
    if len(args) <= 1:
        return config.config_help()
    verb = args[1]
    if verb not in fn_map:
        print('JCL: Unrecognized verb "%s"' % verb)
        config.config_help()
    elif fn_map[verb] is None:
        print('JCL: "%s" not implemented yet' % verb)
    else:
        fn_map[verb](args[1:])


if __name__ == '__main__':
    # process_args(['list'])
    # process_args(['set', 'bleh=hi'])
    process_args(['unset', 'bleh'])
