# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.DisplayCmd import DisplayCmd


class DisplayReq(DisplayCmd):
    def __init__(self, _function, *_args):
        DisplayCmd.__init__(self, GenericCmd.DIRECTION['REQ'])

        function = _function.upper().strip()
        if GenericCmd.find_field(function, DisplayCmd.FUNCTION):
            self.__function = DisplayCmd.FUNCTION[function]
        else:
            raise Exception('unknown function')

        self.__line = 0xff
        self.__column = 0xff
        self.__font = 0xff
        self.__icon = 0xff
        self.__text = ''
        if self.function == DisplayCmd.FUNCTION['CLEAN']:
            pass
        elif self.function == DisplayCmd.FUNCTION['POSITION']:
            self.__line = _args[0] if isinstance(_args[0], int) \
                else int(_args[0], 10)
            self.__column = _args[1] if isinstance(_args[1], int) \
                else int(_args[1], 10)
        elif self.function == DisplayCmd.FUNCTION['FONT']:
            self.__font = _args[0] if isinstance(_args[0], int) \
                else int(_args[0], 10)
        elif self.function == DisplayCmd.FUNCTION['ICON']:
            self.__icon = _args[0] if isinstance(_args[0], int) \
                else int(_args[0], 10)
        elif self.function == DisplayCmd.FUNCTION['TEXT']:
            self.__text = _args[0]

    @property
    def function(self):
        return self.__function

    @property
    def sdu(self):
        if self.function == DisplayReq.FUNCTION['CLEAN']:
            return [self.command, self.function]
        elif self.function == DisplayReq.FUNCTION['POSITION']:
            return [self.command, self.function, self.__line, self.__column]
        elif self.function == DisplayReq.FUNCTION['FONT']:
            return [self.command, self.function, self.__font]
        elif self.function == DisplayReq.FUNCTION['ICON']:
            return [self.command, self.function, self.__icon]
        elif self.function == DisplayReq.FUNCTION['TEXT']:
            return [self.command, self.function] + [ord(a) for a in self.__text]

        return [self.command, self.function]

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  self.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %s' % ('function', VDELIM, self.function,
                                  GenericCmd.str_field(self.function, DisplayCmd.FUNCTION))
        if self.function == DisplayCmd.FUNCTION['CLEAN']:
            pass
        elif self.function == DisplayCmd.FUNCTION['POSITION']:
            s += '\n'
            s += '%-20s%c %02X %d' % ('line', VDELIM,
                                      self.__line, self.__line)
            s += '\n'
            s += '%-20s%c %02X %d' % ('column', VDELIM,
                                      self.__column, self.__column)
        elif self.function == DisplayCmd.FUNCTION['TEXT']:
            s += '\n'
            s += '%-20s%c %s' % ('text', VDELIM, self.__text)
        elif self.function == DisplayCmd.FUNCTION['FONT']:
            s += '\n'
            s += '%-20s%c %02X %d' % ('font', VDELIM, self.__font, self.__font)
        elif self.function == DisplayCmd.FUNCTION['ICON']:
            s += '\n'
            s += '%-20s%c %02X %d' % ('icon', VDELIM, self.__icon, self.__icon)

        return s
