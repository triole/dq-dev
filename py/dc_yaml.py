import os
import sys

from py.lib.colours import Colours
from py.lib.env import gather_env
from py.lib.port import gather_ports
from py.lib.util import appendx, pprint, read_yaml, write_yaml
from py.lib.volume import gather_volumes, valid_volume


class DCYaml():
    def __init__(self, conf, prof):
        self.c = Colours()
        self.conf = conf
        self.prof = prof
        self.dyaml = read_yaml(self.conf['templ']['dc'])
        self.dyaml['volumes'] = {}

    def get_yaml_template(self, profile):
        yaml = profile['yaml']
        if os.path.isfile(yaml) is False:
            print('Can not find "' + yaml + '"')
            sys.exit(1)
        print('Read config file ' + self.c.yel(yaml))
        conf = read_yaml(yaml)
        return conf

    def render_dc_yaml(self, profname=None):
        gp = self.prof.get(profname)
        conf = self.get_yaml_template(gp)
        print('Render dc yaml to ' + self.c.yel(gp['dc_yaml']))

        env = gather_env(conf)
        ports = gather_ports(conf)
        volumes = gather_volumes(conf)

        for vol in volumes:
            t = {}
            t['driver_opts'] = vol['driver_opts']
            self.dyaml['volumes'][vol['name']] = t

        for ser in self.dyaml['services']:
            self.dyaml['services'][ser]['container_name'] =\
                self.dyaml['services'][ser]['container_name'] + '_' + gp['name']

            self.dyaml['services'][ser]['environment'] = []
            for e in env:
                try:
                    f = env[ser]
                except KeyError:
                    pass
                else:
                    self.dyaml['services'][ser]['environment'] = f

            for p in ports:
                self.dyaml['services'][p]['ports'] = ports[p]

            self.dyaml['services'][ser]['volumes'] = []
            for vol in volumes:
                if valid_volume(vol, required_git=vol['required_git']) is True:

                    self.dyaml['services'][ser]['volumes'].append(
                        vol['name'] + ':' + vol['mp']
                    )

                    if vol['required_git'] is True and vol['name'] == 'dq_source':
                        self.dyaml['services']['daiquiri']['environment'] = appendx(
                            'DQSOURCE=' + vol['mp'],
                            self.dyaml['services']['daiquiri']['environment']
                        )

                    if vol['required_git'] is True and vol['name'] != 'dq_source':
                        self.dyaml['services']['daiquiri']['environment'] = appendx(
                            'DQAPP=' + vol['mp'],
                            self.dyaml['services']['daiquiri']['environment']
                        )

        if self.conf['dry_run'] is True:
            print(self.c.yel('\nDry run, dc yaml would look like this:'))
            pprint(self.dyaml)
        else:
            write_yaml(self.dyaml, gp['dc_yaml'])
