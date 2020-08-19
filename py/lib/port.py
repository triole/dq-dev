def gather_ports(conf):
    ports = {}
    for k in conf['exposed_ports']:
        try :
            p = conf['exposed_ports'][k]
        except KeyError:
            p = []
        else:
            if p is None:
                p = []
        ports[k] = p
    return ports
