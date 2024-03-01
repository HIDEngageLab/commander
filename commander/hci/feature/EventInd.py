# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.control.PowerCmd import PowerCmd
from commander.hci.feature.EventCmd import EventCmd


class EventInd(EventCmd):
    """
    event indication
    """

    def __init__(self, command):
        EventCmd.__init__(self, GenericCmd.DIRECTION['IND'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) == 0:
            print('payload empty')
            payload = [0] * 5

        self.__event = payload[0]
        self.__data = payload[1:]

    @property
    def event(self):
        return self.__event

    @GenericCmd.fields.getter
    def fields(self):
        if self.event == EventCmd.EVENT['HASH']:
            event_fields = {
                self.str_field(self.event, EventCmd.EVENT): {
                    self.str_field(self.__data[0], EventCmd.KEY_ID): self.str_field(self.__data[1], EventCmd.KEY_LEVEL)
                }
            }
        elif self.event == EventCmd.EVENT['WHEEL']:
            from commander.utilities.floats import convert_to_float
            event_fields = {
                'WHEEL': convert_to_float(self.__data) * 100.0
            }
        elif self.event == EventCmd.EVENT['DELAY']:
            from commander.utilities.floats import convert_to_float
            event_fields = {
                'DELAY': convert_to_float(self.__data)
            }
        elif self.event == EventCmd.EVENT['DEBUG']:
            event_fields = {
                'DEBUG': ''.join(['%02X' % i for i in self.__data])
            }
        elif self.event == EventCmd.EVENT['LED']:
            event_fields = {
                'LED': ''.join(['%02X' % i for i in self.__data])
            }
        elif self.event == EventCmd.EVENT['POWER']:
            from commander.utilities.floats import convert_to_float
            event_fields = {
                self.str_field(self.__data[0], PowerCmd.VOLTAGE): self.str_field(self.__data[1], EventCmd.POWER),
                'VALUE': convert_to_float(self.__data[2:6]),
                'LOW': convert_to_float(self.__data[6:10]),
                'HIGH': convert_to_float(self.__data[10:14])
            }
        else:
            event_fields = {'DATA': ''.join(['%02X' % i for i in self.__data])}

        return {self.str_command(self.command, GenericCmd.COMMANDS, '_'): event_fields}

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s\n' % ('event', VDELIM, self.event,
                                    self.str_field(self.event, EventCmd.EVENT))

        if self.event == EventCmd.EVENT['HASH']:
            key_str = ''
            key_str += self.str_field(self.__data[0], EventCmd.KEY_ID) + '/'
            key_str += self.str_field(self.__data[1], EventCmd.KEY_LEVEL)
            s += '%-20s%c %02X %02X %s' % ('value', VDELIM,
                                           self.__data[0], self.__data[1], key_str)
        elif self.event == EventCmd.EVENT['WHEEL']:
            from commander.utilities.floats import convert_to_float
            event_str = '%5.2f%%' % (convert_to_float(self.__data) * 100.0)
            s += '%-20s%c %s' % ('value', VDELIM, event_str)
        elif self.event == EventCmd.EVENT['DELAY']:
            from commander.utilities.floats import convert_to_float
            event_str = '%5.2f us' % convert_to_float(self.__data)
            s += '%-20s%c %s' % ('value', VDELIM, event_str)
        elif self.event == EventCmd.EVENT['DEBUG']:
            key_str = ''
            key_str += self.str_field(self.__data[0], EventCmd.DEBUG_ID) + '/'
            key_str += self.str_field(self.__data[1], EventCmd.DEBUG_LEVEL)
            s += '%-20s%c %02X %02X %s' % ('value', VDELIM,
                                           self.__data[0], self.__data[1], key_str)
        elif self.event == EventCmd.EVENT['LED']:
            key_str = ''
            key_str += self.str_field(self.__data[0], EventCmd.LED_ID) + '/'
            key_str += self.str_field(self.__data[1], EventCmd.LED_LEVEL)
            s += '%-20s%c %02X %02X %s' % ('value', VDELIM,
                                           self.__data[0], self.__data[1], key_str)
        elif self.event == EventCmd.EVENT['POWER']:
            s += '%-20s%c %02X %s\n' % ('voltage', VDELIM, self.__data[0],
                                        self.str_field(self.__data[0], PowerCmd.VOLTAGE))
            s += '%-20s%c %02X %s\n' % ('level', VDELIM, self.__data[1],
                                        self.str_field(self.__data[1], EventCmd.POWER))

            voltage_raw = self.__data[2:6]
            from commander.utilities.floats import convert_to_float
            voltage = '%5.2fV' % convert_to_float(voltage_raw)
            s += '%-20s%c %s\n' % ('value', VDELIM, voltage)

            limit_low_raw = self.__data[6:10]
            from commander.utilities.floats import convert_to_float
            limit_low = '%5.2fV' % convert_to_float(limit_low_raw)
            s += '%-20s%c %s\n' % ('low', VDELIM, limit_low)

            limit_high_raw = self.__data[10:14]
            from commander.utilities.floats import convert_to_float
            limit_high = '%5.2fV' % convert_to_float(limit_high_raw)
            s += '%-20s%c %s' % ('high', VDELIM, limit_high)

        else:
            s += '%-20s%c %s' % ('value', VDELIM,
                                 ' '.join(['%02X' % a for a in self.__data]))
        return s
