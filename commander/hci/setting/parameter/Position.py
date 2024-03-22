# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.utilities.floats import convert_to_bytes, convert_to_long, convert_to_float


class Position:
    """
    MCU position two float (4 byte) values

    input:
        hex, latitude longitude in sec
    """

    DEFAULT = [49.441624, 11.053797]

    def __init__(self, _value=None):
        self.__latitude = 0
        self.__longitude = 0

        _value = _value if _value is not None else Position.DEFAULT
        if len(_value) == 2:
            _value = convert_to_bytes(_value[0]) + \
                convert_to_bytes(_value[1])

        self.serialize(_value)

    @property
    def value(self):
        return convert_to_bytes(self.__latitude) + \
            convert_to_bytes(self.__longitude)

    def serialize(self, _value):
        if len(_value) != self.type_len:
            raise Exception('set position: check payload length')

        self.__latitude = convert_to_float(_value[0:4])
        self.__longitude = convert_to_float(_value[4:8])

    @property
    def type_len(self):
        return 8

    def __str__(self):
        s = ''
        s += '%s ' % ''.join(['%02x' % a for a in self.value[0:4]])
        s += '%s ' % ''.join(['%02x' % a for a in self.value[4:8]])
        s += '(LAT:%7.4f, ' % self.__latitude
        s += 'LON:%7.4f) ' % self.__longitude
        return s
