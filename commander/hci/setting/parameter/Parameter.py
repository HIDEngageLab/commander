# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


class Parameter(object):
    def __init__(self, new_value=None, base=10):
        if new_value is not None:
            if base == 10:
                self.__value = new_value
            elif base == 16:
                self.__value = int(str(new_value), 16)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    @value.getter
    def value(self):
        return self.__value
