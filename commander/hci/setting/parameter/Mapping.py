# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


class Mapping:
    """
    mapping parameter
        Change one of the 24 custom mapping table values (modifier, code).
        Keys: 
        - button: keys 0-4 and 5-9, 
        - incremental encoder 1 (up, dn, select) keys: 10-12 
        - incremental encoder 2 (up, dn, select) keys: 13-15
        - joystick 1 (left, right, up, dn) keys: 16-19  
        - joystick 2 (left, right, up, dn) keys: 20-23
        Modifier bit flags: RM RC RS RA LM LC LS LA; (R/L - right/left, MCSA - meta, ctrl, shift, alt)
        Code: value 0x00-0xff
    input:
        hex values:
        KEY MODIFIER CODE
    """

    DEFAULT = [0xff, 0xff, 0xff]

    def __init__(self, _value=None):
        self.__item = [0xff] * self.type_len
        self.serialize(_value if _value is not None else Mapping.DEFAULT)

    @property
    def value(self):
        return self.__item

    def serialize(self, _value):
        if len(_value) < self.type_len:
            _value = _value + [0xff] * (self.type_len - len(_value))
        elif len(_value) > self.type_len:
            _value = _value[:self.type_len]

        value = []
        for item in _value:
            if isinstance(item, str):
                value.append(int(item, 16))
            else:
                value.append(item)

        self.__item = value

    @property
    def type_len(self):
        return 3

    def __str__(self):

        index = self.value[0]
        modifier = self.value[1]
        code = self.value[2]

        s = ' '.join(['%02X' % a for a in self.value])
        s += ' key: %02X (%d),' % (index, index)
        s += ' modifier: %02X (%d),' % (modifier, modifier)
        s += ' code: %02X (%d)' % (code, code)

        return s
