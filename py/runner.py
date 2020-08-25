import os
import re

from py.lib.colours import Colours
from py.lib.util import run_cmd


class Runner():
    def __init__(self, profconf, debug=True):
        self.c = Colours()
        self.profconf = profconf
        self.debug = debug

    def run_cmd_fg(self, cmd):
        print(self.c.mag(cmd))
        if self.debug is False:
            os.system(cmd)

    def sudo(self):
        g = run_cmd(['groups'])
        if bool(re.search('docker', g)) is True:
            return ''
        else:
            return 'sudo '

    def dcf(self):
        return '-f ' + self.profconf['dc_yaml'] + ' '

    def dc(self, args):
        self.run_cmd_fg(
            self.sudo() + 'docker-compose ' + self.dcf() + args
        )

    # docker compose commands
    def start(self):
        self.dc('up --build -d')
        self.tail_logs()

    def down(self):
        self.dc('down --verbose')

    def tail_logs(self):
        self.dc('logs -f')
