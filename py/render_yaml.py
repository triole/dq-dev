import argparse
import os
import re
import sys
from os.path import join as pj

from lib.env import gather_env
from lib.util import appendx, expand_vars, is_git, read_yaml, write_yaml
from lib.port import gather_ports
from lib.volume import gather_volumes, valid_volume

scriptname = os.path.realpath(__file__)
scriptdir = '/'.join(scriptname.split('/')[:-1])
basedir = re.search('.*(?=/)', scriptdir).group(0)

cend = '\033[0m'
cwarn = '\033[91m'
cyel = '\033[93m'

parser = argparse.ArgumentParser(
    description=os.path.basename(__file__).title() + ': ' +
    'description of what this is',
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument('config_file', nargs='?', default='conf.yaml', help='config file to read')
args = parser.parse_args()


def read_config():
    conf_file = pj(basedir, args.config_file)
    if os.path.isfile(conf_file) is False:
        print('Can not find "' + conf_file + '"')
        sys.exit(1)
    print('Read config file ' + cyel + conf_file + cend)
    conf = read_yaml(conf_file)
    return conf


if __name__ == '__main__':
    conf = read_config()
    dyaml = read_yaml(pj(scriptdir, 'dc_template.yaml'))

    env = gather_env(conf)
    ports = gather_ports(conf)
    volumes = gather_volumes(conf)

    dyaml['volumes'] = {}
    for vol in volumes:
        t = {}
        t['driver_opts'] = vol['driver_opts']
        dyaml['volumes'][vol['name']] = t

    for ser in dyaml['services']:
        dyaml['services'][ser]['environment'] = []
        for e in env:
            try:
                f = env[ser]
            except KeyError:
                pass
            else:
                dyaml['services'][ser]['environment'] = f

        for p in ports:
            dyaml['services'][p]['ports'] = ports[p]

        dyaml['services'][ser]['volumes'] = []
        for vol in volumes:
            if valid_volume(vol, required_git=vol['required_git']) is True:

                dyaml['services'][ser]['volumes'].append(
                    vol['name'] + ':' + vol['mp']
                )

                if vol['required_git'] is True and vol['name'] == 'dq_source':
                    dyaml['services']['daiquiri']['environment'] = appendx(
                        'DQSOURCE=' + vol['mp'],
                        dyaml['services']['daiquiri']['environment']
                    )

                if vol['required_git'] is True and vol['name'] != 'dq_source':
                    dyaml['services']['daiquiri']['environment'] = appendx(
                        'DQAPP=' + vol['mp'],
                        dyaml['services']['daiquiri']['environment']
                    )

    write_yaml(dyaml, pj(basedir, 'docker-compose.yaml'))
