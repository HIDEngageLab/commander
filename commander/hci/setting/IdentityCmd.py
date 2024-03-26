# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd


class IdentityCmd(GenericCmd):
    FUNCTION = {
        'GET': GenericCmd.FUNCTION['GET'],
        'SET': GenericCmd.FUNCTION['SET'],
    }

    PART = {
        'FIRMWARE': 0,
        'HARDWARE': 1,
        'PLATFORM': 2,
        'PRODUCT': 3,
        'SERIAL': 4,
        'UNIQUE': 5,

        'UNDEFINED': 0xff,
    }

    RESULT = {
        **GenericCmd.RESULT,
    }

    def __init__(self, direction):
        GenericCmd.__init__(self, GenericCmd.COMMANDS['IDENTITY'], direction)
