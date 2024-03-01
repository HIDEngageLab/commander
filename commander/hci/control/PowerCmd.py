# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd


class PowerCmd(GenericCmd):
    FUNCTION = {'GET': 0x00,
                'OBSERVER_SET': 0x01,
                'OBSERVER_RESET': 0x02,
                'OBSERVER_INTERVAL': 0x07,
                'UNDEFINED': 0xff}

    VOLTAGE = {'1V8': 0x00,
               '3V2': 0x01,
               '5V0': 0x02,
               'SER_VBUS': 0x03,
               'UNDEFINED': 0xff}

    RESULT = {'SUCCESS': 0x00,
              'FAILURE': 0x01,
              'UNKNOWN_FUNCTION': 0x02,
              'UNDEFINED_VOLTAGE': 0x03,
              'SHORT_INTERVAL': 0x04,
              'NO_OBSERVER': 0x05,
              'ALREADY_DONE': 0x0f}

    def __init__(self, direction):
        GenericCmd.__init__(
            self, GenericCmd.COMMANDS['BACKLIGHT'], direction)
