# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.GpioCmd import GpioCmd


class GpioReq(GpioCmd):
    def __init__(self, _identifier, _function):
        GpioCmd.__init__(self, GenericCmd.DIRECTION['REQ'])

        self.__identifier = _identifier if isinstance(_identifier, int) \
            else int(_identifier, 10)
        assert self.__identifier < 4, 'wrong pin number'

        function = _function.upper().strip()
        if GenericCmd.find_field(function, GpioCmd.FUNCTION):
            self.__function = GpioCmd.FUNCTION[function]
        else:
            raise Exception('unknown function')

    @property
    def function(self):
        return self.__function

    @property
    def identifier(self):
        return self.__identifier

    @property
    def sdu(self):
        return [self.command, self.function, self.identifier]

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  self.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %s' % ('function', VDELIM, self.function,
                                  GenericCmd.str_field(self.function, GpioReq.FUNCTION))
        s += '\n'
        s += '%-20s%c %02X GPIO%d' % ('identifier', VDELIM, self.identifier,
                                      self.identifier)
        return s
