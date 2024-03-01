# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


class Maintainer:
    """
    maintainer

    +- - - - - - - -+
        ------+ --+ --+
            |   |   +--- Firmware
            |   +------- Hardware
            +----------- Maintainer

    input:
        hex value like: fe
    """

    def __init__(self, value=None):
        if value is None:
            self.__value = 0
        else:
            self.__value = int(value[0], 16)

    @property
    def value(self):
        return [self.__value]

    @property
    def maintainer(self):
        return (self.__value >> 4)

    @property
    def hardware(self):
        return (self.__value >> 2) & 0x03

    @property
    def protocol(self):
        return (self.__value) & 0x03

    @property
    def type_len(self):
        return 1

    def serialize(self, value):
        if len(value) != self.type_len:
            raise Exception('Maintainer setter: check payload length')

        self.__value = value[0]

    def __str__(self):
        s = ''
        s += '%02X maintainer:%d, hw:%d, protocol:%d' % \
             (self.__value, self.maintainer, self.hardware, self.protocol)
        return s
