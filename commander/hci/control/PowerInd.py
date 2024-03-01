# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.control.PowerCmd import PowerCmd


class PowerInd(PowerCmd):
    """
    power indication
    """

    def __init__(self, command):
        PowerCmd.__init__(self, GenericCmd.DIRECTION['IND'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) < 6:
            print('payload empty')
            payload += [0xff] * (6 - len(payload))

        self.__voltage = payload[0]
        from commander.utilities.floats import convert_to_float
        self.__value = convert_to_float(payload[1:5])

    @property
    def voltage(self):
        return self.__voltage

    @property
    def value(self):
        return self.__value

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'):  {
                self.str_field(self.voltage, PowerCmd.VOLTAGE): self.value,
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s\n' % ('voltage', VDELIM, self.voltage,
                                    self.str_field(self.voltage, PowerCmd.VOLTAGE))
        s += '%-20s%c %5.2fV' % ('value', VDELIM, self.value)
        return s
