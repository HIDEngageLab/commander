# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.control.TemperatureCmd import TemperatureCmd
from commander.utilities.floats import convert_to_bytes


class TemperatureReq(TemperatureCmd):
    """
    temperature request
    """

    def __init__(self, _function, _temperature=None):
        TemperatureCmd.__init__(self, GenericCmd.DIRECTION['REQ'])

        function = _function.upper().strip()
        self.__function = TemperatureCmd.FUNCTION[function]
        self.__temperature = int(_temperature, 10) \
            if _temperature is not None else -300

    @property
    def function(self):
        return self.__function

    @property
    def temperature(self):
        return self.__temperature

    @property
    def sdu(self):
        return [self.command, self.function] + \
            (convert_to_bytes(self.temperature)
             if self.__function == TemperatureCmd.FUNCTION['ALARM'] else [])

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s' % ('function', VDELIM, self.function,
                                  self.str_field(self.function, TemperatureCmd.FUNCTION))
        if self.function == TemperatureCmd.FUNCTION['ALARM']:
            s += '\n'
            s += '%-20s%c %5.2f C' % ('temperature', VDELIM, self.temperature)
        return s
