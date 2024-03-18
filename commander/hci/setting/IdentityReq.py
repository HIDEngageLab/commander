# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.setting.IdentityCmd import IdentityCmd


class IdentityReq(IdentityCmd):
    """
    identity request
    """

    def __init__(self, _function, _part, _value=None):
        IdentityCmd.__init__(self, GenericCmd.DIRECTION['REQ'])

        function = _function.upper().strip()
        if GenericCmd.find_field(function, IdentityCmd.FUNCTION):
            self.__function = IdentityCmd.FUNCTION[function]
        else:
            raise Exception('unknown identity function')

        part = _part.upper().strip()
        if GenericCmd.find_field(part, IdentityCmd.PART):
            self.__part = IdentityCmd.PART[part]
        else:
            raise Exception('unknown identity part')

        if self.part == IdentityCmd.PART['SERIAL'] and self.function == IdentityCmd.FUNCTION['SET']:
            if isinstance(_value, []):
                if len(_value) < 12:
                    _value = [0] * (12-len(_value)) + _value
                self.__value = _value
            else:
                self.__value = None
                raise Exception("identity set serial number: wrong value")
        else:
            self.__value = None

    @property
    def sdu(self):
        return [self.command, self.function, self.part]

    @property
    def function(self):
        return self.__function

    @property
    def part(self):
        return self.__part

    @property
    def value(self):
        return self.__value

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  GenericCmd.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %s' % ('function', VDELIM, self.function,
                                  GenericCmd.str_field(self.function, IdentityCmd.FUNCTION))
        s += '\n'
        s += '%-20s%c %02X %s' % ('part', VDELIM, self.part,
                                  GenericCmd.str_field(self.part, IdentityCmd.PART))
        if self.function == IdentityCmd.FUNCTION['SET'] and self.part == IdentityCmd.PART['SERIAL']:
            s += '\n'
            s += '%-20s%c %s' % ('serial', VDELIM,
                                 ' '.join(['%02X' % byte for byte in self.value]))

        return s
