import argparse
import os
import re
import sys
from os.path import join as pj

import yaml

scriptname = os.path.realpath(__file__)
scriptdir = '/'.join(scriptname.split('/')[:-1])
basedir = re.search('.*(?=/)', scriptdir).group(0)

parser = argparse.ArgumentParser(
    description=os.path.basename(__file__).title() + ': ' +
    'description of what this is',
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument('config_file', nargs='?', default='conf.yaml', help='config file to read')
args = parser.parse_args()


def read_yaml(filename):
    with open(filename, 'r') as stream:
        try:
            return(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)


def save_yaml(data, filename):
    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, indent=4)


def make_volume(name, device):
    vol = {}
    device = replace_vars(device)
    if os.path.isdir(device) is False:
        print(
            'Run without volume \"' + name +
            '\". Path on host does not exist \"' + device + '\"'
        )
    else:
        vol['driver_opts'] = {}
        vol['driver_opts']['device'] = replace_vars(device)
        vol['driver_opts']['o'] = 'bind'
        vol['driver_opts']['type'] = 'none'
        vol['name'] = name
    return vol


def add_volume(vol, serv):
    try:
        serv['volumes']
    except KeyError:
        serv['volumes'] = []
    try:
        mountpoint = conf['active_volumes'][vol['name']]
    except KeyError:
        mountpoint = conf['active_app']['mountpoint']
    try:
        vol_entry = vol['name'] + ':' + replace_vars(mountpoint)
    except KeyError:
        pass
    else:
        serv['volumes'].append(vol_entry)
    return serv


def replace_vars(str):
    return str.replace('<HOME>', os.environ['HOME'])


if __name__ == '__main__':
    conf_file = pj(basedir, args.config_file)
    if os.path.isfile(conf_file) is False:
        print('Can not find "' + conf_file + '"')
        sys.exit(1)
    print('Read config file ' + conf_file)
    conf = read_yaml(conf_file)
    yd = read_yaml(pj(scriptdir, 'dc_template.yaml'))

    # add volumes to volume list
    yd['volumes'] = {}
    for volname in conf['active_volumes']:
        volpath = conf['active_volumes'][volname]
        yd['volumes'][volname] = make_volume(volname, conf['folders'][volname])

    yd['volumes']['dq_app'] = make_volume(
        'dq_app', conf['folders'][conf['active_app']['name']]
    )

    # add volumes to services
    for s in yd['services']:
        serv = yd['services'][s]
        for v in yd['volumes']:
            try:
                vol = yd['volumes'][v]
            except KeyError:
                pass
            else:
                yd['services'][s] = add_volume(vol, serv)

    save_yaml(yd, pj(basedir, 'docker-compose.yaml'))
