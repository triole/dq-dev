from lib.util import appendx

def gather_env(conf):
    env = {}
    for e in conf['env']:
        env[e] = conf['env'][e]

    for p in conf['exposed_ports']['daiquiri']:
        s = "EXPOSED_PORT=" + p.split(':')[0]
        env['daiquiri'] = appendx(s, env['daiquiri'])
    return env
