import argparse
import os
import re
import sys
from os.path import join as pj

from util import expand_vars, is_git, read_yaml, write_yaml

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


def gather_volumes(conf):
    vols = []
    for volname in conf['docker_volume_mountpoints']:
        vol = {}
        vol['driver_opts'] = {}
        vol['driver_opts']['o'] = 'bind'
        vol['driver_opts']['type'] = 'none'
        vol['mp'] = conf['docker_volume_mountpoints'][volname]
        vol['required_git'] = volname.startswith('dq_')
        if volname == 'dq_app':
            volname = conf['active_app']
        vol['name'] = volname
        vol['driver_opts']['device'] = expand_vars(
            conf['folders_on_host'][volname]
        )
        vols.append(vol)
    return vols


def valid_volume(invol, required_git=False):
    r = False
    dev = invol['driver_opts']['device']
    is_dir = os.path.isdir(dev)

    if is_dir is False and required_git is False:
        print(
            'Run without volume \"' + invol['name'] +
            '\". Path on host does not exist \"' + dev + '\"'
        )

    if is_dir is True:
        r = True

    if required_git is True:
        ig = is_git(dev)
        if ig[0] is False:
            print(
                cwarn +
                '\nFolder ' + cyel + dev + cwarn +
                ' does not look like a git repo.\n' +
                'Please make sure that it really contains the source of ' +
                cyel + invol['name'] + cend + '\n'
            )
            sys.exit(1)
        else:
            r = True
    return r


if __name__ == '__main__':
    conf = read_config()
    dyaml = read_yaml(pj(scriptdir, 'dc_template.yaml'))
    volumes = gather_volumes(conf)

    dyaml['volumes'] = {}
    for vol in volumes:
        t = {}
        t['driver_opts'] = vol['driver_opts']
        dyaml['volumes'][vol['name']] = t

    for ser in dyaml['services']:
        dyaml['services'][ser]['volumes'] = []
        for vol in volumes:
            if valid_volume(vol, required_git=vol['required_git']) is True:
                dyaml['services'][ser]['volumes'].append(
                    vol['name'] + ':' + vol['mp']
                )

    write_yaml(dyaml, pj(basedir, 'docker-compose.yaml'))
