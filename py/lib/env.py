from py.lib.util import appendx, expand_vars


def gather_env(conf, profname):
    env = {}

    expand_list = [['<PROFILE_NAME>', profname]]

    for e in conf['env']:
        for i, f in enumerate(conf['env'][e]):
            conf['env'][e][i] = expand_vars(f, expand_list)
        env[e] = conf['env'][e]

    for p in conf['exposed_ports']['daiquiri']:
        s = "EXPOSED_PORT=" + p.split(':')[0]
        env['daiquiri'] = appendx(s, env['daiquiri'])
    return env
