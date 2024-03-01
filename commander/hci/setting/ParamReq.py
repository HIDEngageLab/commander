# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.setting.ParamCmd import ParamCmd
from commander.hci.setting.parameter.GenericParam import GenericParam


class ParamReq(ParamCmd):
    def __init__(self, identifier, func, parameter):
        ParamCmd.__init__(self, GenericCmd.DIRECTION['REQ'])

        self.__identifier = GenericParam.PARAM_ID[identifier.upper()]
        self.__function = ParamCmd.FUNCTION[func.upper()]

        if self.__function == ParamCmd.FUNCTION['GET']:
            self.__sdu = [self.command, self.__identifier, self.__function]
        else:
            self.__parameter = parameter
            self.__sdu = [self.command, self.__identifier,
                          self.__function] + self.__parameter.value

    @property
    def sdu(self):
        return self.__sdu

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    GenericCmd.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s\n' % ('identifier', VDELIM, self.__identifier,
                                    GenericCmd.str_field(self.__identifier, GenericParam.PARAM_ID))
        s += '%-20s%c %02X %s' % ('function', VDELIM,
                                  self.__function, GenericCmd.str_field(self.__function, ParamCmd.FUNCTION))
        if self.__function != ParamCmd.FUNCTION['GET']:
            s += '\n'
            s += '%-20s%c %s ' % ('value', VDELIM, self.__parameter.__str__())
        return s
