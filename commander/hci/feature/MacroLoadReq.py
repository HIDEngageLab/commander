# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.MacroCmd import MacroCmd


class MacroLoadReq(MacroCmd):
    def __init__(self, _data):
        # Attention: the command parameter are for the upload session
        MacroCmd.__init__(self, 'MACRO_LOAD', GenericCmd.DIRECTION['REQ'])

        if len(_data) == 0:
            print(__file__, __name__, 'empty payload')
            _data = [0]

        self.__max = int(_data[0])

    @property
    def sdu(self):
        sdu_data = [self.command, self.max >> 8, self.max & 0xff]
        return sdu_data

    @property
    def max(self):
        return self.__max

    @max.setter
    def max(self, _value):
        self.__max = _value

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %04X %d\n' % ('max', VDELIM, self.max, self.max)

        return s
