# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.utilities.floats import convert_to_long, convert_to_float


class Position:
    """
    node position two 4 byte long values

    input:
        hex, latitude longitude in sec
    """

    DEFAULT = None

    def __init__(self, value=DEFAULT):
        if value is None:
            self._latitude = 0
            self._longitude = 0
        else:
            if len(value) == 2:
                self._latitude = convert_to_long(float(value[0]))
                self._longitude = convert_to_long(float(value[1]))
            else:
                raise Exception('Position setter: enter two hex values')

    @property
    def value(self):
        v1 = [(self._latitude >> 24) & 0xff,
              (self._latitude >> 16) & 0xff,
              (self._latitude >> 8) & 0xff,
              self._latitude & 0xff]

        v2 = [(self._longitude >> 24) & 0xff,
              (self._longitude >> 16) & 0xff,
              (self._longitude >> 8) & 0xff,
              self._longitude & 0xff]

        return v1 + v2

    def serialize(self, value):
        if len(value) != self.type_len:
            raise Exception('Position setter: check payload length')

        self._latitude = (value[0] << 24) + (value[1] <<
                                             16) + (value[2] << 8) + value[3]
        self._longitude = (value[4] << 24) + \
            (value[5] << 16) + (value[6] << 8) + value[7]

    @property
    def type_len(self):
        return 8

    def __str__(self):
        s = ''
        s += '%08X ' % self._latitude
        s += '%08X ' % self._longitude
        s += '(LAT:%7.4f, ' % convert_to_float(self.value[0:4])
        s += 'LON:%7.4f) ' % convert_to_float(self.value[4:8])
        return s
