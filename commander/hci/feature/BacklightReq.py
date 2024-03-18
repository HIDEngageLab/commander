# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.BacklightCmd import BacklightCmd


class BacklightReq(BacklightCmd):
    """
    keypad backlight control request
    """

    def __init__(self, _function, _left=None, _right=None):
        BacklightCmd.__init__(self, GenericCmd.DIRECTION['REQ'])

        function = _function.upper().strip()
        if GenericCmd.find_field(function, BacklightCmd.PROGRAM):
            self.__function = BacklightCmd.PROGRAM[function]
        else:
            raise Exception('unknown function')

        self.__left = BacklightCmd.Color(_left)
        self.__right = BacklightCmd.Color(_right)

    @property
    def function(self):
        return self.__function

    @property
    def left(self):
        return '%s' % self.__left

    @property
    def right(self):
        return '%s' % self.__right

    @property
    def sdu(self):
        if self.function == BacklightCmd.PROGRAM['SET'] or self.function == BacklightCmd.PROGRAM['MORPH']:
            return [self.command, self.function] + self.__left.value + self.__right.value
        return [self.command, self.function]

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  self.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %s' % ('program', VDELIM, self.function,
                                  GenericCmd.str_field(self.function, BacklightCmd.PROGRAM))
        if self.function == BacklightCmd.PROGRAM['SET'] or self.function == BacklightCmd.PROGRAM['MORPH']:
            s += '\n'
            s += '%-20s%c %s' % ('left', VDELIM, self.left)
            s += '\n'
            s += '%-20s%c %s' % ('right', VDELIM, self.right)
        return s
