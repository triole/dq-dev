import sys
from os.path import join as pj

from py.lib.colours import Colours
from py.lib.util import find, path_up_to_last_slash, read_yaml, write_yaml


class Profile():
    def __init__(self, conf):
        self.conf = conf
        self.c = Colours()

    def active_profile(self):
        y = read_yaml(self.conf['prof_conf'])
        return y['active_profile']

    def set_profile(self, str):
        p = {}
        p['active_profile'] = str
        write_yaml(p, self.conf['prof_conf'])

    def get_profile(self):
        n = self.active_profile()
        r = {}
        f = find(
            self.conf['prof_dir'],
            n + r'.*.yaml$',
            'f'
        )
        if len(f) < 1:
            print(
                'Set profile ' + self.c.yel(n) + ' does not seem to exist. ' +
                'Please check ' + self.c.yel(self.conf['prof_dir'])
            )
            sys.exit(1)
        if len(f) > 1:
            print(
                'Multiple profiles matched. ' +
                'Please check ' + self.conf['prof_dir']
            )
            sys.exit(1)
        r['name'] = n
        r['yaml'] = f[0]
        r['folder'] = path_up_to_last_slash(f[0])
        r['dc_target'] = pj(r['folder'], 'docker-compose.yaml')
        return r
