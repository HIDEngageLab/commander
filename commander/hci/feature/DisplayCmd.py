# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd


class DisplayCmd(GenericCmd):
    """
    macro data upload/download/clean
    """

    FUNCTION = {
        'CLEAN': GenericCmd.FUNCTION['CUSTOM'],
        'FONT': GenericCmd.FUNCTION['CUSTOM'] + 1,
        'ICON': GenericCmd.FUNCTION['CUSTOM'] + 2,
        'POSITION': GenericCmd.FUNCTION['CUSTOM'] + 3,
        'TEXT': GenericCmd.FUNCTION['CUSTOM'] + 4,
    }

    RESULT = {
        'SUCCESS': GenericCmd.RESULT['SUCCESS'],
        'FAILURE': GenericCmd.RESULT['FAILURE'],
        'UNKNOWN': GenericCmd.RESULT['UNKNOWN'],
        'WRONG_POSITION': GenericCmd.RESULT['CUSTOM'],
    }

    def __init__(self, direction):
        GenericCmd.__init__(self, GenericCmd.COMMANDS['DISPLAY'], direction)
