# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


class Keypad:
    """
    button click and push times in ms (16 bit values)

    input:
        integer ms like: CLICK_VALUE PUSH_VALUE
    """

    DEFAULT_CLICK_MS = 128
    DEFAULT_PUSH_MS = 384
    DEFAULT = [(DEFAULT_CLICK_MS >> 8) & 0xff, (DEFAULT_CLICK_MS >> 0) & 0xff,
               (DEFAULT_PUSH_MS >> 8) & 0xff, (DEFAULT_PUSH_MS >> 0) & 0xff]

    def __init__(self, _value=None):
        self.__click_ms = Keypad.DEFAULT_CLICK_MS
        self.__push_ms = Keypad.DEFAULT_PUSH_MS
        self.serialize(_value if _value is not None else Keypad.DEFAULT)

    @property
    def value(self):
        v1 = [(self.__click_ms >> 8) & 0xff, self.__click_ms & 0xff]
        v2 = [(self.__push_ms >> 8) & 0xff, self.__push_ms & 0xff]
        return v1 + v2

    def serialize(self, _value):
        if len(_value) == 2:
            click_ms = _value[0] if isinstance(
                _value[0], int) else int(_value[0], 10)
            push_ms = _value[1] if isinstance(
                _value[1], int) else int(_value[1], 10)
            value = [(click_ms >> 8) & 0xff, (click_ms >> 0) & 0xff,
                     (push_ms >> 8) & 0xff, (push_ms >> 0) & 0xff]
        elif len(_value) == self.type_len:
            value = _value
        else:
            value = Keypad.DEFAULT

        self.__click_ms = (value[0] << 8) + value[1]
        self.__push_ms = (value[2] << 8) + value[3]

    @property
    def type_len(self):
        return 4

    def __str__(self):
        s = ''
        s += 'click: %04X (%d ms)' % (self.__click_ms, self.__click_ms)
        s += ' push: %04X (%d ms)' % (self.__push_ms, self.__push_ms)
        return s
