# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.BacklightCmd import BacklightCmd


class BacklightCfm(BacklightCmd):
    """
    backlight confirmation
    """

    def __init__(self, command):
        BacklightCmd.__init__(self, GenericCmd.DIRECTION['CFM'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) < 2:
            print('payload empty')
            payload = [0xff] * 2

        self.__result = payload[0]
        self.__function = payload[1]

        if self.function == BacklightCmd.PROGRAM['SET'] or self.function == BacklightCmd.PROGRAM['MORPH']:
            if len(payload) < 8:
                print('set/morph payload empty')
                payload += [0xff] * 6

        self.__left = BacklightCmd.Color(payload[2:5])
        self.__right = BacklightCmd.Color(payload[5:8])

    @property
    def result(self):
        return self.__result

    @property
    def function(self):
        return self.__function

    @property
    def left(self):
        return '%s' % self.__left

    @property
    def right(self):
        return '%s' % self.__right

    @GenericCmd.fields.getter
    def fields(self):
        if self.function == BacklightCmd.PROGRAM['SET'] or self.function == BacklightCmd.PROGRAM['MORPH']:
            return {
                self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                    'RESULT': GenericCmd.str_field(self.result, BacklightCmd.RESULT),
                    'PROGRAM': GenericCmd.str_field(self.function, BacklightCmd.PROGRAM),
                    'LEFT': self.left,
                    'RIGHT': self.right,
                }
            }

        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                'RESULT': GenericCmd.str_field(self.result, BacklightCmd.RESULT),
                'PROGRAM': GenericCmd.str_field(self.function, BacklightCmd.PROGRAM),
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s\n' % ('result', VDELIM, self.result,
                                    GenericCmd.str_field(self.result, BacklightCmd.RESULT))
        s += '%-20s%c %02X %s' % ('program', VDELIM, self.function,
                                  GenericCmd.str_field(self.function, BacklightCmd.PROGRAM))
        if self.function == BacklightCmd.PROGRAM['SET'] or self.function == BacklightCmd.PROGRAM['MORPH']:
            s += '\n'
            s += '%-20s%c %s\n' % ('left', VDELIM, self.left)
            s += '%-20s%c %s' % ('right', VDELIM, self.right)
        return s
