# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


class Features:
    """
    features

    input:
        <[auto_start:<ENABLE|DISABLE>][, ...]>
    """

    AUTO_START = 0x01

    VALUE = {
        'AUTO_START': AUTO_START}

    def __init__(self, value=None):
        if value is None:
            self.__value = 0

            self.__value |= Features.AUTO_START
        else:
            self.__value = 0
            for item in value:
                key, value = item.split(':')
                key = key.upper()
                value = value.upper()
                if key in Features.VALUE:
                    if value == 'ENABLE':
                        self.__value |= Features.VALUE[key]
                    elif value == 'DISABLE':
                        self.__value &= ~Features.VALUE[key]
                    else:
                        # default behavior?
                        self.__value &= ~Features.VALUE[key]
                else:
                    raise Exception('Features: unknown value', key)

    @property
    def value(self):
        return [self.__value]

    def serialize(self, value):
        if len(value) != self.type_len:
            raise Exception('Features setter: check payload length')

        self.__value = value[0]

    @property
    def type_len(self):
        return 1

    def __str__(self):
        s = '%02X' % self.__value
        for k, v in Features.VALUE.items():
            s += ' %s:' % k
            if self.__value & v == v:
                s += 'ENABLED'
            else:
                s += 'DISABLED'
        return s
