import os
from lib.util import expand_vars, is_git

def gather_volumes(conf):
    vols = []
    for volname in conf['docker_volume_mountpoints']:
        vol = {}
        vol['driver_opts'] = {}
        vol['driver_opts']['o'] = 'bind'
        vol['driver_opts']['type'] = 'none'
        vol['mp'] = conf['docker_volume_mountpoints'][volname]
        vol['required_git'] = volname.startswith('dq_')
        if volname == 'dq_app':
            volname = conf['active_app']
        vol['name'] = volname
        vol['driver_opts']['device'] = expand_vars(
            conf['folders_on_host'][volname]
        )
        vols.append(vol)
    return vols


def valid_volume(invol, required_git=False):
    r = False
    dev = invol['driver_opts']['device']
    is_dir = os.path.isdir(dev)

    if is_dir is False and required_git is False:
        print(
            'Run without volume \"' + invol['name'] +
            '\". Path on host does not exist \"' + dev + '\"'
        )

    if is_dir is True:
        r = True

    if required_git is True:
        ig = is_git(dev)
        if ig[0] is False:
            print(
                cwarn +
                '\nFolder ' + cyel + dev + cwarn +
                ' does not look like a git repo.\n' +
                'Please make sure that it really contains the source of ' +
                cyel + invol['name'] + cend + '\n'
            )
            sys.exit(1)
        else:
            r = True
    return r
