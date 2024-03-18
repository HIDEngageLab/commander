# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd


class ResetCmd(GenericCmd):

    RESULT = {
        'SUCCESS': 0x00,
        'ERROR': 0x01,
        'CRITICAL_ERROR': 0x02,
        'WATCHDOG': 0x03,
        'PARAMETER_MISSED': 0x04,
        'PARAMETER_RESTORED': 0x05,
        'PARAMETER_RECREATED': 0x06,
        'PARAMETER_BACKUP_CREATED': 0x07,
    }

    FUNCTION = {
        'SHUTDOWN': GenericCmd.FUNCTION['CUSTOM'],
        'FORMAT': GenericCmd.FUNCTION['CUSTOM'] + 1,
    }

    def __init__(self, direction):
        GenericCmd.__init__(self, GenericCmd.COMMANDS['RESET'], direction)
