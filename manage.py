#!/usr/bin/python3
import argparse
import os

from py.colours import Colours
from py.dcompose import DCompose
from py.init import init
from py.profile import Profile
from py.runner import Runner
from py.util import pprint

parser = argparse.ArgumentParser(
    description=os.path.basename(__file__).title() + ': ' +
    'dq-dev, daiquiri docker compose dev setup',
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument(
    '-r', '--run', type=str, nargs='*', default=None,
    help='run a profile\'s containers'
)
parser.add_argument(
    '-p', '--stop', type=str, nargs='*', default=None,
    help='stop profile\'s running containers'
)
parser.add_argument(
    '-d', '--down', type=str, nargs='*', default=None,
    help=(
        'stop and remove profile\'s running containers, ' +
        'remove docker\'s volumes, keep folders containing the ' +
        'volume data, they can be reused on next run'
    )
)
parser.add_argument(
    '-rmi', '--remove_images', action='store_true', default=False,
    help='remove images when running "down", used in combination "-d -rmi"\n\n'
)
parser.add_argument(
    '-g', '--tail_logs', type=str, nargs='*', default=None,
    help='tail docker compose logs\n\n'
)
parser.add_argument(
    '-c', '--create_profile', type=str, default=None,
    help='create a new profile with the default settings'
)
parser.add_argument(
    '-s', '--set_profile', type=str, default=None,
    help='set profile to active'
)
parser.add_argument(
    '-e', '--render', type=str, nargs='*', default=None,
    help='only render docker-compose.yaml for profile'
)
parser.add_argument(
    '-a', '--display_profile', type=str, nargs='*', default=None,
    help='display currently active profile'
)
parser.add_argument(
    '-l', '--list_profiles', action='store_true', default=False,
    help='list all available profiles'
)
parser.add_argument(
    '-n', '--dry_run', action='store_true', default=False,
    help=(
        'do not run any docker-compose commands nor ' +
        'save rendered docker-compose.yaml, just print them'
    )
)
args = parser.parse_args()


if __name__ == '__main__':
    col = Colours()
    conf = init(args)
    prof = Profile(conf)
    dco = DCompose(conf, prof)
    pprint(conf)
    if args.list_profiles is True:
        prof.list()

    if args.create_profile is not None:
        prof.create(args.create_profile)

    if args.set_profile is not None:
        prof.set(args.set_profile)

    if args.display_profile is not None:
        c = prof.read_profile_config(conf['args']['display_profile'])
        print(
            'Currently set profile',
            col.yel(c['name'])
        )
        pprint(c)

    if args.render is not None:
        dco.render_dc_yaml(conf['args']['render'])
        dco.render_dockerfile_templates()

    if args.run is not None:
        dco.render_dc_yaml(conf['args']['run'])
        dco.render_dockerfile_templates()
        run = Runner(
            prof.get_profile_yaml_by_name(conf['args']['run']),
            args.dry_run
        )
        run.start()

    if args.stop is not None:
        run = Runner(
            prof.get_profile_yaml_by_name(conf['args']['stop']),
            args.dry_run
        )
        run.stop()

    if args.down is not None:
        run = Runner(
            prof.get_profile_yaml_by_name(conf['args']['down']),
            args.dry_run
        )
        run.down(args.remove_images)

    if args.tail_logs is True:
        run = Runner(prof.get_profile_conf_by_name(conf['args']['tail_logs']))
        run.tail_logs()
