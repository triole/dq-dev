def gather_ports(conf):
    ports = {}
    for k in conf['exposed_ports']:
        p = conf['exposed_ports'][k]
        ports[k] = conf['exposed_ports'][k]
    return ports
