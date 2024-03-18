# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


class UserRegister:
    """
    user register (16 bit for user values)

    input:
        two hex bytes, like: ab cd
    """

    DEFAULT = [0, 0]

    def __init__(self, _value=DEFAULT):
        self.__value = UserRegister.DEFAULT
        self.serialize(_value)

    @property
    def value(self):
        return self.__value

    def serialize(self, _value):
        if len(_value) != self.type_len:
            self.__value = UserRegister.DEFAULT

        self.__value = []
        for item in _value:
            if isinstance(item, str):
                self.__value.append(int(item, 16))
            else:
                self.__value.append(item)

    @property
    def type_len(self):
        return 2

    def __str__(self):
        s = '%02X%02X ' % (self.__value[0], self.__value[1])
        return s
