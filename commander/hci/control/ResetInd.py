# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.control.ResetCmd import ResetCmd


class ResetInd(ResetCmd):
    """
    reset indication
    """

    RESULT = {'SUCCESS': 0x00,
              'ERROR': 0x01,
              'CRITICAL_ERROR': 0x02,
              'WATCHDOG': 0x03,
              'PARAMETER_MISSED': 0x04,
              'PARAMETER_RESTORED': 0x05,
              'PARAMETER_RECREATED': 0x06,
              'PARAMETER_BACKUP_CREATED': 0x07}

    def __init__(self, command):
        ResetCmd.__init__(self, GenericCmd.DIRECTION['IND'])

        if self.command != command[0]:
            raise 'ResetInd:unknown command id: %04X' % command[0]

        payload = command[1]
        if len(payload) == 0:
            print('payload empty')
            payload = [0]

        self.__result = payload[0]

    @property
    def result(self):
        return self.__result

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS, '_'): {
                'RESULT': GenericCmd.str_field(self.result, ResetInd.RESULT),
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % (
            'command', VDELIM, self.command, GenericCmd.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s' % ('result', VDELIM, self.result,
                                  GenericCmd.str_field(self.result, ResetInd.RESULT))
        return s
