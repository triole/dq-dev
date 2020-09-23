import os
import pickle
import re
from os.path import join as pj

import requests
import yaml

from py.colours import Colours
from py.util import ptable


def read_yaml(filename):
    with open(filename, 'r') as stream:
        try:
            return(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)


class ReqCheck():
    def __init__(self, base_url="http://localhost:9280"):
        self.col = Colours()
        self.scriptname = os.path.realpath(__file__)
        self.scriptdir = '/'.join(self.scriptname.split('/')[:-1])
        self.urls = {}
        self.urls['base'] = base_url
        self.urls['login'] = '/accounts/login/'
        self.cred = {}
        self.cred['user'] = 'admin'
        self.cred['pass'] = 'admin'
        self.req = {}
        self.req['headers'] = (
            'User-Agent: Mozilla/5.0 ' +
            '(X11; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'
        )
        self.session = requests.session()
        self.conf = read_yaml(
            pj(self.scriptdir, 'py', 'testconf', 'request_test.yaml')
        )

    def save_cookies(self):
        with open('/tmp/dqreqcheck.tmp', 'wb') as f:
            pickle.dump(self.session.cookies, f)

    def request(self, url):
        return self.session.get(self.urls['base'] + url)

    def assert_page(self, url, rx):
        t = self.request(url)
        return bool(re.search(rx, t.text))

    def assert_all(self):
        tab = []
        for el in self.conf:
            if self.assert_page(el['url'], el['exp']) is True:
                line = [self.col.gre('[good]'), el['url'], el['exp']]
            else:
                line = [self.col.red('[fail]'), el['url'], el['exp']]
            tab.append(line)
        return tab


if __name__ == '__main__':
    rq = ReqCheck()
    res = rq.assert_all()
    ptable(['result', 'url', 'expectation'], res)
