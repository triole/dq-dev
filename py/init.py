import os
from os.path import join as pj

from py.util import mkdir


def init(args):
    conf = {}
    n = os.path.realpath(__file__)
    basedir = '/'.join(n.split('/')[:-2])
    conf['basedir'] = basedir
    conf['args'] = {}
    conf['args']['down'] = parse_nargs(args.down)
    conf['args']['render'] = parse_nargs(args.render)
    conf['args']['run'] = parse_nargs(args.run)
    conf['args']['stop'] = parse_nargs(args.stop)
    conf['args']['display_profile'] = parse_nargs(args.display_profile)
    conf['args']['tail_logs'] = parse_nargs(args.tail_logs)
    conf['prof'] = {}
    conf['prof']['basedir'] = pj(basedir, 'usr', 'profiles')
    conf['prof']['active_conf'] = pj(conf['prof']['basedir'], 'active.yaml')
    conf['templ'] = {}
    conf['templ']['config'] = pj(basedir, 'tpl', 'conf.yaml')
    conf['templ']['dc'] = pj(basedir, 'py', 'tpl', 'dc_template.yaml')
    conf['dry_run'] = args.dry_run
    conf['user'] = {}
    conf['user']['id'] = os.getuid()
    conf['user']['idstr'] = str(conf['user']['id'])
    conf['user']['group'] = get_group(conf['user']['id'])
    conf['user']['groupstr'] = str(conf['user']['group'])
    mkdir(conf['prof']['basedir'])
    return conf


def parse_nargs(nargs):
    if isinstance(nargs, list):
        if len(nargs) < 1:
            return None
        else:
            return nargs[0]
    return None


def get_group(user_id):
    groups = os.getgroups()
    if user_id in groups:
        return user_id
    else:
        return groups[len(groups)-1]
