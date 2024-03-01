# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.utilities.PrettyPrint import VDELIM


class HciStatusInd(GenericCmd):
    """
    init indication
    """

    # Generic Error
    # Cmd is invalid/unknown
    # Cmd is not supported by this firmware
    RESULT = {'SUCCESS': 0x00,
              'FAILURE': 0x01,
              'INVALID_COMMAND': 0x02,
              'UNSUPPORTED': 0x03}

    def __init__(self, command):
        GenericCmd.__init__(self, GenericCmd.COMMANDS['PROTOCOL'], GenericCmd.DIRECTION['IND'])

        payload = command[1]
        if len(payload) == 0:
            print('payload empty')
            payload = [0] * 1

        if self.command != command[0]:
            raise 'HciStatusInd: unknown command id: %04X' % command[0]

        self.__result = payload[0]
        self.__data = payload[1:]

    @property
    def result(self):
        return self.__result

    def __str__(self):
        s = ''
        s += '%-20s%c %04X %s\n' % (
            'command', VDELIM, self.command, self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %04X %s\n' % ('result', VDELIM, self.__result, self.str_field(self.__result, HciStatusInd.RESULT))
        s += '%-20s%c %s' % ('data', VDELIM, ' '.join('%02X' % byte for byte in self.__data))
        return s
