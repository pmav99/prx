#!/usr/bin/env python

from cleo import Application as BaseApplication

from .match_command import MatchCommand
from .sub_command import SubCommand

from .. import __version__


class Application(BaseApplication):
    def __init__(self):
        super(Application, self).__init__("prx", __version__)

        for command in self.get_default_commands():
            self.add(command)

    def get_default_commands(self) -> list:
        commands = [MatchCommand(), SubCommand()]
        return commands
