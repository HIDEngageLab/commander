# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd


class TemperatureCmd(GenericCmd):

    RESULT = {
        **GenericCmd.RESULT,
    }

    FUNCTION = {
        'GET': GenericCmd.FUNCTION['GET'],

        'ALARM': GenericCmd.FUNCTION['CUSTOM'],

        'UNDEFINED': 0xff
    }

    def __init__(self, direction):
        GenericCmd.__init__(
            self, GenericCmd.COMMANDS['TEMPERATURE'], direction)
