# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.control.TemperatureCmd import TemperatureCmd


class TemperatureInd(TemperatureCmd):
    """
    temperature indication
    """

    def __init__(self, command):
        TemperatureCmd.__init__(self, GenericCmd.DIRECTION['IND'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) < 4:
            print('payload empty')
            payload += [0xff] * (4 - len(payload))

        from commander.utilities.floats import convert_to_float
        self.__temperature = convert_to_float(payload[0:])

    @property
    def temperature(self):
        return self.__temperature

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'):  {
                'TEMPERATURE': self.temperature,
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %5.2f C' % ('temperature', VDELIM, self.temperature)
        return s
