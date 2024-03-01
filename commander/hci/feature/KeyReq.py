# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.KeyCmd import KeyCmd


class KeyReq(KeyCmd):
    def __init__(self, data):
        KeyCmd.__init__(self, GenericCmd.DIRECTION['REQ'])

        if data[0] == data[-1] and data[0] in ["'", "\""]:

            if (len(data) - 2) > GenericCmd.MAX_PAYLOAD_LEN - 1:
                raise Exception('KeyReq: data too long, max: %d' %
                                GenericCmd.MAX_PAYLOAD_LEN)

            self.__data = [byte for byte in bytes(data[1:-1], 'utf-8')]

        else:
            data = data.replace(',', ' ').replace(
                '0x', ' ').replace(' ', '').strip()
            if (len(data) / 2) > GenericCmd.MAX_PAYLOAD_LEN - 1:
                raise Exception('KeyReq: data too long, max: %d' %
                                GenericCmd.MAX_PAYLOAD_LEN)

            self.__data = [int('%c%c' % (data[i], data[i + 1]), 16)
                           for i in range(0, (len(data) >> 1) << 1, 2)]

    @property
    def sdu(self):
        return [self.command] + self.__data

    @property
    def data(self):
        return self.__data

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % (
            'command', VDELIM, self.command, self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %s' % ('data', VDELIM, ''.join('%02X' %
                             byte for byte in self.__data))
        return s
