# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.EventCmd import EventCmd
from commander.hci.feature.MacroCmd import MacroCmd


class MacroStoreInd(MacroCmd):
    """
    macro data indication
    """

    def __init__(self, command):
        MacroCmd.__init__(self, 'DISPLAY', GenericCmd.DIRECTION['IND'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) < 9:
            print('payload empty')
            payload += [0] * (9 - len(payload))

        self.__index = (payload[0] << 8) + payload[1]
        self.__max = (payload[2] << 8) + payload[3]
        self.__event = payload[4]
        self.__data = payload[5:]

    @property
    def index(self):
        return self.__index

    @property
    def max(self):
        return self.__max

    @property
    def event(self):
        return self.__event

    @property
    def data(self):
        return self.__data

    @GenericCmd.fields.getter
    def fields(self):

        if self.event == EventCmd.EVENT['HASH']:
            macro_fields = {
                'INDEX': self.index,
                'MAX': self.max,
                GenericCmd.str_field(self.data[0], EventCmd.KEY_ID): GenericCmd.str_field(self.data[1], EventCmd.KEY_LEVEL)
            }
        elif self.event == EventCmd.EVENT['WHEEL']:
            from commander.utilities.floats import convert_to_float
            macro_fields = {
                'INDEX': self.index,
                'MAX': self.max,
                'POSITION': convert_to_float(b''.join([b'%c' % byte for byte in self.data]))
            }
        elif self.event == EventCmd.EVENT['DELAY']:
            from commander.utilities.floats import convert_to_float
            macro_fields = {
                'INDEX': self.index,
                'MAX': self.max,
                'DELAY': convert_to_float(b''.join([b'%c' % byte for byte in self.data]))
            }
        else:
            macro_fields = {
                'INDEX': self.index,
                'MAX': self.max,
                'DATA': ''.join(['%02X' % i for i in self.data])
            }

        return {self.str_command(self.command, GenericCmd.COMMANDS, '_'): macro_fields}

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %04X %d\n' % ('index', VDELIM,
                                    self.__index, self.__index)
        s += '%-20s%c %04X %d\n' % ('max', VDELIM, self.__max, self.__max)
        s += '%-20s%c %02X %s\n' % ('event', VDELIM, self.event,
                                    GenericCmd.str_field(self.event, EventCmd.EVENT))

        if self.event == EventCmd.EVENT['HASH']:
            key_id = GenericCmd.str_field(self.data[0], EventCmd.KEY_ID)
            s += '%-20s%c %02X %s\n' % ('key', VDELIM, self.data[0], key_id)
            key_level = GenericCmd.str_field(self.data[1], EventCmd.KEY_LEVEL)
            s += '%-20s%c %02X %s' % ('level', VDELIM, self.data[1], key_level)
        elif self.event == EventCmd.EVENT['WHEEL']:
            from commander.utilities.floats import convert_to_float
            event_data = ''.join(['%02X' % byte for byte in self.data])
            event_value = convert_to_float(
                b''.join([b'%c' % byte for byte in self.data]))
            s += '%-20s%c %s %5.2f%%' % ('position',
                                         VDELIM, event_data, event_value * 100)
        elif self.event == EventCmd.EVENT['DELAY']:
            from commander.utilities.floats import convert_to_float
            event_data = ''.join(['%02X' % byte for byte in self.data])
            event_value = convert_to_float(
                b''.join([b'%c' % byte for byte in self.data]))
            s += '%-20s%c %s %5.2f us' % ('delay',
                                          VDELIM, event_data, event_value)

        return s
