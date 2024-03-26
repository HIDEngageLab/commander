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
        self.__function = payload[1]
        self.__part = payload[2]
        self.__value = payload[3:]

    @property
    def result(self):
        return self.__result

    @property
    def function(self):
        return self.__function

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
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  GenericCmd.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %s' % ('result', VDELIM, self.result,
                                  self.str_field(self.result, IdentityCmd.RESULT))
        s += '\n'
        s += '%-20s%c %02X %s' % ('function', VDELIM, self.function,
                                  self.str_field(self.function, IdentityCmd.FUNCTION))
        s += '\n'
        s += '%-20s%c %02X %s' % ('part', VDELIM, self.part,
                                  self.str_field(self.part, IdentityCmd.PART))

        if self.part == IdentityCmd.PART['FIRMWARE']:
            firmware = (self.value[0] << 8) + (self.value[1] << 0)
            revision = (self.value[2] << 8) + (self.value[3] << 0)
            patch = (self.value[4] << 8) + (self.value[5] << 0)
            build = (self.value[6] << 8) + (self.value[7] << 0)
            vendor = (self.value[8] << 8) + (self.value[9] << 0)
            s += '\n'
            s += '%-20s%c %04X %d' % ('firmware', VDELIM,
                                      firmware, firmware)
            s += '\n'
            s += '%-20s%c %04X %d' % ('revision', VDELIM,
                                      revision, revision)
            s += '\n'
            s += '%-20s%c %04X %d' % ('patch', VDELIM,
                                      patch, patch)
            s += '\n'
            s += '%-20s%c %04X %d' % ('build', VDELIM,
                                      build, build)
            s += '\n'
            s += '%-20s%c %04X %d ' % ('vendor', VDELIM,
                                       vendor, vendor)
        elif self.part == IdentityCmd.PART['HARDWARE']:
            maintainer = (self.value[0] << 8) + (self.value[1] << 0)
            hardware = (self.value[2] << 8) + (self.value[3] << 0)
            s += '\n'
            s += '%-20s%c %04X %d' % ('maintainer', VDELIM,
                                      maintainer, maintainer)
            s += '\n'
            s += '%-20s%c %04X %d' % ('hardware', VDELIM,
                                      hardware, hardware)
            s += '\n'
            s += '%-20s%c %02X %d' % ('number', VDELIM,
                                      self.value[4], self.value[4])
            s += '\n'
            s += '%-20s%c %02X %d' % ('variant', VDELIM,
                                      self.value[5], self.value[5])
        elif self.part == IdentityCmd.PART['PLATFORM']:
            s += '\n'
            s += '%-20s%c %s' % ('platform', VDELIM,
                                 ''.join('%c' % byte for byte in self.value))
        elif self.part == IdentityCmd.PART['PRODUCT']:
            s += '\n'
            s += '%-20s%c %s' % ('product', VDELIM,
                                 ''.join('%c' % byte for byte in self.value))
        elif self.part == IdentityCmd.PART['SERIAL']:
            s += '\n'
            s += '%-20s%c %s' % ('serial', VDELIM,
                                 ''.join('%02X ' % byte for byte in self.value))

        elif self.part == IdentityCmd.PART['UNIQUE']:
            s += '\n'
            s += '%-20s%c %02X' % ('unique', VDELIM,
                                   (self.value[2] << 24) +
                                   (self.value[3] << 16) +
                                   (self.value[4] << 8) +
                                   (self.value[5] << 0))
        return s
