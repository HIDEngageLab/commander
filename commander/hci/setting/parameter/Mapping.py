# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


class Mapping:
    """
    mapping parameter
        Custom mapping table, 24 bytes. 
        - button 1-5 and 6-10, 
        - incremental encoder 1 (up, dn, select) and 2 (up, dn, select)
        - joystick 1 (left, right, up, dn) and 2 (left, right, up, dn)
    input:
        24 hex values
    """

    DEFAULT = [0xff, 0xff, 0xff, 0xff, 0xff,
               0xff, 0xff, 0xff, 0xff, 0xff,
               0xff, 0xff, 0xff,
               0xff, 0xff, 0xff,
               0xff, 0xff, 0xff, 0xff,
               0xff, 0xff, 0xff, 0xff]

    def __init__(self, _value=DEFAULT):
        self.__table = [0xff] * self.type_len
        self.serialize(_value if _value is not None else Mapping.DEFAULT)

    @property
    def value(self):
        return self.__table

    def serialize(self, _value):
        if len(_value) != self.type_len:
            _value = Mapping.DEFAULT

        value = []
        for item in _value:
            if isinstance(item, str):
                value.append(int(item, 16))
            else:
                value.append(item)

        self.__table = value

    @property
    def type_len(self):
        return 24

    def __str__(self):
        s = ''
        s += 'mapping: '
        s += ' '.join(['%02X' %a for a in self.__table[0:5]])
        s += ', '
        s += ' '.join(['%02X' %a for a in self.__table[5:10]])
        s += ', '
        s += ' '.join(['%02X' %a for a in self.__table[10:13]])
        s += ', '
        s += ' '.join(['%02X' %a for a in self.__table[13:16]])
        s += ', '
        s += ' '.join(['%02X' %a for a in self.__table[16:20]])
        s += ', '
        s += ' '.join(['%02X' %a for a in self.__table[20:24]])
        return s
