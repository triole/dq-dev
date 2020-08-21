import sys
from os.path import exists as ex
from os.path import join as pj
from shutil import copyfile as cp

from py.lib.colours import Colours
from py.lib.util import (find, mkdir, path_up_to_last_slash, read_yaml,
                         write_yaml)


class Profile():
    def __init__(self, conf):
        self.conf = conf
        self.c = Colours()

    def active_name(self):
        y = read_yaml(self.conf['prof_conf'])
        return y['active_profile_name']

    def create(self, str):
        tfol = pj(self.conf['prof_basedir'], str)
        if ex(tfol) is True:
            print(
                'Please check ' + self.c.yel(self.conf['prof_basedir']) +
                'Profile ' + self.c.yel(str) + ' already seems to exist. '
            )
        else:
            mkdir(tfol)
            cp(self.conf['conf_template'], pj(tfol, 'conf.yaml'))
            print(
                'Fresh profile ' + self.c.yel(str) + ' created inside of folder ' +
                self.c.yel(tfol)
            )

    def set(self, str):
        p = {}
        p['active_profile_name'] = str
        write_yaml(p, self.conf['prof_conf'])

    def get(self):
        n = self.active_name()
        r = {}
        f = find(
            self.conf['prof_basedir'],
            n + r'.*conf.yaml$',
            'f'
        )
        if len(f) < 1:
            print(
                'Please check ' + self.c.yel(self.conf['prof_basedir']) +
                'Set profile ' + self.c.yel(n) + ' does not seem to exist. '
            )
            sys.exit(1)
        if len(f) > 1:
            print(
                'Please check ' + self.c.yel(self.conf['prof_basedir']) +
                '\nMultiple profiles matched: '
            )
            for el in f:
                print('\t' + el)
            sys.exit(1)
        r['name'] = n
        r['yaml'] = f[0]
        r['folder'] = path_up_to_last_slash(f[0])
        r['dc_yaml'] = pj(r['folder'], 'docker-compose.yaml')
        return r
