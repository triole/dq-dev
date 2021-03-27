import argparse
import os
import re
from os.path import join as pj

import requests

import fixpath  # noqa
from colours import Colours
from util import ptable, read_yaml


class ReqCheck():
    def __init__(self, conffile):
        self.conf = read_yaml(conffile)
        self.col = Colours()
        self.req = {}
        self.req['headers'] = {
            'user-agent': self.conf['ua']
        }
        self.s_in = self.session_login()
        self.s_out = requests.Session()

    def get(self, url, login=False):
        rqu = self.conf['urls']['base'] + url
        if login is False:
            return self.s_out.get(rqu, headers=self.req['headers'])
        else:
            return self.s_in.get(rqu, headers=self.req['headers'])

    def post(self, url, data=None, login=False):
        rqu = self.conf['urls']['base'] + url
        if login is False:
            return self.s_out.post(rqu, data=data, headers=self.req['headers'])
        else:
            return self.s_in.post(rqu, data=data, headers=self.req['headers'])

    def assert_page(self, url, rx, login=False):
        try:
            t = self.get(url, login)
        except requests.exceptions.ConnectionError:
            return [self.col.red('[fail]'), login, url, rx]
        else:
            b = bool(re.search(rx, t.text))
            if b is True:
                return [self.col.gre('[good]'), login, url, rx]
            else:
                return [self.col.red('[fail]'), login, url, rx]

    def assert_source(self, src, rx):
        return bool(re.search(rx, src))

    def assert_all(self):
        tab = []
        for el in self.conf['request_check']:
            tab.append(self.assert_page(el['url'], el['exp_out'], login=False))
            tab.append(self.assert_page(el['url'], el['exp_in'], login=True))
            if el['url'].endswith('/'):
                rqu = el['url'][:-1]
                tab.append(self.assert_page(rqu, el['exp_out'], login=False))
                tab.append(self.assert_page(rqu, el['exp_in'], login=True))
        tab = sorted(tab, key=lambda x: (x[1], x[2]))
        return tab

    def session_login(self):
        sess = requests.Session()
        src = sess.get(self.conf['urls']['base'] + '/accounts/login/')
        formtoken = re.search(
            r'(csrfmiddlewaretoken.*value=")([a-zA-Z0-9]+)', src.text
        ).group(2)
        csrftoken = sess.cookies['csrftoken']
        login_data = {
            'login': self.conf['cred']['user'],
            'password': self.conf['cred']['pass'],
            'csrfmiddlewaretoken': csrftoken,
            'csrftoken': formtoken,
            'next': '/query/'
        }
        src = sess.post(
            self.conf['urls']['base'] + self.conf['urls']['login'],
            data=login_data,
            headers=self.req['headers']
        )
        if bool(re.search(r'If you forgot your password', src.text)) is True:
            print(
                self.col.red('\nLogin failed. Please check your login data\n')
            )
        return sess

    def logout(self):
        self.post(self.conf['urls']['logout'])


if __name__ == '__main__':
    scriptname = os.path.realpath(__file__)
    scriptdir = '/'.join(scriptname.split('/')[:-1])
    conffile = pj(scriptdir, 'testconf', 'request_test.yaml')

    parser = argparse.ArgumentParser(
        description=os.path.basename(__file__).title() + ': ' +
        'Daiquiri request checker',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-c', '--config', type=str, default=conffile,
        help='configuration file to use'
    )
    args = parser.parse_args()

    rq = ReqCheck(args.config)
    res = rq.assert_all()
    ptable(['result', 'login', 'url', 'expectation'], res)

    rq.logout()
