import os
import re

from py.colours import Colours
from py.util import run_cmd


class Runner():
    def __init__(self, dcyaml, debug=True):
        self.c = Colours()
        self.dcyaml = dcyaml
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
        return '-f ' + self.dcyaml + ' '

    def dc(self, args):
        self.run_cmd_fg(
            self.sudo() + 'docker-compose ' + self.dcf() + args
        )

    # docker compose commands
    def start(self):
        self.dc('up --build -d')
        self.tail_logs()

    def stop(self):
        self.dc('stop')

    def down(self, rmi):
        cmd = 'down --volumes --remove-orphans'
        if rmi is True:
            cmd += ' --rmi all'
        self.dc(cmd)

    def tail_logs(self):
        self.dc('logs -f')

    def remove_images(self):
        self.dc('down --volume')
