# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.GpioCmd import GpioCmd
from commander.utilities.longs import bytes_to_uint32


class GpioInd(GpioCmd):
    """
    gpio indication
    """

    def __init__(self, command):
        GpioCmd.__init__(self, GenericCmd.DIRECTION['IND'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) < 6:
            print('payload empty')
            payload += [0xff] * (6 - len(payload))

        self.__function = payload[0]
        self.__identifier = payload[1]
        self.__timestamp = bytes_to_uint32(payload[2:6])

    @property
    def function(self):
        return self.__function

    @property
    def identifier(self):
        return self.__identifier

    @property
    def timestamp(self):
        return self.__timestamp

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                'FUNCTION': self.str_field(self.function, GpioCmd.FUNCTION),
                'IDENTIFIER': self.identifier,
                'TIMESTAMP': self.timestamp,
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  self.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %s' % ('function', VDELIM, self.function,
                                  GenericCmd.str_field(self.function, GpioCmd.FUNCTION))
        s += '\n'
        s += '%-20s%c %02X GPIO%d' % ('identifier', VDELIM, self.identifier,
                                      self.identifier)
        s += '\n'
        s += '%-20s%c %08X %d' % ('timestamp', VDELIM, self.timestamp,
                                  self.timestamp)
        return s
