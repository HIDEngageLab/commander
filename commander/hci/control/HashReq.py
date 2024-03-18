# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.control.HashCmd import HashCmd


class HashReq(HashCmd):
    """
    hash (XMODEM CRC-16) value calculation 
    """

    def __init__(self, _data):
        HashCmd.__init__(self, GenericCmd.DIRECTION['REQ'])

        if _data[0] == _data[-1] in ["'", "\""] and _data[0] in ["'", "\""]:
            if (len(_data) - 2) > GenericCmd.MAX_PAYLOAD_LEN - 1:
                raise Exception('KeyReq: data too long, max: %d' %
                                GenericCmd.MAX_PAYLOAD_LEN)

            self.__data = [byte for byte in bytes(_data[1:-1], 'utf-8')]

        else:
            _data = _data.replace(',', ' ')
            _data = _data.replace('0x', ' ')
            _data = _data.replace(' ', '')
            _data = _data.strip()
            if (len(_data) / 2) > GenericCmd.MAX_PAYLOAD_LEN - 1:
                raise Exception('KeyReq: data too long, max: %d' %
                                GenericCmd.MAX_PAYLOAD_LEN)

            self.__data = [int('%c%c' % (_data[i], _data[i + 1]), 16)
                           for i in range(0, (len(_data) >> 1) << 1, 2)]

    @property
    def sdu(self):
        return [self.command] + self.__data

    @property
    def data(self):
        return self.__data

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %s' % ('data', VDELIM, ''.join('%02X' %
                             byte for byte in self.__data))
        return s
