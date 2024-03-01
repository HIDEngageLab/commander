# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.control.PowerCmd import PowerCmd


class PowerReq(PowerCmd):
    def __init__(self, function, parameter=None):
        PowerCmd.__init__(self, GenericCmd.DIRECTION['REQ'])

        self.__function = PowerCmd.FUNCTION[function.upper()]

        if self.function == PowerCmd.FUNCTION['GET']:
            self.__voltage = None
            self.__limit_low = None
            self.__limit_high = None
            self.__interval = None
            self.__sdu = [self.command, self.function]
        elif self.function == PowerCmd.FUNCTION['OBSERVER_SET']:
            voltage = parameter[0].strip().upper()
            if voltage in PowerCmd.VOLTAGE:
                self.__voltage = PowerCmd.VOLTAGE[voltage]
            else:
                self.__voltage = PowerCmd.VOLTAGE['UNDEFINED']
            self.__limit_low = float(parameter[1])
            self.__limit_high = float(parameter[2])
            self.__interval = None

            from commander.utilities.floats import convert_to_long
            limit_low_raw = convert_to_long(self.limit_low)
            limit_high_raw = convert_to_long(self.limit_high)
            self.__sdu = [self.command, self.function, self.voltage,
                          (limit_low_raw >> 24) & 0xff,
                          (limit_low_raw >> 16) & 0xff,
                          (limit_low_raw >> 8) & 0xff,
                          (limit_low_raw >> 0) & 0xff,
                          (limit_high_raw >> 24) & 0xff,
                          (limit_high_raw >> 16) & 0xff,
                          (limit_high_raw >> 8) & 0xff,
                          (limit_high_raw >> 0) & 0xff]

        elif self.function == PowerCmd.FUNCTION['OBSERVER_RESET']:
            voltage = parameter[0].strip().upper()
            if voltage in PowerCmd.VOLTAGE:
                self.__voltage = PowerCmd.VOLTAGE[voltage]
            else:
                self.__voltage = PowerCmd.VOLTAGE['UNDEFINED']
            self.__limit_low = None
            self.__limit_high = None
            self.__interval = None
            self.__sdu = [self.command, self.function, self.voltage]
        elif self.function == PowerCmd.FUNCTION['OBSERVER_INTERVAL']:
            self.__voltage = None
            self.__limit_low = None
            self.__limit_high = None
            self.__interval = int(parameter[0])
            self.__sdu = [self.command, self.function,
                          (self.interval >> 24) & 0xff,
                          (self.interval >> 16) & 0xff,
                          (self.interval >> 8) & 0xff,
                          (self.interval >> 0) & 0xff]

    @property
    def function(self):
        return self.__function

    @property
    def voltage(self):
        return self.__voltage

    @property
    def limit_low(self):
        return self.__limit_low

    @property
    def limit_high(self):
        return self.__limit_high

    @property
    def interval(self):
        return self.__interval

    @property
    def sdu(self):
        return self.__sdu

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s' % ('function', VDELIM, self.function,
                                  self.str_field(self.function, PowerCmd.FUNCTION))
        if self.function == PowerCmd.FUNCTION['GET']:
            pass
        elif self.function == PowerCmd.FUNCTION['OBSERVER_SET']:
            s += '\n'
            s += '%-20s%c %02X %s\n' % ('voltage', VDELIM, self.voltage,
                                        self.str_field(self.voltage, PowerCmd.VOLTAGE))

        elif self.function == PowerCmd.FUNCTION['OBSERVER_RESET']:
            s += '\n'
            s += '%-20s%c %02X %s' % ('voltage', VDELIM, self.voltage,
                                      self.str_field(self.voltage, PowerCmd.VOLTAGE))
        elif self.function == PowerCmd.FUNCTION['OBSERVER_INTERVAL']:
            s += '\n'
            s += '%-20s%c %02X %d' % ('interval',
                                      VDELIM, self.interval, self.interval)

        return s
