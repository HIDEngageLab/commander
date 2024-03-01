# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.setting.IdentityCmd import IdentityCmd


class IdentityReq(IdentityCmd):
    def __init__(self, part):
        IdentityCmd.__init__(self, GenericCmd.DIRECTION['REQ'])

        self.__part = IdentityCmd.PART[part]

    @property
    def sdu(self):
        return [self.command, self.__part]

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % (
            'command', VDELIM, self.command, GenericCmd.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s' % ('part', VDELIM, self.__part,
                                  GenericCmd.str_field(self.__part, IdentityCmd.PART))
        return s
