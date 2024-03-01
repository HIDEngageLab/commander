# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.control.StatusCmd import StatusCmd


class StatusReq(StatusCmd):
    def __init__(self, func):
        StatusCmd.__init__(self, GenericCmd.DIRECTION['REQ'])

        self.__function = StatusCmd.FUNCTION[func.upper()]
        self.__sdu = [self.command, self.__function]

    @property
    def function(self):
        return self.__function

    @property
    def sdu(self):
        return self.__sdu

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s' % ('function', VDELIM, self.__function,
                                  GenericCmd.str_field(self.__function, StatusCmd.FUNCTION))

        return s
