# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.MacroCmd import MacroCmd


class MacroStoreRes(MacroCmd):
    def __init__(self, data):
        MacroCmd.__init__(self, 'DISPLAY', GenericCmd.DIRECTION['RES'])
        if len(data) < 2:
            data = [0] * 2

        self.__index = int(data[0])
        self.__max = int(data[1])

    @property
    def index(self):
        return self.__index

    @property
    def max(self):
        return self.__max

    @property
    def sdu(self):
        return [self.command, self.index >> 8, self.index & 0xff, self.max >> 8, self.max & 0xff]

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                'INDEX': self.index,
                'MAX': self.max
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %04X %d\n' % ('index', VDELIM, self.index, self.index)
        s += '%-20s%c %04X %d' % ('max', VDELIM, self.max, self.max)

        return s
