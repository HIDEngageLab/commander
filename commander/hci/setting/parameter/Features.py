# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


class Features:
    """
    features
        A D K W 
        + - - - - - - + - - - - - - +
        | | | | +-------------------+--- reserved
        | | | +------------------------- wakeup
        | | +--------------------------- keypad
        | +----------------------------- display
        +------------------------------- auto start
    input:
        two hex bytes with bit flags (0:disable, 1:enable) like: f0 00
    """

    AUTO_START_MASK = 0x80
    DISPLAY_MASK = 0x40
    KEYPAD_MASK = 0x20
    WAKEUP_MASK = 0x10

    DEFAULT = [AUTO_START_MASK | DISPLAY_MASK |
               KEYPAD_MASK | WAKEUP_MASK, 0x00]

    VALUE = {
        'AUTO_START': AUTO_START_MASK,
        'DISPLAY': DISPLAY_MASK,
        'KEYPAD': KEYPAD_MASK,
        'WAKEUP': WAKEUP_MASK,
    }

    def __init__(self, _value=None):
        self.__auto_start = True
        self.__display = True
        self.__keypad = True
        self.__wakeup = True

        self.serialize(_value if _value is not None else Features.DEFAULT)

    @property
    def value(self):
        result = 0
        if self.__auto_start:
            result |= Features.AUTO_START_MASK
        if self.__display:
            result |= Features.DISPLAY_MASK
        if self.__keypad:
            result |= Features.KEYPAD_MASK
        if self.__wakeup:
            result |= Features.WAKEUP_MASK

        return [result, 0x00]

    @property
    def type_len(self):
        return 2

    def serialize(self, _value):
        if len(_value) != self.type_len:
            _value = Features.DEFAULT

        value = _value[0] if isinstance(_value[0], int) else int(_value[0], 16)

        if value & Features.AUTO_START_MASK > 0:
            self.__auto_start = True
        else:
            self.__auto_start = False
        if value & Features.DISPLAY_MASK > 0:
            self.__display = True
        else:
            self.__display = False
        if value & Features.KEYPAD_MASK > 0:
            self.__keypad = True
        else:
            self.__keypad = False
        if value & Features.WAKEUP_MASK > 0:
            self.__wakeup = True
        else:
            self.__wakeup = False

    def __str__(self):
        s = '%02X%02X ' % (self.value[0], self.value[1])
        for k, v in Features.VALUE.items():
            s += ' %s:' % k.lower()
            if (self.value[0] & v) > 0:
                s += '1'
            else:
                s += '0'
        return s
