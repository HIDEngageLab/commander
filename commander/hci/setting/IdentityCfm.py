# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.setting.IdentityCmd import IdentityCmd


class IdentityCfm(IdentityCmd):
    """
    identity confirmation
    """

    def __init__(self, command):
        IdentityCmd.__init__(self, GenericCmd.DIRECTION['CFM'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) == 0:
            print('payload empty')
            payload = [0] * 10

        self.__result = payload[0]
        self.__part = payload[1]
        self.__value = payload[2:]

    @property
    def result(self):
        return self.__result

    @property
    def part(self):
        return self.__part

    @property
    def value(self):
        return self.__value

    @GenericCmd.fields.getter
    def fields(self):
        command = self.str_command(self.command, GenericCmd.COMMANDS, '_')
        if self.part == IdentityCmd.PART['SERIAL']:
            identity_fields = {
                command:  {
                    'RESULT': self.str_field(self.result, IdentityCmd.RESULT),
                    self.str_field(self.part, IdentityCmd.PART): ''.join(['%02X ' % byte for byte in self.value])
                }
            }
        elif self.part == IdentityCmd.PART['PLATFORM']:
            identity_fields = {
                command:  {
                    'RESULT': self.str_field(self.result, IdentityCmd.RESULT),
                    self.str_field(self.part, IdentityCmd.PART): {
                        'MAINTAINER': self.value[0] >> 4,
                        'HARDWARE': (self.value[0] >> 2) & 0x03,
                        'PROTOCOL': (self.value[0] >> 0) & 0x03,
                        'IDENTIFIER': (self.value[1] << 8) + self.value[2],
                        'REVISION': self.value[3],
                    }
                }
            }
        else:
            identity_fields = {
                command:  {
                    'VALUE': ''.join(['%02X ' % byte for byte in self.value])
                }
            }
        return identity_fields

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % (
            'command', VDELIM, self.command, GenericCmd.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s\n' % ('result', VDELIM, self.result,
                                    self.str_field(self.result, IdentityCmd.RESULT))
        s += '%-20s%c %02X %s\n' % ('identity', VDELIM, self.part,
                                    self.str_field(self.part, IdentityCmd.PART))
        if self.part == IdentityCmd.PART['SERIAL']:
            s += '%-20s%c %s' % ('serial', VDELIM,
                                 ''.join('%02X ' % byte for byte in self.value))
        elif self.part == IdentityCmd.PART['PLATFORM']:
            s += '%-20s%c %02X\n' % ('maintainer', VDELIM, self.value[0] >> 4)
            s += '%-20s%c %02X\n' % ('hardware', VDELIM,
                                     (self.value[0] >> 2) & 0x03)
            s += '%-20s%c %02X\n' % ('protocol', VDELIM,
                                     (self.value[0] >> 2) & 0x03)
            hw_id = (self.value[1] << 8) + self.value[2]
            s += '%-20s%c %04X\n' % ('hw id', VDELIM, hw_id)
            s += '%-20s%c %02X' % ('hw revision', VDELIM, self.value[3])
        return s
