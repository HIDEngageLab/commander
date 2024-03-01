# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.setting.HardwareCmd import HardwareCmd


class HardwareReq(HardwareCmd):
    def __init__(self):
        HardwareCmd.__init__(self, GenericCmd.DIRECTION['REQ'])
        self.__sdu = [self.command]

    @property
    def sdu(self):
        return self.__sdu

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  self.str_command(self.command, GenericCmd.COMMANDS))
        return s
