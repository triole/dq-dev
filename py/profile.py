from os.path import exists as ex
from os.path import join as pj
from shutil import copyfile as cp
from sys import exit as x

from py.colours import Colours
from py.util import (find, mkdir, path_up_to_last_slash, pprint, read_yaml,
                     rxsearch, write_yaml)


class Profile():
    def __init__(self, conf):
        self.conf = conf
        self.c = Colours()

    def create(self, profname):
        if self.profile_exist(profname) is True:
            print(
                'Please check ' + self.c.yel(self.conf['prof']['basedir']) +
                '\nProfile ' + self.c.yel(profname) +
                ' already seems to exist.'
            )
        else:
            mkdir(self.get_profile_folder_by_name(profname))
            cp(
                self.conf['templ']['config'],
                self.get_profile_conf_by_name(profname)
            )
            print(
                'Fresh profile ' + self.c.yel(profname) +
                ' created inside of folder ' +
                self.c.yel(self.get_profile_folder_by_name(profname))
            )

    def set(self, profname):
        if self.profile_exist(profname) is False:
            print(
                'Unable to set. Profile ' + self.c.yel(profname) +
                ' does not seem to exist'
            )
        else:
            print(
                'Set active profile ' + self.c.yel(profname)
            )
            p = {}
            p['active_profile_name'] = profname
            write_yaml(p, self.conf['prof']['active_conf'])

    def read_profile_config(self, profname=None):
        n = self.get_active_profile_name(profname)
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
        r['conf'] = read_yaml(r['yaml'])
        return r

    def list(self):
        print(self.c.yel('The following profiles are available'))
        arr = find(self.conf['prof']['basedir'], r'.*.conf.yaml$', 'f')
        for el in arr:
            shortname = rxsearch(r'[^/]+/[^/]+$', el)
            profname = rxsearch(r'.*(?=\/)', shortname)
            print('\n' + self.c.mag(profname))
            pprint(self.read_profile_config(profname))

    # utility
    def get_profile_folder_by_name(self, profname):
        return pj(
            self.conf['prof']['basedir'],
            self.get_active_profile_name(profname)
        )

    def get_profile_conf_by_name(self, profname):
        return pj(self.get_profile_folder_by_name(profname), 'conf.yaml')

    def get_profile_yaml_by_name(self, profname):
        return pj(
            self.get_profile_folder_by_name(profname), 'docker-compose.yaml'
        )

    def profile_exist(self, profname):
        return ex(self.get_profile_folder_by_name(profname))

    def get_active_profile_name(self, profname=None):
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
