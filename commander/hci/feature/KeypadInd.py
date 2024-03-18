# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.KeypadCmd import KeypadCmd


class KeypadInd(KeypadCmd):
    """
    keypad indication
    """

    def __init__(self, command):
        KeypadCmd.__init__(self, GenericCmd.DIRECTION['IND'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) == 0:
            print('payload empty')
            payload = [0] * 5

        self.__identifier = payload[0]
        self.__function = payload[1]
        self.__data = payload[2:]

    @property
    def identifier(self):
        return self.__identifier

    @property
    def function(self):
        return self.__function

    @GenericCmd.fields.getter
    def fields(self):
        if self.identifier == KeypadCmd.IDENTIFIER['HCI']:
            event_fields = {
                'FUNCTION': self.str_field(self.function, KeypadCmd.FUNCTION)
            }
        elif self.identifier == KeypadCmd.IDENTIFIER['HID']:
            event_fields = {
                'FUNCTION': self.str_field(self.function, KeypadCmd.FUNCTION)
            }
        elif self.identifier == KeypadCmd.IDENTIFIER['KEYCODE']:
            modifier = self.__data[0]
            code = self.__data[1]
            event_fields = {
                'FUNCTION': self.str_field(self.function, KeypadCmd.FUNCTION),
                'MODIFIER': modifier,
                'CODE': code,
            }
        elif self.identifier == KeypadCmd.IDENTIFIER['MAPPING']:
            table = self.__data[0]
            event_fields = {
                'FUNCTION': self.str_field(self.function, KeypadCmd.FUNCTION),
                'TABLE': table,
            }
        else:
            event_fields = {'DATA': ''.join(['%02X' % i for i in self.__data])}

        return {self.str_command(self.command, GenericCmd.COMMANDS, '_'): event_fields}

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  self.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %s' % ('identifier', VDELIM, self.identifier,
                                  self.str_field(self.identifier, KeypadCmd.IDENTIFIER))
        s += '\n'
        s += '%-20s%c %02X %s' % ('function', VDELIM, self.function,
                                  self.str_field(self.function, KeypadCmd.FUNCTION))

        if self.identifier == KeypadCmd.IDENTIFIER['KEYCODE']:
            modifier = self.__data[0]
            code = self.__data[1]
            s += '\n'
            s += '%-20s%c %02X %s' % ('modifier', VDELIM, modifier,
                                      KeypadCmd.show_modifier(modifier))
            s += '\n'
            s += '%-20s%c %02X %d' % ('code', VDELIM, code, code)
        elif self.identifier == KeypadCmd.IDENTIFIER['MAPPING']:
            table = self.__data[0]
            s += '\n'
            s += '%-20s%c %02X %s' % ('table', VDELIM, table,
                                      self.str_field(table, KeypadCmd.TABLE))
        else:
            s += '%-20s%c %s' % ('data', VDELIM,
                                 ' '.join(['%02X' % a for a in self.__data]))
        return s
