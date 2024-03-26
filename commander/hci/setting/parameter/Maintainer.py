# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


class Maintainer:
    """
    maintainer
        +- - - - - - - -+- - - - - - - -+
        +---+-------+-------------------+
            |       |                   +--- identifier
            |       +----------------------- hardware
            +------------------------------- protocol
    input:
        two proper composed hex values like: 03 ff 
    """

    PROTOCOL_MASK = 0xc0
    HARDWARE_MASK = 0x3c
    IDENTIFIER_MASK_H = 0x03
    IDENTIFIER_MASK_L = 0xff

    DEFAULT = [PROTOCOL_MASK | HARDWARE_MASK |
               IDENTIFIER_MASK_H, IDENTIFIER_MASK_L]

    VALUE = {
        'PROTOCOL': PROTOCOL_MASK,
        'HARDWARE': HARDWARE_MASK,
        'IDENTIFIER': [IDENTIFIER_MASK_H, IDENTIFIER_MASK_H],
    }

    def __init__(self, _value=None):
        self.__protocol = 0
        self.__hardware = 0
        self.__identifier = [0, 0]

        self.serialize(_value if _value is not None else Maintainer.DEFAULT)

    @property
    def value(self):
        return [self.__protocol | self.__hardware | self.__identifier[0], self.__identifier[1]]

    @property
    def protocol(self):
        return ((self.__protocol & Maintainer.PROTOCOL_MASK) >> 6)

    @property
    def hardware(self):
        return ((self.__hardware & Maintainer.HARDWARE_MASK) >> 2) & 0x0f

    @property
    def identifier(self):
        return ((self.__identifier[0] & Maintainer.IDENTIFIER_MASK_H) << 8) + self.__identifier[1]

    @property
    def type_len(self):
        return 2

    def serialize(self, _value):
        if len(_value) != self.type_len:
            _value = Maintainer.DEFAULT

        value = []
        for item in _value:
            if isinstance(item, str):
                value.append(int(item, 16))
            else:
                value.append(item)

        self.__protocol = value[0] & Maintainer.PROTOCOL_MASK
        self.__hardware = value[0] & Maintainer.HARDWARE_MASK
        self.__identifier[0] = value[0] & Maintainer.IDENTIFIER_MASK_H
        self.__identifier[1] = value[1] & Maintainer.IDENTIFIER_MASK_L

    def __str__(self):
        s = ''
        s += '%02X%02X protocol:%d, hw:%d, identifier:%d' % \
             (self.value[0], self.value[1], self.protocol,
              self.hardware, self.identifier)
        return s
