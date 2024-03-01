# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd


class ParamCmd(GenericCmd):
    FUNCTION = {'GET': 0x00,
                'SET': 0x01}

    # buff with mask 0x80 = buffer length
    TYPE = {'BYTE': 0x01,
            'WORD': 0x02,
            'LONG': 0x04,
            'BUFF': 0x80}

    # Contents of FUNC invalid
    # Contents of PRM invalid
    RESULT = {'SUCCESS': 0x00,
              'FAILURE': 0x01,
              'UNKNOWN': 0x02,
              'UNSUPPORTED': 0x03,
              'STORAGE_ERROR': 0x04}

    def __init__(self, direction):
        GenericCmd.__init__(self, GenericCmd.COMMANDS['PARAMETER'], direction)

    @staticmethod
    def str_type(field, dictionary=TYPE):
        co = ''
        for v, k in dictionary.items():
            # print v,k
            if k & 0x80:
                co += 'BUFF[%d]' % (k & ~0x80)
            elif (k & ~0x80) == field:
                co += v
                break
        return co
