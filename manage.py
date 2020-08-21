#!/usr/bin/python3
import argparse
import os
from os.path import join as pj

from py.dc_yaml import DCYaml
from py.lib.colours import Colours
from py.lib.util import mkdir, pprint
from py.profile import Profile
from py.runner import Runner

parser = argparse.ArgumentParser(
    description=os.path.basename(__file__).title() + ': ' +
    'description of what this is',
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument(
    '-r', '--run', action='store_true', default=False,
    help='run currently active profile\'s containers'
)
parser.add_argument(
    '-l', '--tail_logs', action='store_true', default=False,
    help='tail docker compose logs'
)
parser.add_argument(
    '-c', '--create_profile', type=str, default=None,
    help='create a new profile with the default settings'
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
    '-e', '--render', action='store_true', default=False,
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
    conf['prof_conf_name'] = 'profile_conf.yaml'
    conf['basedir'] = basedir
    conf['prof_conf'] = pj(basedir, conf['prof_conf_name'])
    conf['prof_basedir'] = pj(basedir, 'usr', 'profiles')
    conf['conf_template'] = pj(basedir, 'py', 'tpl', 'conf.yaml')
    conf['dc_template'] = pj(basedir, 'py', 'tpl', 'dc_template.yaml')
    conf['prof_basedir'] = pj(basedir, 'usr', 'profiles')
    mkdir(conf['prof_basedir'])
    return conf


if __name__ == '__main__':
    col = Colours()
    conf = init()
    prof = Profile(conf)
    dcy = DCYaml(conf, prof)

    if args.create_profile is not None:
        prof.create(args.create_profile)

    if args.set_profile is not None:
        prof.set(args.set_profile)

    if args.get_profile is True:
        p = prof.get()
        print(col.yel('Currently set profile'))
        pprint(p)

    if args.render is True:
        dcy.render_dc_yaml(args.dry_run)

    if args.run is True:
        run = Runner(prof.get(), args.dry_run)
        run.start()

    if args.tail_logs is True:
        run = Runner(prof.get())
        run.tail_logs()
