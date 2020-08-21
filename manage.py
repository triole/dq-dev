#!/usr/bin/python3
import argparse
import os
from os.path import join as pj

from py.dc_yaml import DCYaml
from py.lib.colours import Colours
from py.lib.util import pprint
from py.profile import Profile

parser = argparse.ArgumentParser(
    description=os.path.basename(__file__).title() + ': ' +
    'description of what this is',
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument(
    '-s', '--set_profile', type=str, default=None,
    help='set active profile'
)
parser.add_argument(
    '-g', '--get_profile', action='store_true', default=False,
    help='print active profile settings'
)
parser.add_argument(
    '-r', '--render', action='store_true', default=False,
    help='render docker-compose.yaml for currently set profile'
)
parser.add_argument(
    '-n', '--dry_run', action='store_true', default=False,
    help='do not render docker-compose.yaml, just print it'
)
args = parser.parse_args()


def init():
    conf = {}
    n = os.path.realpath(__file__)
    basedir = '/'.join(n.split('/')[:-1])
    conf['basedir'] = basedir
    conf['prof_conf'] = pj(basedir, 'conf.yaml')
    conf['prof_dir'] = pj(basedir, 'usr', 'profiles')
    conf['dc_template'] = pj(basedir, 'py', 'tpl', 'dc_template.yaml')
    return conf


if __name__ == '__main__':
    col = Colours()
    conf = init()
    prof = Profile(conf)
    dcy = DCYaml(conf, prof)

    if args.set_profile is not None:
        prof.set_profile(args.set_profile)

    if args.get_profile is True:
        p = prof.get_profile()
        print(col.yel('Currently set profile'))
        pprint(p)

    if args.render is True:
        dcy.render_dc_yaml(args.dry_run)
