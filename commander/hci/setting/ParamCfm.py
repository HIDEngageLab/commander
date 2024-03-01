# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.setting.ParamCmd import ParamCmd
from commander.hci.setting.parameter.GenericParam import GenericParam


class ParamCfm(ParamCmd):
    """
    parameter confirmation
    """

    def __init__(self, command):
        ParamCmd.__init__(self, GenericCmd.DIRECTION['CFM'])

        if self.command != command[0]:
            print('unknown command id: %04X' % command[0])

        payload = command[1]
        if len(payload) == 0:
            print('payload empty')
            payload = [0] * 3

        self.__result = payload[0]
        self.__identifier = payload[1]
        self.__function = payload[2]
        self.__value = payload[3:]

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
    def value(self):
        return self.__value

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                'RESULT': GenericCmd.str_field(self.result, ParamCmd.RESULT),
                'IDENTIFIER': GenericCmd.str_field(self.identifier, GenericParam.PARAM_ID),
                'FUNCTION': GenericCmd.str_field(self.function, ParamCmd.FUNCTION),
                'VALUE': ''.join(['%02X' % i for i in self.value]),
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM,
                                    self.command, GenericCmd.str_command(self.command))
        s += '%-20s%c %02X %s\n' % ('result', VDELIM, self.result,
                                    GenericCmd.str_field(self.result, ParamCmd.RESULT))
        s += '%-20s%c %02X %s\n' % ('identifier', VDELIM, self.identifier,
                                    GenericCmd.str_field(self.identifier, GenericParam.PARAM_ID))
        s += '%-20s%c %02X %s\n' % ('function', VDELIM, self.function,
                                    GenericCmd.str_field(self.function, ParamCmd.FUNCTION))
        s += '%-20s%c' % ('value', VDELIM)
        return s
