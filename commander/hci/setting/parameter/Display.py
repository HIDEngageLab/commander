# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


class Display:
    """
    display parameter

    input:

    """

    DEFAULT_CLICK_MS = '128'
    DEFAULT_PUSH_MS = '384'
    DEFAULT = [DEFAULT_CLICK_MS, DEFAULT_PUSH_MS]

    def __init__(self, value=DEFAULT):
        if value is not None:
            self.__click_ms = int(value[0], 10)
            self.__push_ms = int(value[1], 10)
        else:
            self.__click_ms = Display.DEFAULT_CLICK_MS
            self.__push_ms = Display.DEFAULT_PUSH_MS

    @property
    def value(self):
        v1 = [(self.__click_ms >> 8) & 0xff, self.__click_ms & 0xff]
        v2 = [(self.__push_ms >> 8) & 0xff, self.__push_ms & 0xff]

        return v1 + v2

    def serialize(self, value):
        if len(value) != self.type_len:
            v1 = [(Display.DEFAULT_CLICK_MS >> 8) &
                  0xff, Display.DEFAULT_CLICK_MS & 0xff]
            v2 = [(Display.DEFAULT_PUSH_MS >> 8) &
                  0xff, Display.DEFAULT_PUSH_MS & 0xff]
            value = v1 + v2

        self.__click_ms = (value[0] << 8) + value[1]
        self.__push_ms = (value[2] << 8) + value[3]

    @property
    def type_len(self):
        return 4

    def __str__(self):
        s = ''
        s += 'click: %d, (%04X)' % (self.__click_ms, self.__click_ms)
        s += ' push: %d (%04X)' % (self.__push_ms, self.__push_ms)
        return s
