# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.control.TargetBootCmd import TargetBootCmd


class TargetBootReq(TargetBootCmd):
    """
    Target boot request

    syntax:
        <ALIAS[, ALIAS[...]]|all> target boot <START|STOP>

        START           set the boot state (push boot button)
        STOP            release the boot state (boot button)
    """

    def __init__(self, func):
        TargetBootCmd.__init__(self, GenericCmd.DIRECTION['REQ'])

        self.__function = TargetBootCmd.FUNCTION[func.upper()]

    @property
    def sdu(self):
        return [self.command, self.__function]

    @property
    def function(self):
        return self.__function

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s' % ('function', VDELIM, self.__function,
                                  GenericCmd.str_field(self.__function, TargetBootCmd.FUNCTION))
        return s
