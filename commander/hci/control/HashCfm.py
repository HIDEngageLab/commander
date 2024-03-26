# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.control.HashCmd import HashCmd


class HashCfm(HashCmd):
    """
    hash value (XMODEM CRC-16) confirmation
    """

    def __init__(self, command):
        HashCmd.__init__(self, GenericCmd.DIRECTION['CFM'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) == 0:
            print('payload empty')
            payload = [0] * 5

        self.__result = payload[0]
        self.__hash = \
            (payload[1] << 8) + \
            payload[2]

    @property
    def result(self):
        return self.__result

    @property
    def hash(self):
        return self.__hash

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                'RESULT': self.str_field(self.result, HashCmd.RESULT),
                'HASH': self.hash,
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s\n' % ('result', VDELIM, self.result,
                                    self.str_field(self.result, HashCmd.RESULT))
        s += '%-20s%c 0x%04X (%d)' % ('hash', VDELIM, self.hash, self.hash)
        return s
