# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd


class MacroCmd(GenericCmd):
    """
    macro data upload/download/clean
    """

    RESULT = {'SUCCESS': 0x00,
              'FAILURE': 0x01,
              'UNKNOWN_FUNCTION': 0x02,
              'WRONG_OPERATION': 0x03,
              'WRONG_MODE': 0x04,
              'OUT_OF_MEMORY': 0x05,
              'BUSY': 0x06,
              'EMPTY': 0x07}

    def __init__(self, function, direction):
        GenericCmd.__init__(self, GenericCmd.COMMANDS[function], direction)
