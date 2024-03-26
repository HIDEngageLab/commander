# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd


class GadgetCmd(GenericCmd):
    STATE = {
        'ACTIVE': 0x01,
        'IDLE': 0x00,
        'PENDING': 0x03,
        'SUSPEND': 0x02,

        'UNDEFINED': 0xff,
    }

    FUNCTION = {
        'GET': GenericCmd.FUNCTION['GET'],

        'MOUNT': GenericCmd.FUNCTION['CUSTOM'],
        'RESUME': GenericCmd.FUNCTION['CUSTOM'] + 1,
        'SUSPEND': GenericCmd.FUNCTION['CUSTOM'] + 2,
        'UNMOUNT': GenericCmd.FUNCTION['CUSTOM'] + 3,

        'UNDEFINED': 0xff,
    }

    RESULT = {
        'FAILURE': GenericCmd.RESULT['FAILURE'],
        'SUCCESS': GenericCmd.RESULT['SUCCESS'],
        'UNKNOWN': GenericCmd.RESULT['UNKNOWN'],
        'UNSUPPORTED': GenericCmd.RESULT['UNSUPPORTED'],

        'WRONG_STATE': GenericCmd.RESULT['CUSTOM'],
    }

    def __init__(self, direction):
        GenericCmd.__init__(self, GenericCmd.COMMANDS['GADGET'], direction)
