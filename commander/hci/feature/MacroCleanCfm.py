# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.MacroCmd import MacroCmd


class MacroCleanCfm(MacroCmd):
    """
    macro data storage clean confirmation
    """

    def __init__(self, command):
        MacroCmd.__init__(self, 'MACRO_CLEAN', GenericCmd.DIRECTION['CFM'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) < 1:
            print('payload empty')
            payload = [0]

        self.__result = payload[0]

    @property
    def result(self):
        return self.__result

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                'RESULT': self.str_field(self.result, MacroCmd.RESULT),
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s' % ('result', VDELIM, self.result,
                                  self.str_field(self.result, MacroCmd.RESULT))

        return s
