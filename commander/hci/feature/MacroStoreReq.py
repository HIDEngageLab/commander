# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.MacroCmd import MacroCmd


class MacroStoreReq(MacroCmd):
    def __init__(self, _payload=None):
        # Attention the command parameter are for the download session
        MacroCmd.__init__(self, 'DISPLAY', GenericCmd.DIRECTION['REQ'])

    @property
    def sdu(self):
        sdu_data = [self.command]
        return sdu_data

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        return s
