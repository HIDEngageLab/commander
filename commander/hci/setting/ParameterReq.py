# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.setting.ParameterCmd import ParameterCmd
from commander.hci.setting.parameter.GenericParam import GenericParam


class ParameterReq(ParameterCmd):
    def __init__(self, _function, _identifier, _value=None):
        ParameterCmd.__init__(self, GenericCmd.DIRECTION['REQ'])

        function = _function.upper().strip()
        if GenericCmd.find_field(function, ParameterCmd.FUNCTION):
            self.__function = ParameterCmd.FUNCTION[function]
        else:
            raise Exception('unknown parameter function')

        identifier = _identifier.upper().strip()
        parameter = GenericParam.search(identifier)
        if parameter is None:
            raise Exception('parameter %s not found' % identifier)
        self.__identifier = identifier

        if self.function == ParameterCmd.FUNCTION['GET']:
            self.__parameter = parameter()
        elif self.function == ParameterCmd.FUNCTION['SET']:
            self.__parameter = parameter(_value)

        self.__index = None
        if self.identifier == GenericParam.PARAM_ID['MAPPING'] and self.function == ParameterCmd.FUNCTION['GET']:
            if _value is None:
                self.__index = 0
            else:
                self.__index = int(_value[0], 10)

    @property
    def function(self):
        return self.__function

    @property
    def identifier(self):
        return GenericParam.PARAM_ID[self.__identifier]

    @property
    def parameter(self):
        return self.__parameter

    @property
    def index(self):
        return self.__index

    @property
    def sdu(self):
        sdu = [self.command, self.identifier, self.function]
        if self.function == ParameterCmd.FUNCTION['SET']:
            sdu += self.parameter.value

        if self.identifier == GenericParam.PARAM_ID['MAPPING'] and self.function == ParameterCmd.FUNCTION['GET']:
            sdu += [self.index]

        return sdu

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  GenericCmd.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %s' % ('identifier', VDELIM, self.identifier,
                                  GenericCmd.str_field(self.identifier, GenericParam.PARAM_ID))
        s += '\n'
        s += '%-20s%c %02X %s' % ('function', VDELIM, self.function,
                                  GenericCmd.str_field(self.function, ParameterCmd.FUNCTION))
        if self.function == ParameterCmd.FUNCTION['SET']:
            s += '\n'
            s += '%-20s%c %s' % ('value', VDELIM, self.parameter)
        if self.identifier == GenericParam.PARAM_ID['MAPPING'] and self.function == ParameterCmd.FUNCTION['GET']:
            s += '\n'
            s += '%-20s%c %02X %d' % ('index', VDELIM, self.index, self.index)

        return s
