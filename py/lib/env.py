def gather_env(conf):
    env = {}
    for e in conf['env']:
        env[e] = conf['env'][e]
    return env
