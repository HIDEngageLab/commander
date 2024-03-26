# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.control.GadgetCmd import GadgetCmd


class GadgetCfm(GadgetCmd):
    """
    gadget status confirmation
    """

    def __init__(self, command):
        GadgetCmd.__init__(self, GenericCmd.DIRECTION['CFM'])

        if self.command != command[0]:
            raise 'unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) < 12:
            print('payload empty')
            payload += [0xff] * (12 - len(payload))

        self.__result = payload[0]
        self.__function = payload[1]
        self.__state = payload[2]
        self.__unique = (payload[3] << 24) + \
            (payload[4] << 16) + \
            (payload[5] << 8) + \
            (payload[6] << 0)

    @property
    def result(self):
        return self.__result

    @property
    def function(self):
        return self.__function

    @property
    def state(self):
        return self.__state

    @property
    def unique(self):
        return self.__unique

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                'RESULT': GenericCmd.str_field(self.result, GadgetCmd.RESULT),
                'FUNCTION': self.str_field(self.function, GadgetCmd.FUNCTION),
                'STATE': self.str_field(self.state, GadgetCmd.STATE),
                'UNIQUE': self.unique,
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  self.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %s' % ('result', VDELIM, self.result,
                                  GenericCmd.str_field(self.result, GadgetCmd.RESULT))
        s += '\n'
        s += '%-20s%c %02X %s' % ('function', VDELIM, self.function,
                                  self.str_field(self.function, GadgetCmd.FUNCTION))
        s += '\n'
        s += '%-20s%c %02X %s' % ('state', VDELIM, self.state,
                                  self.str_field(self.state, GadgetCmd.STATE))
        s += '\n'
        s += '%-20s%c %02X %s' % ('unique', VDELIM, self.unique,
                                  self.str_field(self.unique, GadgetCmd.STATE))
        return s
