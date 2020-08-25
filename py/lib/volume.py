import os
from os.path import join as pj
from sys import exit as x

from py.lib.util import expand_vars, is_git, mkdir


def make_volume(volname, mp, folder_on_host, required_git=False, mount_inside='.*'):
    vol = {}
    vol['name'] = volname
    vol['mp'] = mp
    vol['required_git'] = required_git
    vol['mount_inside'] = mount_inside
    vol['driver_opts'] = {}
    vol['driver_opts']['o'] = 'bind'
    vol['driver_opts']['type'] = 'none'
    vol['driver_opts']['device'] = expand_vars(folder_on_host)
    return vol


def gather_volumes(conf, prof):
    vols = []
    for volname in conf['docker_volume_mountpoints']:
        vn = volname
        if volname == 'dq_app':
            volname = conf['active_app']
        vols.append(
            make_volume(
                volname,
                conf['docker_volume_mountpoints'][vn],
                conf['folders_on_host'][volname],
                vn.startswith('dq_')
            )
        )
    for volname in conf['enable_database_volumes']:
        if conf['enable_database_volumes'][volname] is True:
            volfolder = pj(prof['folder'], volname)
            mkdir(volfolder)
            mp = '/var/lib/mysql'
            if volname.startswith('pg'):
                mp = '/var/lib/postgresql/data'
            vols.append(
                make_volume(
                    volname,
                    mp,
                    volfolder,
                    mount_inside=volname
                )
            )
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
                '\nFolder "' + dev + '" ' +
                ' does not look like a git repo.\n' +
                'Please make sure that it really contains the source of' +
                ' "' + invol['name'] + '"' + '\n'
            )
            x(1)
        else:
            r = True
    return r
