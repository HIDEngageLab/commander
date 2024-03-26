# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


class Display:
    """
    display parameter
        R I S 
        + - - - - - - +
        | | | +-------+--- reserved
        | | +------------- slides
        | +--------------- inverse
        +----------------- rotate 180 deg.
    input:
        hex byte with bit flags (0:disable, 1:enable) like: e0
    """

    ROTATE_MASK = 0x80
    INVERSE_MASK = 0x40
    SLIDES_MASK = 0x20

    DEFAULT = [ROTATE_MASK | INVERSE_MASK | SLIDES_MASK]

    VALUE = {
        'ROTATE': ROTATE_MASK,
        'INVERSE': INVERSE_MASK,
        'SLIDES': SLIDES_MASK,
    }

    def __init__(self, _value=None):
        self.__rotate = True
        self.__inverse = True
        self.__slides = True
        self.serialize(_value if _value is not None else Display.DEFAULT)

    @property
    def value(self):
        result = 0
        if self.__rotate:
            result |= Display.ROTATE_MASK
        if self.__inverse:
            result |= Display.INVERSE_MASK
        if self.__slides:
            result |= Display.SLIDES_MASK

        return [result]

    def serialize(self, _value):
        if len(_value) != self.type_len:
            _value = Display.DEFAULT

        value = _value[0] if isinstance(_value[0], int) else int(_value[0], 16)

        if value & Display.ROTATE_MASK > 0:
            self.__rotate = True
        else:
            self.__rotate = False

        if value & Display.INVERSE_MASK > 0:
            self.__inverse = True
        else:
            self.__inverse = False

        if value & Display.SLIDES_MASK > 0:
            self.__slides = True
        else:
            self.__slides = False

    @property
    def type_len(self):
        return 1

    def __str__(self):
        s = ''
        s += '%02X ' % (self.value[0])
        for k, v in Display.VALUE.items():
            s += ' %s:' % k.lower()
            if (self.value[0] & v) > 0:
                s += '1'
            else:
                s += '0'
        return s
