# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.MacroCmd import MacroCmd


class MacroLoadInd(MacroCmd):
    """
    macro data item upload indication
    """

    def __init__(self, command):
        MacroCmd.__init__(self, 'MACRO_LOAD', GenericCmd.DIRECTION['IND'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) < 4:
            print('payload empty')
            payload += [0] * (4 - len(payload))

        self.__index = (payload[0] << 8) + payload[1]
        self.__max = (payload[2] << 8) + payload[3]

    @property
    def index(self):
        return self.__index

    @property
    def max(self):
        return self.__max

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                'INDEX': self.index,
                'MAX': self.max,
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %04X %d\n' % ('index', VDELIM,
                                    self.index, self.index)
        s += '%-20s%c %04X %d' % ('max', VDELIM, self.max, self.max)

        return s
