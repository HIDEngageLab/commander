# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd


class HardwareCmd(GenericCmd):

    RESULT = {'SUCCESS': 0x00,
              'FAILURE': 0x01,
              'UNKNOWN': 0x02,
              'UNSUPPORTED': 0x03}

    def __init__(self, _direction):
        GenericCmd.__init__(self, GenericCmd.COMMANDS['HARDWARE'], _direction)
