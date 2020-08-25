import json
import os
import re
from os.path import join as pj
from os.path import sep as sep
from subprocess import PIPE, Popen
from sys import exit as x

import yaml


def appendx(val, arr):
    if val not in arr:
        arr.append(val)
    return arr


def expand_vars(str, replace_list=[]):
    r = str.replace('<HOME>', os.environ['HOME'])
    for el in replace_list:
        r = r.replace(el[0], el[1])
    return r


def find(root, filter='.*', filter_type='f'):
    detected = []
    for (path, dirs, files) in os.walk(root):
        if files and filter_type == 'f':
            for filename in files:
                rfn = pj(path, filename)
                if bool(re.search(filter, rfn)) is True:
                    detected.append(rfn)
        elif dirs and filter_type == 'd':
            for dirname in dirs:
                rdir = pj(path, dirname)
                if bool(re.search(filter, rdir)) is True:
                    detected.append(rdir)
    return(sorted(detected))


def run_cmd(cmd, silent=True, debug=False):
    o = ''
    if debug is False:
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, close_fds=True)
        (out, err) = proc.communicate()
        exitcode = proc.wait()
        if exitcode != 0:
            print(err.decode('utf-8'))
            return (False, None)
            x()
        o = out.decode('utf-8')
        if silent is False:
            print(o)
    else:
        print(' '.join(cmd))
    return o


def is_git(folder):
    proc = Popen(
        ['git', '-C', folder, 'remote', '-v'],
        stdout=PIPE, stderr=PIPE, close_fds=True
    )
    (out, err) = proc.communicate()
    exitcode = proc.wait()
    if exitcode != 0:
        return (False, None)
    out = out.splitlines()[0].decode('utf-8')
    out = re.search(r'git.*?\s', out).group(0)
    return (True, out)


def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def read_yaml(filename):
    with open(filename, 'r') as stream:
        try:
            return(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)


def write_yaml(data, filename):
    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, indent=4)


def rxsearch(rx, s, gr=0):
    r = None
    m = re.search(rx, s, flags=re.IGNORECASE)
    if bool(m) is True:
        r = m.group(gr)
    return r


def path_after_last_slash(s):
    return rxsearch('[^' + sep + ']+$', s)


def path_up_to_last_slash(s):
    return rxsearch('.*(?=\\' + sep + ')', s)


def pprint(jdata):
    if type(jdata) == str:
        jdata = json.dumps(jdata)
    print(json.dumps(jdata, sort_keys=True, indent=4))
