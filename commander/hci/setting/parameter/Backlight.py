# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


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

    DEFAULT = [0x09, 0x00, 0x0f, 0x0f, 0x00, 0x0e, 0x1f, 0x3a, 0x98]

    def __init__(self, value=DEFAULT):
        if value is not None:
            self.__mode = int(value[0], 16)
            self.__left = value[1:4]
            self.__right = value[4:7]
            self.__timeout = (value[7] << 8) + (value[8])
        else:
            self.__mode = int(Backlight.DEFAULT[0], 16)
            self.__left = Backlight.DEFAULT[1:4]
            self.__right = Backlight.DEFAULT[4:7]
            self.__timeout = (
                Backlight.DEFAULT[7] << 8) + (Backlight.DEFAULT[8])

    @property
    def value(self):
        return [self.__mode] + self.__left + self.__right + [(self.__timeout >> 8) & 0xff, self.__timeout & 0xff]

    def serialize(self, value):
        if len(value) != self.type_len:
            value = Backlight.DEFAULT

        self.__mode = int(value[0], 16)
        self.__left = value[1:4]
        self.__right = value[4:7]
        self.__timeout = (value[7] << 8) + (value[8])

    @property
    def type_len(self):
        return 9

    def __str__(self):
        s = ''
        s += 'mode: %d, (%04X)' % (self.__mode,
                                   self.__mode)
        s += 'left: #%04X%04X%04X' % (self.__left[0],
                                      self.__left[1],
                                      self.__left[2])
        s += 'right: #%04X%04X%04X' % (self.__right[0],
                                       self.__right[1],
                                       self.__right[2])
        s += ' timeout: %d (%04X)' % (self.__timeout,
                                      self.__timeout)
        return s
