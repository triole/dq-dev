import os
from os.path import join as pj

from py.lib.util import mkdir


def init(args):
    conf = {}
    n = os.path.realpath(__file__)
    basedir = '/'.join(n.split('/')[:-3])
    conf['basedir'] = basedir
    conf['args'] = {}
    conf['args']['run'] = parse_nargs(args.run)
    conf['args']['render'] = parse_nargs(args.render)
    conf['args']['display_profile'] = parse_nargs(args.display_profile)
    conf['args']['tail_logs'] = parse_nargs(args.tail_logs)
    conf['prof'] = {}
    conf['prof']['basedir'] = pj(basedir, 'usr', 'profiles')
    conf['prof']['active_conf'] = pj(conf['prof']['basedir'], 'active.yaml')
    conf['templ'] = {}
    conf['templ']['config'] = pj(basedir, 'py', 'tpl', 'conf.yaml')
    conf['templ']['dc'] = pj(basedir, 'py', 'tpl', 'dc_template.yaml')
    conf['dry_run'] = args.dry_run
    mkdir(conf['prof']['basedir'])
    return conf


def parse_nargs(nargs):
    if isinstance(nargs, list):
        if len(nargs) < 1:
            return None
        else:
            return nargs[0]
    return None
