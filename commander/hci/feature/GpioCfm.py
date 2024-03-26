# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.GpioCmd import GpioCmd


class GpioCfm(GpioCmd):
    """
    gpio confirmation
    """

    def __init__(self, command):
        GpioCmd.__init__(self, GenericCmd.DIRECTION['CFM'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) < 3:
            print('payload empty')
            payload = [0] * (3 - len(payload))

        self.__result = payload[0]
        self.__function = payload[1]
        self.__identifier = payload[2]

    @property
    def result(self):
        return self.__result

    @property
    def function(self):
        return self.__function

    @property
    def identifier(self):
        return self.__identifier

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                'RESULT': GenericCmd.str_field(self.result, GpioCmd.RESULT),
                'FUNCTION': GenericCmd.str_field(self.function, GpioCmd.FUNCTION),
                'IDENTIFIER': self.identifier,
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  GenericCmd.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %s' % ('result', VDELIM, self.result,
                                  GenericCmd.str_field(self.result, GpioCmd.RESULT))
        s += '\n'
        s += '%-20s%c %02X %s' % ('function', VDELIM, self.function,
                                  GenericCmd.str_field(self.function, GpioCmd.FUNCTION))
        s += '\n'
        s += '%-20s%c %02X GPIO%d' % ('identifier', VDELIM, self.identifier,
                                      self.identifier)
        return s
