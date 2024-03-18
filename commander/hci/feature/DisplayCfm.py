# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.DisplayCmd import DisplayCmd


class DisplayCfm(DisplayCmd):
    """
    display confirmation
    """

    def __init__(self, command):
        DisplayCmd.__init__(self, GenericCmd.DIRECTION['CFM'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) < 2:
            print('payload empty')
            payload = [0] * (2 - len(payload))

        self.__result = payload[0]
        self.__function = payload[1]

        if self.function == DisplayCmd.FUNCTION['CLEAN']:
            self.__args = []
        else:
            self.__args = payload[2:]

    @property
    def result(self):
        return self.__result

    @property
    def function(self):
        return self.__function

    @GenericCmd.fields.getter
    def fields(self):
        if self.function == DisplayCmd.FUNCTION['POSITION']:
            return {
                self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                    'RESULT': self.str_field(self.result, DisplayCmd.RESULT),
                    'FUNCTION': self.str_field(self.function, DisplayCmd.FUNCTION),
                    'LINE': self.__args[0],
                    'COLUMN': self.__args[1],
                }
            }
        elif self.function == DisplayCmd.FUNCTION['TEXT']:
            return {
                self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                    'RESULT': self.str_field(self.result, DisplayCmd.RESULT),
                    'FUNCTION': self.str_field(self.function, DisplayCmd.FUNCTION),
                    'TEXT': self.__args[0],
                }
            }
        elif self.function == DisplayCmd.FUNCTION['FONT']:
            return {
                self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                    'RESULT': self.str_field(self.result, DisplayCmd.RESULT),
                    'FUNCTION': self.str_field(self.function, DisplayCmd.FUNCTION),
                    'FONT': self.__args[0],
                }
            }
        elif self.function == DisplayCmd.FUNCTION['ICON']:
            return {
                self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                    'RESULT': self.str_field(self.result, DisplayCmd.RESULT),
                    'FUNCTION': self.str_field(self.function, DisplayCmd.FUNCTION),
                    'ICON': self.__args[0],
                }
            }

        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                'RESULT': self.str_field(self.result, DisplayCmd.RESULT),
                'FUNCTION': self.str_field(self.function, DisplayCmd.FUNCTION),
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  self.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %s' % ('result', VDELIM, self.result,
                                  self.str_field(self.result, DisplayCmd.RESULT))
        s += '\n'
        s += '%-20s%c %02X %s' % ('function', VDELIM, self.function,
                                  GenericCmd.str_field(self.function, DisplayCmd.FUNCTION))
        if self.function == DisplayCmd.FUNCTION['CLEAN']:
            pass
        elif self.function == DisplayCmd.FUNCTION['POSITION']:
            s += '\n'
            s += '%-20s%c %02X %d' % ('line', VDELIM,
                                      self.__args[0], self.__args[0])
            s += '\n'
            s += '%-20s%c %02X %d' % ('column', VDELIM,
                                      self.__args[1], self.__args[1])
        elif self.function == DisplayCmd.FUNCTION['TEXT']:
            s += '\n'
            s += '%-20s%c %02X %d' % ('text', VDELIM,
                                      self.__args[0], self.__args[0])
        elif self.function == DisplayCmd.FUNCTION['FONT']:
            s += '\n'
            s += '%-20s%c %02X %d' % ('font', VDELIM,
                                      self.__args[0], self.__args[0])

        elif self.function == DisplayCmd.FUNCTION['ICON']:
            s += '\n'
            s += '%-20s%c %02X %d' % ('icon', VDELIM,
                                      self.__args[0], self.__args[0])

        else:
            raise Exception('unknown function')
        return s
