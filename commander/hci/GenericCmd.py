# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


def get_value(type_definition, key):
    if key in type_definition.__dict__:
        return type_definition.__dict__[key]
    else:
        raise Exception('unknown value')


def get_key(type_definition, value):
    return [k for k, v in type_definition.__dict__.items() if v == value][0]


class GenericCmd(object):
    MAX_PAYLOAD_LEN = 32
    DIRECTION_OFFSET = 2

    DIRECTION = {
        'REQ': 0x00,
        'CFM': 0x01,
        'IND': 0x02,
        'RES': 0x03,
    }

    COMMANDS = {
        'BACKLIGHT': (0x01 << DIRECTION_OFFSET),
        'DISPLAY': (0x02 << DIRECTION_OFFSET),
        'GADGET': (0x03 << DIRECTION_OFFSET),
        'GPIO': (0x04 << DIRECTION_OFFSET),
        'HASH': (0x05 << DIRECTION_OFFSET),
        'IDENTITY': (0x06 << DIRECTION_OFFSET),
        'KEYPAD': (0x07 << DIRECTION_OFFSET),
        'PARAMETER': (0x08 << DIRECTION_OFFSET),
        'PROTOCOL': (0x09 << DIRECTION_OFFSET),
        'RESET': (0x0A << DIRECTION_OFFSET),
        'TEMPERATURE': (0x0B << DIRECTION_OFFSET),
    }

    RESULT = {
        'ERROR': 0x04,
        'FAILURE': 0x01,
        'SUCCESS': 0x00,
        'UNKNOWN': 0x02,
        'UNSUPPORTED': 0x03,

        'CUSTOM': 0x80,
    }

    FUNCTION = {
        'CLEAN': 0x08,
        'DISABLE': 0x03,
        'ENABLE': 0x02,
        'GET': 0x00,
        'OFF': 0x07,
        'ON': 0x06,
        'SET': 0x01,
        'START': 0x04,
        'STOP': 0x05,

        'CUSTOM': 0x80,
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
