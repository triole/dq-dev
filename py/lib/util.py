import os
import re
from subprocess import PIPE, Popen

import yaml


def appendx(val, arr):
    if val not in arr:
        arr.append(val)
    return arr


def expand_vars(str):
    return str.replace('<HOME>', os.environ['HOME'])


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


def read_yaml(filename):
    with open(filename, 'r') as stream:
        try:
            return(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)


def write_yaml(data, filename):
    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, indent=4)
