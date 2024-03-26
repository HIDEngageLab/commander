# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.KeypadCmd import KeypadCmd

import commander.termbase as output


class KeypadReq(KeypadCmd):
    """
    keypad request
    """

    def __init__(self, _function, *_args):
        KeypadCmd.__init__(self, GenericCmd.DIRECTION['REQ'])

        function = _function.upper().strip()
        if GenericCmd.find_field(function, KeypadCmd.FUNCTION):
            self.__function = KeypadCmd.FUNCTION[function]
        else:
            raise Exception('unknown function')

        self.__identifier = KeypadCmd.IDENTIFIER['UNDEFINED']

        if self.function == KeypadCmd.FUNCTION['DISABLE'] or self.function == KeypadCmd.FUNCTION['ENABLE']:
            identifier = _args[0].upper().strip()
            if identifier in ['HCI', 'HID']:
                self.__identifier = KeypadCmd.IDENTIFIER[identifier]
            else:
                raise Exception('wrong identifier')
        elif self.function == KeypadCmd.FUNCTION['GET']:
            self.__identifier = KeypadCmd.IDENTIFIER['MAPPING']
            self.__table = KeypadCmd.TABLE['UNDEFINED']
        elif self.function == KeypadCmd.FUNCTION['SET']:
            self.__identifier = KeypadCmd.IDENTIFIER['MAPPING']
            table = _args[0].upper().strip()
            if GenericCmd.find_field(table, KeypadCmd.TABLE):
                self.__table = KeypadCmd.TABLE[table]
            else:
                raise Exception('unknown mapping table')
        elif self.function == KeypadCmd.FUNCTION['CLICK'] or \
                function == KeypadCmd.FUNCTION['PUSH'] or \
                function == KeypadCmd.FUNCTION['PRESS'] or \
                function == KeypadCmd.FUNCTION['RELEASE']:
            self.__identifier = KeypadCmd.IDENTIFIER['KEYCODE']
            self.__modifier = int(_args[0], 16)
            self.__code = int(_args[1], 16)
        else:
            raise Exception('unexpected function')

    @property
    def sdu(self):
        base = [self.command, self.identifier, self.function]

        if self.identifier == KeypadCmd.IDENTIFIER['KEYCODE']:
            return base + [self.modifier, self.code]
        elif self.identifier == KeypadCmd.IDENTIFIER['MAPPING']:
            if self.function == KeypadCmd.FUNCTION['SET']:
                return base + [self.table]

        return base

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

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  self.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %s' % ('identifier', VDELIM, self.identifier,
                                  GenericCmd.str_field(self.identifier, KeypadCmd.IDENTIFIER))
        s += '\n'
        s += '%-20s%c %02X %s' % ('function', VDELIM, self.function,
                                  GenericCmd.str_field(self.function, KeypadCmd.FUNCTION))

        if self.identifier == KeypadCmd.IDENTIFIER['KEYCODE']:
            s += '\n'
            s += '%-20s%c %02X %s' % ('modifier', VDELIM, self.modifier,
                                      KeypadCmd.show_modifier(self.modifier))
            s += '\n'
            s += '%-20s%c %02X %d' % ('code', VDELIM, self.code, self.code)
        elif self.identifier == KeypadCmd.IDENTIFIER['MAPPING']:
            if self.function == KeypadCmd.FUNCTION['SET']:
                s += '\n'
                s += '%-20s%c %02X %s' % ('table', VDELIM, self.table,
                                          GenericCmd.str_field(self.table, KeypadCmd.TABLE))
        else:
            pass

        return s
