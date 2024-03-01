# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


class GenericCmd(object):
    # a1 b2 c3 e4 22 00 00 00 00 00 00 00 00 00 00
    MAX_PAYLOAD_LEN = 32

    DIRECTION_OFFSET = 2

    DIRECTION = {
        'REQ': 0x00,
        'CFM': 0x01,
        'IND': 0x02,
        'RES': 0x03,
    }

    COMMANDS = {
        'BACKLIGHT': (0x0e << DIRECTION_OFFSET),
        'DISPLAY': (0x08 << DIRECTION_OFFSET),
        'GADGET': (0x02 << DIRECTION_OFFSET),
        'GPIO': (0x11 << DIRECTION_OFFSET),
        'HASH': (0x07 << DIRECTION_OFFSET),
        'IDENTITY': (0x05 << DIRECTION_OFFSET),
        'KEYPAD': (0x0c << DIRECTION_OFFSET),
        'PARAMETER': (0x06 << DIRECTION_OFFSET),
        'PROTOCOL': (0x00 << DIRECTION_OFFSET),
        'RESET': (0x01 << DIRECTION_OFFSET),
        'TEMPERATURE': (0x0d << DIRECTION_OFFSET),
    }

    def __init__(self, command, direction):
        self.__command = command + direction

    @property
    def command(self):
        return self.__command

    @property
    def fields(self):
        return {
            'command': self.__command
        }

    @staticmethod
    def str_command(command, dictionary=COMMANDS, junction='+'):
        co = ''
        for v, k in dictionary.items():
            if k == (command & 0xfc):
                co += v
                break
        co += junction
        for v, k in GenericCmd.DIRECTION.items():
            if k == (command & 0x03):
                co += v
                break
        return co

    @staticmethod
    def str_field(field, dictionary):
        co = ''
        for v, k in dictionary.items():
            # print v,k
            if k == field:
                co += v
                break
        return co

    @staticmethod
    def find_field(field, dictionary):
        for v, k in dictionary.items():
            if v == field:
                return v
        return None
