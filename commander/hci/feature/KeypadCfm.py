# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.KeypadCmd import KeypadCmd


class KeypadCfm(KeypadCmd):
    """
    keypad confirmation
    """

    def __init__(self, command):
        KeypadCmd.__init__(self, GenericCmd.DIRECTION['CFM'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]

        self.__result = payload[0]
        self.__identifier = payload[1]
        self.__function = payload[2]

        if self.identifier == KeypadCmd.IDENTIFIER['KEYCODE']:
            self.__modifier = payload[3]
            self.__code = payload[4]
            self.__table = None
        elif self.identifier == KeypadCmd.IDENTIFIER['MAPPING']:
            self.__modifier = None
            self.__code = None
            self.__table = payload[3]

    @property
    def result(self):
        return self.__result

    @property
    def identifier(self):
        return self.__identifier

    @property
    def function(self):
        return self.__function

    @property
    def modifier(self):
        return self.__modifier

    @property
    def code(self):
        return self.__code

    @property
    def table(self):
        return self.__table

    @GenericCmd.fields.getter
    def fields(self):
        fields_dictionary = {
            'RESULT': self.str_field(self.result, KeypadCmd.RESULT),
            'IDENTIFIER': self.str_field(self.identifier, KeypadCmd.IDENTIFIER),
            'FUNCTION': self.str_field(self.function, KeypadCmd.FUNCTION),
        }
        if self.identifier == KeypadCmd.IDENTIFIER['KEYCODE']:
            fields_dictionary['MODIFIER'] = self.modifier
            fields_dictionary['CODE'] = self.code
            return {
                self.str_command(self.command, GenericCmd.COMMANDS, '_'): fields_dictionary
            }
        elif self.identifier == KeypadCmd.IDENTIFIER['MAPPING']:
            fields_dictionary['TABLE'] = self.str_field(self.table,
                                                        KeypadCmd.TABLE)
            return {
                self.str_command(self.command, GenericCmd.COMMANDS, '_'): fields_dictionary
            }
        else:
            return {
                self.str_command(self.command, GenericCmd.COMMANDS, '_'): fields_dictionary
            }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  self.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %s' % ('result', VDELIM, self.result,
                                  self.str_field(self.result, KeypadCmd.RESULT))
        s += '\n'
        s += '%-20s%c %02X %s' % ('identifier', VDELIM, self.identifier,
                                  self.str_field(self.identifier, KeypadCmd.IDENTIFIER))
        s += '\n'
        s += '%-20s%c %02X %s' % ('function', VDELIM, self.function,
                                  self.str_field(self.function, KeypadCmd.FUNCTION))
        if self.identifier == KeypadCmd.IDENTIFIER['KEYCODE']:
            s += '\n'
            s += '%-20s%c %02X %s' % ('modifier', VDELIM, self.modifier,
                                      KeypadCmd.show_modifier(self.modifier))
            s += '\n'
            s += '%-20s%c %02X %d' % ('code', VDELIM, self.code, self.code)
        elif self.identifier == KeypadCmd.IDENTIFIER['MAPPING']:
            s += '\n'
            s += '%-20s%c %02X %s' % ('table', VDELIM, self.table,
                                      self.str_field(self.table, KeypadCmd.TABLE))
        return s
