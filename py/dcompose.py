import os
import re
from os.path import join as pj
from sys import exit as x

from py.colours import Colours
from py.util import (find, is_git, mkdir, pprint, rxbool, rxsearch,
                     write_array_to_file, write_yaml)


class DCompose():
    def __init__(self, conf, prof):
        self.c = Colours()
        self.conf = conf
        self.prof = prof
        self.dcyaml = {}
        self.profconf = {}
        self.names = {}
        self.volumes = []

    def expand_vars_arr(self, arr):
        for i, el in enumerate(arr):
            arr[i] = self.expand_vars(arr[i])
        return arr

    def expand_vars(self, str):
        return str\
            .replace('<HOME>', os.environ['HOME'])\
            .replace('<CONTAINER_PGAPP>', self.nam_con('pgapp'))\
            .replace('<CONTAINER_PGDATA>', self.nam_con('pgdata'))\
            .replace('<CONTAINER_WPDB>', self.nam_con('wpdb'))\
            .replace('<UID>', self.conf['user']['idstr'])\
            .replace('<GID>', self.conf['user']['groupstr'])

    # service and container names
    def make_names(self):
        for service in self.profconf['conf']['env']:
            self.names[service] = {}
            self.names[service]['con'] =\
                'dqdev' + '-' + service + '-' + self.profconf['name']
            self.names[service]['img'] =\
                'dqdev' + '_' + service + '_' + self.profconf['name']

    def nam_img(self, service):
        return self.names[service]['img']

    def nam_con(self, service):
        return self.names[service]['con']

    def nam_daiq(self):
        for service in self.names:
            img = self.nam_img(service)
            if 'daiquiri' in img:
                return img
        return None

    def container_enabled(self, container_name):
        try:
            return self.profconf['conf']['enable_containers'][container_name]
        except KeyError:
            return False

    # template
    def make_template(self):
        self.dcyaml['version'] = '3.7'
        self.dcyaml['services'] = {}
        self.dcyaml['volumes'] = {}

        for service in self.profconf['conf']['env']:
            if self.container_enabled(service) is True:
                c = self.nam_img(service)
                self.dcyaml['services'][c] = {}
                self.dcyaml['services'][c]['build'] = {}
                self.dcyaml['services'][c]['build']['context'] =\
                    '../../../docker/' + service
                self.dcyaml['services'][c]['container_name'] =\
                    self.nam_con(service)
                self.dcyaml['services'][c]['restart'] = 'always'

    # depends on
    def add_depends_on(self):
        self.dcyaml['services'][self.nam_daiq()]['depends_on'] = []
        for service in self.dcyaml['services']:
            if 'daiquiri' not in service:
                self.dcyaml['services'][self.nam_daiq()]['depends_on']\
                    .append(service)

    # env
    def add_env(self):
        for service in self.profconf['conf']['env']:
            env = self.expand_vars_arr(self.profconf['conf']['env'][service])

            try:
                exposed_ports = self.profconf['conf']['exposed_ports'][service]
            except KeyError:
                pass
            if exposed_ports is not None:
                p = exposed_ports[0].split(':')[0]
                env.append('EXPOSED_PORT=' + str(p))

            for mp in self.profconf['conf']['docker_volume_mountpoints']:
                key = ''.join(re.findall('[A-Z0-9]', mp.upper()))
                val = self.profconf['conf']['docker_volume_mountpoints'][mp]
                env.append(key + '=' + val)
            # try because exception occurs when a container is disabled
            try:
                self.dcyaml['services'][self.nam_img(service)]['environment'] = env
            except KeyError:
                pass

    # ports
    def add_ports(self):
        for service in self.profconf['conf']['exposed_ports']:
            try:
                p =\
                    self.profconf['conf']['exposed_ports'][service]
            except KeyError:
                pass
            if p is None:
                p = []
            # same as in the last lines of add_env
            try:
                self.dcyaml['services'][self.nam_img(service)]['ports'] = p
            except KeyError:
                pass

    # volumes
    def add_volumes(self):
        for vol in self.volumes:
            self.dcyaml['volumes'][vol['name']] = {}
            self.dcyaml['volumes'][vol['name']]['driver_opts'] =\
                vol['driver_opts']

        for service in self.dcyaml['services']:
            self.dcyaml['services'][service]['volumes'] = []

            for vol in self.volumes:
                if rxbool(vol['mount_inside'], service) is True:
                    self.dcyaml['services'][service]['volumes'].append(
                        vol['name'] + ':' + vol['mp']
                    )

    def make_volumes(self):
        vols = []
        for volname in self.profconf['conf']['docker_volume_mountpoints']:
            try:
                fol = self.profconf['conf']['folders_on_host'][volname]
            except KeyError:
                fol = self.profconf['conf']['folders_on_host'][
                    self.profconf['conf']['active_app']
                ]
            v = self.make_volume(
                volname + '_' + self.profconf['name'],
                self.profconf['conf']['docker_volume_mountpoints'][volname],    # noqa: E501
                fol,
                volname.startswith('dq_')
            )
            if self.valid_volume(v) is True:
                vols.append(v)

        for volname in self.profconf['conf']['enable_database_volumes']:
            if self.profconf['conf']['enable_database_volumes'][volname] is True:   # noqa: E501
                volfolder = pj(
                    self.prof.get_profile_folder_by_name(
                        self.profconf['name']
                    ),
                    volname
                )
                mkdir(volfolder)
                mp = '/var/lib/mysql'
                if volname.startswith('pg'):
                    mp = '/var/lib/postgresql/data'
                vols.append(
                    self.make_volume(
                        volname + '_' + self.profconf['name'],
                        mp,
                        volfolder,
                        mount_inside=volname
                    )
                )
        self.volumes = vols

    def make_volume(
        self, volname, mp, folder_on_host,
        required_git=False, mount_inside='.*'
    ):
        vol = {}
        vol['name'] = volname
        vol['mp'] = mp
        vol['required_git'] = required_git
        vol['mount_inside'] = mount_inside
        vol['driver_opts'] = {}
        vol['driver_opts']['o'] = 'bind'
        vol['driver_opts']['type'] = 'none'
        vol['driver_opts']['device'] = self.expand_vars(folder_on_host)
        return vol

    def valid_volume(self, vol):
        r = False
        dev = vol['driver_opts']['device']
        is_dir = os.path.isdir(dev)

        if is_dir is False and vol['required_git'] is False:
            print(
                'Run without volume ' + self.c.yel(vol['name']) +
                '. Path does not exist on host ' + self.c.yel(dev)
            )

        if is_dir is True:
            r = True

        if vol['required_git'] is True:
            ig = is_git(dev)
            if ig[0] is False:
                print(
                    '\n' + self.c.err() + 'Folder ' + self.c.yel(dev) +
                    ' does not look like a git repo. ' +
                    '\nPlease make sure that it contains the source of ' +
                    self.c.yel(vol['name']) + '\n'
                )
                x(1)
            else:
                r = True
        return r

    def write_yaml(self):
        if self.conf['dry_run'] is True:
            print(self.c.yel('\nDry run, dc yaml would look like this:'))
            pprint(self.dcyaml)
        else:
            print(
                'Write dc yaml to ' +
                self.c.yel(self.profconf['dc_yaml'])
            )
            write_yaml(self.dcyaml, self.profconf['dc_yaml'])

    def render_dockerfile_templates(self):
        arr = find(self.conf['basedir'], '.*/dockerfile.tpl', 'f')
        for fn in arr:
            print('Render dockerfile template ' + self.c.yel(fn))
            self.render_template_file(fn)

    def render_template_file(self, filename):
        new_filename = rxsearch(r'.*(?=\.)', filename)
        r = []
        try:
            filecontent = open(filename, 'r')
        except Exception as e:
            raise(e)
        else:
            for line in filecontent.read().splitlines():
                r.append(self.expand_vars(line))
        write_array_to_file(r, new_filename)

    # main
    def render_dc_yaml(self, profname=None):
        self.profconf = self.prof.read_profile_config(profname)

        self.make_names()
        self.make_template()
        self.make_volumes()

        self.add_depends_on()
        self.add_env()
        self.add_ports()
        self.add_volumes()

        self.write_yaml()
