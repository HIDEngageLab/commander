# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.control.StatusCmd import StatusCmd


class StatusInd(StatusCmd):
    """
    sync status indication
    """

    def __init__(self, command):
        StatusCmd.__init__(self, GenericCmd.DIRECTION['IND'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) < 6:
            print('payload empty')
            payload += [0xff] * (6 - len(payload))

        self.__operation = payload[0]
        self.__mode = payload[1]
        from commander.utilities.floats import convert_to_float
        self.__memory = convert_to_float(payload[2:])

    @property
    def operation(self):
        return self.__operation

    @property
    def mode(self):
        return self.__mode

    @property
    def memory(self):
        return self.__memory

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                'OPERATION': self.str_field(self.operation, StatusCmd.OPERATION),
                'MODE': self.str_field(self.mode, StatusCmd.MODE),
                'MEMORY': self.memory,
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s\n' % ('operation', VDELIM, self.operation,
                                    self.str_field(self.operation, StatusCmd.OPERATION))
        s += '%-20s%c %02X %s\n' % ('mode', VDELIM, self.mode,
                                    self.str_field(self.mode, StatusCmd.MODE))
        from commander.utilities.floats import convert_to_long
        s += '%-20s%c %04X (%5.2f%% free)' % ('memory', VDELIM,
                                              convert_to_long(self.memory), self.memory)
        return s
