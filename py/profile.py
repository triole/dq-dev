from os.path import exists as ex
from os.path import join as pj
from shutil import copyfile as cp
from sys import exit as x

from py.lib.colours import Colours
from py.lib.util import (find, mkdir, path_up_to_last_slash, read_yaml,
                         write_yaml)


class Profile():
    def __init__(self, conf):
        self.conf = conf
        self.c = Colours()

    def active_name(self, profname=None):
        r = None
        if profname is not None:
            return profname
        else:
            yaml_file = self.conf['prof']['active_conf']
            try:
                k = read_yaml(yaml_file)
                r = k['active_profile_name']
            except (FileNotFoundError, KeyError):
                pass
            return r

    def create(self, str):
        tfol = pj(self.conf['prof']['basedir'], str)
        if ex(tfol) is True:
            print(
                'Please check ' + self.c.yel(self.conf['prof']['basedir']) +
                '\nProfile ' + self.c.yel(str) + ' already seems to exist. '
            )
        else:
            mkdir(tfol)
            cp(self.conf['conf']['template'], pj(tfol, 'conf.yaml'))
            print(
                'Fresh profile ' + self.c.yel(str) + ' created inside of folder ' +
                self.c.yel(tfol)
            )

    def set(self, str):
        p = {}
        p['active_profile_name'] = str
        write_yaml(p, self.conf['prof']['active_conf'])

    def get(self, profname=None):
        n = self.active_name(profname)
        if n is None:
            print(
                'Unable to detect active profile. Either set one or use ' +
                'the command line arg.'
            )
            x(1)
        r = {}
        f = find(
            self.conf['prof']['basedir'],
            n + r'.*conf.yaml$',
            'f'
        )
        if len(f) < 1:
            print(
                'Please check ' + self.c.yel(self.conf['prof']['basedir']) +
                '\nSet profile ' + self.c.yel(n) + ' does not seem to exist. '
            )
            x(1)
        if len(f) > 1:
            print(
                'Please check ' + self.c.yel(self.conf['prof']['basedir']) +
                '\nMultiple profiles matched: '
            )
            for el in f:
                print('\t' + el)
            x(1)
        r['name'] = n
        r['yaml'] = f[0]
        r['folder'] = path_up_to_last_slash(f[0])
        r['dc_yaml'] = pj(r['folder'], 'docker-compose.yaml')
        return r
