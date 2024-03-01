# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd


class StatusCmd(GenericCmd):
    FUNCTION = {'GET': 0x00,
                'START': 0x05,
                'STOP': 0x06,
                'RECORD': 0x07,
                'PLAY': 0x08}

    OPERATION = {'RECORD': 0x00,
                 'PLAY': 0x01,
                 'UNDEFINED': 0xff}

    MODE = {'IDLE': 0x00,
            'ACTIVE': 0x01,
            'PENDING': 0x02,
            'UNDEFINED': 0xff}

    RESULT = {'SUCCESS': 0x00,
              'FAILURE': 0x01,
              'UNKNOWN_FUNCTION': 0x02,
              'WRONG_OPERATION': 0x03,
              'WRONG_MODE': 0x04,
              'IDENTIFIER_EXISTS': 0x05}

    def __init__(self, direction):
        GenericCmd.__init__(self, GenericCmd.COMMANDS['GADGET'], direction)
