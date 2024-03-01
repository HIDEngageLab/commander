# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.MacroCmd import MacroCmd


class MacroLoadCfm(MacroCmd):
    """
    macro data upload confirmation
    """

    def __init__(self, command):
        MacroCmd.__init__(self, 'MACRO_LOAD', GenericCmd.DIRECTION['CFM'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) < 5:
            print('payload empty')
            payload += [0] * (5 + len(payload))

        self.__result = payload[0]
        from commander.utilities.floats import convert_to_float
        self.__memory = convert_to_float(payload[1:])

    @property
    def result(self):
        return self.__result

    @property
    def memory(self):
        return self.__memory

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                'RESULT': self.str_field(self.result, MacroCmd.RESULT),
                'MEMORY': self.memory,
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s\n' % ('result', VDELIM, self.result,
                                    self.str_field(self.result, MacroCmd.RESULT))
        from commander.utilities.floats import convert_to_long
        s += '%-20s%c %04X (%5.2f%% free)' % ('memory',
                                              VDELIM, convert_to_long(self.memory), self.memory)

        return s
