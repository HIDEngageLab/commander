# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd


class ResetCmd(GenericCmd):
    FUNCTION = {'SHUTDOWN': 0x00,
                'FORMAT': 0x01}

    def __init__(self, direction):
        GenericCmd.__init__(self, GenericCmd.COMMANDS['RESET'], direction)
