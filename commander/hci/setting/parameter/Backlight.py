# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


from commander.hci.GenericCmd import GenericCmd


class Backlight:
    """
    backlight parameter
        DEFAULT_MODE (1 Byte):  0:ALERT, 1:CONST, 2:MEDIUM, 3:MORPH, 4:MOUNT, 5:OFF, 6:SET, 7:SLOW, 8:SUSPEND and 9:TURBO
        COLOR_LEFT (3 Bytes, R,G,B)
        COLOR_RIGHT (3 Bytes, R,G,B)
        TIMEOUT (2 Bytes) Time period from Default to Normal Mode in ms

    input:
        hex array, like: 07 ff 00 00 00 ff 00 00 ff
    """

    MODE = {
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

    DEFAULT = [0x09, 0x00, 0x0f, 0x0f, 0x00, 0x0e, 0x1f, 0x3a, 0x98]

    def __init__(self, _value=None):
        self.serialize(_value if _value is not None else Backlight.DEFAULT)

    def serialize(self, _value):
        if len(_value) != self.type_len:
            _value = Backlight.DEFAULT

        value = []
        for item in _value:
            if isinstance(item, str):
                value.append(int(item, 16))
            else:
                value.append(item)

        self.__mode = value[0]
        self.__left = value[1:4]
        self.__right = value[4:7]
        self.__timeout = (value[7] << 8) + (value[8])

    @property
    def value(self):
        return [self.__mode] + self.__left + self.__right + [(self.__timeout >> 8) & 0xff, self.__timeout & 0xff]

    @property
    def type_len(self):
        return 9

    def __str__(self):
        s = ''
        s += 'mode: %02X (%d %s)' % (self.__mode, self.__mode,
                                     GenericCmd.str_field(self.__mode, Backlight.MODE))
        s += 'left: #%02X%02X%02X' % (self.__left[0],
                                      self.__left[1],
                                      self.__left[2])
        s += 'right: #%02X%02X%02X' % (self.__right[0],
                                       self.__right[1],
                                       self.__right[2])
        s += ' timeout: %04X (%d)' % (self.__timeout,
                                      self.__timeout)
        return s
