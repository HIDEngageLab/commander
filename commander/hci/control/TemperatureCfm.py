# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.control.TemperatureCmd import TemperatureCmd


class TemperatureCfm(TemperatureCmd):
    """
    temperature confirmation
    """

    def __init__(self, command):
        TemperatureCmd.__init__(self, GenericCmd.DIRECTION['CFM'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) < 3:
            print('payload empty')
            payload += [0xff] * (3 - len(payload))

        self.__result = payload[0]
        from commander.utilities.floats import convert_to_float
        self.__temperature = convert_to_float(payload[1:])

    @property
    def result(self):
        return self.__result

    @property
    def temperature(self):
        return self.__temperature

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                'RESULT': GenericCmd.str_field(self.result, TemperatureCmd.RESULT),
                'TEMPERATURE': self.temperature,
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % (
            'command', VDELIM, self.command, self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s\n' % (
            'result', VDELIM, self.__result, GenericCmd.str_field(self.result, TemperatureCmd.RESULT))
        s += '%-20s%c %5.2f C' % ('temperature', VDELIM, self.temperature)
        return s
