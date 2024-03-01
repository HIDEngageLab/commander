# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.control.PowerCmd import PowerCmd


class PowerCfm(PowerCmd):
    """
    power confirmation
    """

    def __init__(self, command):
        PowerCmd.__init__(self, GenericCmd.DIRECTION['CFM'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) < 2:
            print('payload empty')
            payload = [0xff, 0xff]

        self.__result = payload[0]
        self.__function = payload[1]

    @property
    def result(self):
        return self.__result

    @property
    def function(self):
        return self.__function

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                'RESULT': GenericCmd.str_field(self.result, PowerCmd.RESULT),
                'FUNCTION': GenericCmd.str_field(self.function, PowerCmd.FUNCTION),
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s\n' % ('result', VDELIM, self.result,
                                    GenericCmd.str_field(self.result, PowerCmd.RESULT))
        s += '%-20s%c %02X %s' % ('function', VDELIM, self.function,
                                  GenericCmd.str_field(self.function, PowerCmd.FUNCTION))
        return s
