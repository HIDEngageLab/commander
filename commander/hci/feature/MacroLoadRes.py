# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.EventCmd import EventCmd
from commander.hci.feature.MacroCmd import MacroCmd


class MacroLoadRes(MacroCmd):
    def __init__(self, data):
        MacroCmd.__init__(self, 'MACRO_LOAD', GenericCmd.DIRECTION['RES'])

        if len(data) < 3:
            data = ['0', '0', 'key', 's0', 'release']

        self.__index = int(data[0])
        self.__max = int(data[1])
        self.__event = 0
        self.__value = [0] * 4

        event_id = data[2].strip().upper()
        if event_id in EventCmd.EVENT:
            self.__event = EventCmd.EVENT[event_id]
            if event_id == 'HASH':
                key_id = data[3].strip().upper()
                if key_id in EventCmd.KEY_ID:
                    self.__value[0] = EventCmd.KEY_ID[key_id]
                else:
                    self.__value[0] = 0
                    print('unknown key id')
                key_level = data[4].strip().upper()
                if key_level in EventCmd.KEY_LEVEL:
                    self.__value[1] = EventCmd.KEY_LEVEL[key_level]
                else:
                    self.__value[1] = 0
                    print('unknown key level')
                self.__value[2] = 0
                self.__value[3] = 0
            elif event_id == 'WHEEL':
                from commander.utilities.floats import convert_to_long
                wheel_value = convert_to_long((float(data[3]) % 100.0) / 100)
                self.__value[0] = (wheel_value >> 24) & 0xff
                self.__value[1] = (wheel_value >> 16) & 0xff
                self.__value[2] = (wheel_value >> 8) & 0xff
                self.__value[3] = wheel_value & 0xff
            elif event_id == 'DELAY':
                from commander.utilities.floats import convert_to_long
                delay_value = convert_to_long(float(eval(data[3])))
                self.__value[0] = (delay_value >> 24) & 0xff
                self.__value[1] = (delay_value >> 16) & 0xff
                self.__value[2] = (delay_value >> 8) & 0xff
                self.__value[3] = delay_value & 0xff
        else:
            print('unknown parameter')
            self.__event = 0
            self.__value = [0] * 4

        if len(self.__value) < 4:
            self.__value += [0] * (4 - len(self.__event))

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
    def value(self):
        return self.__value

    @property
    def sdu(self):
        sdu = [self.command, self.index >> 8, self.index &
               0xff, self.max >> 8, self.max & 0xff, self.event]
        sdu += self.value
        return sdu

    @GenericCmd.fields.getter
    def fields(self):

        if self.event == EventCmd.EVENT['HASH']:
            macro_fields = {
                'INDEX': self.index,
                'MAX': self.max,
                GenericCmd.str_field(self.event, EventCmd.EVENT): {
                    self.str_field(self.value[0], EventCmd.KEY_ID): self.str_field(self.value[1], EventCmd.KEY_LEVEL)
                }
            }
        elif self.event == EventCmd.EVENT['WHEEL']:
            from commander.utilities.floats import convert_to_float
            macro_fields = {
                'INDEX': self.index,
                'MAX': self.max,
                GenericCmd.str_field(self.event, EventCmd.EVENT): {
                    'POSITION': convert_to_float(self.value) * 100.0
                }
            }
        elif self.event == EventCmd.EVENT['DELAY']:
            from commander.utilities.floats import convert_to_float
            macro_fields = {
                'INDEX': self.index,
                'MAX': self.max,
                GenericCmd.str_field(self.event, EventCmd.EVENT): {
                    'DELAY': convert_to_float(self.value)
                }
            }
        else:
            macro_fields = {
                'INDEX': self.index,
                'MAX': self.max,
                GenericCmd.str_field(self.event, EventCmd.EVENT): {
                    'DATA': ''.join(['%02X' % i for i in self.sdu])
                }
            }

        return {self.str_command(self.command, GenericCmd.COMMANDS, '_'): macro_fields}

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %04X %d\n' % ('index', VDELIM, self.index, self.index)
        s += '%-20s%c %04X %d\n' % ('max', VDELIM, self.max, self.max)
        s += '%-20s%c %02X %s\n' % ('event', VDELIM, self.event,
                                    GenericCmd.str_field(self.event, EventCmd.EVENT))

        if self.event == EventCmd.EVENT['HASH']:
            key_str = ''
            key_str += self.str_field(self.value[0], EventCmd.KEY_ID) + '/'
            key_str += self.str_field(self.value[1], EventCmd.KEY_LEVEL)
            s += '%-20s%c %02X %02X %s' % ('value', VDELIM,
                                           self.value[0], self.value[1], key_str)
        elif self.event == EventCmd.EVENT['WHEEL']:
            from commander.utilities.floats import convert_to_float
            event_str = '%5.2f%%' % (convert_to_float(self.value) * 100.0)
            s += '%-20s%c %s' % ('value', VDELIM, event_str)
        elif self.event == EventCmd.EVENT['DELAY']:
            from commander.utilities.floats import convert_to_float
            event_str = '%5.2fus' % convert_to_float(self.value)
            s += '%-20s%c %s' % ('value', VDELIM, event_str)

        return s
