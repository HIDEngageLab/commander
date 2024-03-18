# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd


class GpioCmd(GenericCmd):
    FUNCTION = {
        'ENABLE': GenericCmd.FUNCTION['ENABLE'],
        'DISABLE': GenericCmd.FUNCTION['DISABLE'],

        'DIRECTION': GenericCmd.FUNCTION['CUSTOM'],
        'IN': GenericCmd.FUNCTION['CUSTOM'] + 1,
        'OUT': GenericCmd.FUNCTION['CUSTOM'] + 2,
        'VALUE': GenericCmd.FUNCTION['CUSTOM'] + 3,
        'HIGH': GenericCmd.FUNCTION['CUSTOM'] + 4,
        'LOW': GenericCmd.FUNCTION['CUSTOM'] + 5,
    }

    RESULT = {
        'FAILURE': GenericCmd.RESULT['FAILURE'],
        'SUCCESS': GenericCmd.RESULT['SUCCESS'],
        'UNKNOWN': GenericCmd.RESULT['UNKNOWN'],
        'UNSUPPORTED': GenericCmd.RESULT['UNSUPPORTED'],

        'WRONG_DIRECTION': GenericCmd.RESULT['CUSTOM'],
        'WRONG_IDENTIFIER': GenericCmd.RESULT['CUSTOM'] + 1,
    }

    def __init__(self, direction):
        GenericCmd.__init__(self, GenericCmd.COMMANDS['GPIO'], direction)
