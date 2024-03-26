# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.setting.ParameterCmd import ParameterCmd
from commander.hci.setting.parameter.GenericParam import GenericParam
from commander.utilities.dict_tweaks import value_to_key


class ParameterCfm(ParameterCmd):
    """
    parameter confirmation
    """

    def __init__(self, command):
        ParameterCmd.__init__(self, GenericCmd.DIRECTION['CFM'])

        if self.command != command[0]:
            print('unknown command id: %04X' % command[0])

        payload = command[1]
        if len(payload) == 0:
            print('payload empty')
            payload = [0] * 3

        self.__result = payload[0]
        self.__identifier = payload[1]
        self.__function = payload[2]

        identifier = value_to_key(GenericParam.PARAM_ID, self.__identifier)
        if identifier is None:
            self.__parameter = None
            raise Exception('unknown parameter identifier')

        parameter = GenericParam.search(identifier)
        if parameter is None:
            raise Exception('parameter %s not found' % identifier)
        
        self.__parameter = parameter(payload[3:])

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
    def parameter(self):
        return self.__parameter

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                'RESULT': GenericCmd.str_field(self.result, ParameterCmd.RESULT),
                'IDENTIFIER': GenericCmd.str_field(self.identifier, GenericParam.PARAM_ID),
                'FUNCTION': GenericCmd.str_field(self.function, ParameterCmd.FUNCTION),
                'VALUE': self.parameter,
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM,
                                  self.command, GenericCmd.str_command(self.command))
        s += '\n'
        s += '%-20s%c %02X %s' % ('result', VDELIM, self.result,
                                  GenericCmd.str_field(self.result, ParameterCmd.RESULT))
        s += '\n'
        s += '%-20s%c %02X %s' % ('identifier', VDELIM, self.identifier,
                                  GenericCmd.str_field(self.identifier, GenericParam.PARAM_ID))
        s += '\n'
        s += '%-20s%c %02X %s' % ('function', VDELIM, self.function,
                                  GenericCmd.str_field(self.function, ParameterCmd.FUNCTION))
        s += '\n'
        s += '%-20s%c %s' % ('value', VDELIM, self.parameter)
        return s
