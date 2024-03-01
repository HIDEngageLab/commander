# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


class UserRegister:
    """
    test register (16 bit for user values)

    input:
        hex
    """

    def __init__(self, value=None):
        if value is not None:
            self.__value = int(value[0], 16) & 0xffff
        else:
            self.__value = 0

    @property
    def value(self):
        return [(self.__value >> 8) & 0xff, self.__value & 0xff]

    def serialize(self, value):
        if len(value) != self.type_len:
            raise Exception('TestRegister setter: check payload length')

        self.__value = (value[0] << 8) + value[1]

    @property
    def type_len(self):
        return 2

    def __str__(self):
        s = '%04X (%d)' % (self.__value, self.__value)
        return s           
