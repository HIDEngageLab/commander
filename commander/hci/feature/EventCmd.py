# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd


class EventCmd(GenericCmd):
    EVENT = {'HASH': 0x00,
             'WHEEL': 0x01,
             'DELAY': 0x02,
             'DEBUG': 0x03,
             'LED': 0x04,
             'POWER': 0x05,
             'UNDEFINED': 0xff}

    KEY_ID = {'S0': 0x00,
              'S1': 0x01,
              'S2': 0x02,
              'S3': 0x03,
              'S4': 0x04,
              'S5': 0x05,
              'S6': 0x06,
              'S7': 0x07,
              'S8': 0x08,
              'S9': 0x09}

    KEY_LEVEL = {'PRESS': 0x00,
                 'RELEASE': 0x01,
                 'CLICK': 0x02,
                 'PUSH': 0x03,
                 'UNDEFINED': 0xff}

    DEBUG_ID = {'DEBUG_PIN1': 0x0a,
                'DEBUG_PIN2': 0x0b,
                'DEBUG_PIN3': 0x0c,
                'DEBUG_PIN4': 0x0d}

    DEBUG_LEVEL = {'LOW': 0x00,
                   'HIGH': 0x01,
                   'UNDEFINED': 0xff}

    LED_ID = {'LED_TEST1': 0x0e,
              'LED_TEST2': 0x0f}

    LED_LEVEL = {'OFF': 0x00,
                 'ON': 0x01,
                 'UNDEFINED': 0xff}

    POWER = {'BELOW': 0x00,
             'ABOVE': 0x01,
             'NORMAL': 0x02}

    FILTER = {'ENABLE': 0x00,
              'DISABLE': 0x01}

    RESULT = {'SUCCESS': 0x00,
              'FAILURE': 0x01,
              'UNKNOWN_EVENT': 0x02,
              'WRONG_VALUE': 0x03,
              'WRONG_OPERATION': 0x04}

    def __init__(self, direction):
        GenericCmd.__init__(self, GenericCmd.COMMANDS['KEYPAD'], direction)
