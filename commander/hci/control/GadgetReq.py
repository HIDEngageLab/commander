# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.control.GadgetCmd import GadgetCmd


class GadgetReq(GadgetCmd):
    """
    gadget status request 
    """

    def __init__(self, _function):
        GadgetCmd.__init__(self, GenericCmd.DIRECTION['REQ'])

        function = _function.upper().strip()
        if GenericCmd.find_field(function, GadgetCmd.FUNCTION):
            self.__function = GadgetCmd.FUNCTION[function]
        else:
            raise Exception('unknown function')

        self.__function = GadgetCmd.FUNCTION[function]

    @property
    def function(self):
        return self.__function

    @property
    def sdu(self):
        return [self.command, self.__function]

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s\n' % ('function', VDELIM, self.__function,
                                    GenericCmd.str_field(self.__function, GadgetCmd.FUNCTION))

        return s
