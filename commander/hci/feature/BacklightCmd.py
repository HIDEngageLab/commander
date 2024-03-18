# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd


class BacklightCmd(GenericCmd):
    class Color:
        def __init__(self, _color=None):
            self.__r = 0xff
            self.__g = 0xff
            self.__b = 0xff
            self.deserialize(_color)

        def deserialize(self, _data=None):
            if _data is None:
                _data = "ffffff"

            if isinstance(_data, str):
                tmp = [int('%c%c' % (_data[i], _data[i + 1]), 16)
                       for i in range(0, (len(_data) >> 1) << 1, 2)]
                if len(tmp) < 3:
                    tmp += [0xff] * (3-len(tmp))
            else:
                tmp = _data

            self.__r = tmp[0]
            self.__g = tmp[1]
            self.__b = tmp[2]

        def __str__(self):
            return '%02X%02X%02X' % (self.__r, self.__g, self.__b)

        @property
        def r(self):
            return self.__r

        @property
        def g(self):
            return self.__g

        @property
        def b(self):
            return self.__b

        @r.setter
        def r(self, _value):
            self.__r = _value

        @g.setter
        def g(self, _value):
            self.__g = _value

        @b.setter
        def b(self, _value):
            self.__b = _value

        @property
        def value(self):
            return [self.r, self.g, self.b]

    PROGRAM = {
        'ALERT': 0x00,
        'CONST': 0x01,
        'MEDIUM': 0x02,
        'MORPH': 0x03,
        'MOUNT': 0x04,
        'OFF': 0x05,
        'SET': 0x06,
        'SLOW': 0x07,
        'SUSPEND': 0x08,
        'TURBO': 0x09,

        'UNDEFINED': 0xff,
    }

    RESULT = {
        **GenericCmd.RESULT,
    }

    def __init__(self, direction):
        GenericCmd.__init__(
            self, GenericCmd.COMMANDS['BACKLIGHT'], direction)
