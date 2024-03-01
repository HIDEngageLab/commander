# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.control.StatusCmd import StatusCmd


class StatusCfm(StatusCmd):
    """
    status confirmation
    """

    def __init__(self, command):
        StatusCmd.__init__(self, GenericCmd.DIRECTION['CFM'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) < 12:
            print('payload empty')
            payload += [0xff] * (12 - len(payload))

        self.__result = payload[0]
        self.__function = payload[1]
        self.__operation = payload[2]
        self.__mode = payload[3]
        from commander.utilities.floats import convert_to_float
        self.__memory = convert_to_float(payload[4:8])
        self.__unique_key = (
            payload[8] << 24) + (payload[9] << 16) + (payload[10] << 8) + payload[11]

    @property
    def result(self):
        return self.__result

    @property
    def function(self):
        return self.__function

    @property
    def operation(self):
        return self.__operation

    @property
    def mode(self):
        return self.__mode

    @property
    def memory(self):
        return self.__memory

    @property
    def unique_key(self):
        return self.__unique_key

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                'RESULT': GenericCmd.str_field(self.result, StatusCmd.RESULT),
                'FUNCTION': self.str_field(self.function, StatusCmd.FUNCTION),
                'OPERATION': self.str_field(self.operation, StatusCmd.OPERATION),
                'MODE': self.str_field(self.mode, StatusCmd.MODE),
                'MEMORY': self.memory,
                'UNIQUE_KEY': self.unique_key,
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s\n' % ('result', VDELIM, self.result,
                                    GenericCmd.str_field(self.result, StatusCmd.RESULT))
        s += '%-20s%c %02X %s\n' % ('function', VDELIM, self.function,
                                    self.str_field(self.function, StatusCmd.FUNCTION))
        s += '%-20s%c %02X %s\n' % ('operation', VDELIM, self.operation,
                                    self.str_field(self.operation, StatusCmd.OPERATION))
        s += '%-20s%c %02X %s\n' % ('mode', VDELIM, self.mode,
                                    self.str_field(self.mode, StatusCmd.MODE))
        from commander.utilities.floats import convert_to_long
        s += '%-20s%c %04X (%5.2f%% free)\n' % ('memory',
                                                VDELIM, convert_to_long(self.memory), self.memory)
        bla = 'INVALID' if self.__unique_key == 0xffffffff else ''
        s += '%-20s%c %08X %s' % ('unique id', VDELIM, self.unique_key, bla)
        return s
