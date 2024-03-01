# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.setting.HardwareCmd import HardwareCmd


class HardwareCfm(HardwareCmd):
    """
    hardware revision confirmation
    """

    def __init__(self, command):
        HardwareCmd.__init__(self, GenericCmd.DIRECTION['CFM'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) < 4:
            print('payload empty')
            payload += [0xff] * (4 - len(payload))

        self.__result = payload[0]
        self.__identifier = (payload[1] << 8) + payload[2]
        self.__revision = payload[3]

    @property
    def result(self):
        return self.__result

    @property
    def identifier(self):
        return self.__identifier

    @property
    def revision(self):
        return self.__revision

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                'RESULT': self.str_field(self.result, HardwareCmd.RESULT),
                'IDENTIFIER': self.identifier,
                'REVISION': self.revision,
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % (
            'command', VDELIM, self.command, GenericCmd.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s\n' % ('result', VDELIM, self.result,
                                    self.str_field(self.result, HardwareCmd.RESULT))
        s += '%-20s%c %04X (%d)\n' % ('identifier', VDELIM,
                                      self.identifier, self.identifier)
        s += '%-20s%c %02X (%d)' % ('revision', VDELIM,
                                    self.revision, self.revision)
        return s
