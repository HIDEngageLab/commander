# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.utilities.PrettyPrint import VDELIM

from commander.hci.control.GadgetCfm import GadgetCfm
from commander.hci.control.GadgetInd import GadgetInd
from commander.hci.control.HashCfm import HashCfm
from commander.hci.control.ProtocolInd import ProtocolInd
from commander.hci.control.ResetCfm import ResetCfm
from commander.hci.control.ResetInd import ResetInd
from commander.hci.control.TemperatureCfm import TemperatureCfm
from commander.hci.control.TemperatureInd import TemperatureInd
from commander.hci.feature.BacklightCfm import BacklightCfm
from commander.hci.feature.DisplayCfm import DisplayCfm
from commander.hci.feature.GpioCfm import GpioCfm
from commander.hci.feature.GpioInd import GpioInd
from commander.hci.feature.KeypadCfm import KeypadCfm
from commander.hci.feature.KeypadInd import KeypadInd
from commander.hci.setting.IdentityCfm import IdentityCfm
from commander.hci.setting.ParameterCfm import ParameterCfm


def check_command(_command, _payload):
    if _command == GenericCmd.COMMANDS['BACKLIGHT'] + GenericCmd.DIRECTION['CFM']:
        return BacklightCfm(_payload)
    elif _command == GenericCmd.COMMANDS['DISPLAY'] + GenericCmd.DIRECTION['CFM']:
        return DisplayCfm(_payload)
    elif _command == GenericCmd.COMMANDS['GADGET'] + GenericCmd.DIRECTION['CFM']:
        return GadgetCfm(_payload)
    elif _command == GenericCmd.COMMANDS['GADGET'] + GenericCmd.DIRECTION['IND']:
        return GadgetInd(_payload)
    elif _command == GenericCmd.COMMANDS['GPIO'] + GenericCmd.DIRECTION['CFM']:
        return GpioCfm(_payload)
    elif _command == GenericCmd.COMMANDS['GPIO'] + GenericCmd.DIRECTION['IND']:
        return GpioInd(_payload)
    elif _command == GenericCmd.COMMANDS['HASH'] + GenericCmd.DIRECTION['CFM']:
        return HashCfm(_payload)
    elif _command == GenericCmd.COMMANDS['IDENTITY'] + GenericCmd.DIRECTION['CFM']:
        return IdentityCfm(_payload)
    elif _command == GenericCmd.COMMANDS['KEYPAD'] + GenericCmd.DIRECTION['IND']:
        return KeypadInd(_payload)
    elif _command == GenericCmd.COMMANDS['KEYPAD'] + GenericCmd.DIRECTION['CFM']:
        return KeypadCfm(_payload)
    elif _command == GenericCmd.COMMANDS['PARAMETER'] + GenericCmd.DIRECTION['CFM']:
        return ParameterCfm(_payload)
    elif _command == GenericCmd.COMMANDS['PROTOCOL'] + GenericCmd.DIRECTION['IND']:
        return ProtocolInd(_payload)
    elif _command == GenericCmd.COMMANDS['RESET'] + GenericCmd.DIRECTION['CFM']:
        return ResetCfm(_payload)
    elif _command == GenericCmd.COMMANDS['RESET'] + GenericCmd.DIRECTION['IND']:
        return ResetInd(_payload)
    elif _command == GenericCmd.COMMANDS['TEMPERATURE'] + GenericCmd.DIRECTION['CFM']:
        return TemperatureCfm(_payload)
    elif _command == GenericCmd.COMMANDS['TEMPERATURE'] + GenericCmd.DIRECTION['IND']:
        return TemperatureInd(_payload)
    return None


class HciParser(GenericCmd):
    """
    messages factory
    """

    def __init__(self, payload, alias=None):
        GenericCmd.__init__(self, payload[0] & 0xfc, payload[0] & 0x03)

        self.__alias = alias

        if len(payload[1]) == 0:
            print('payload empty')
            payload[1] = []

        self.__payload = payload
        self.__command = payload[0]
        self.__data = payload[1][0:]
        self.command_obj = check_command(self.__command,
                                         self.__payload)

    @property
    def data(self):
        return self.__data

    def get_command(self):
        return self.command_obj

    def __str__(self):
        if self.command_obj is not None:
            s = self.command_obj.__str__()

        else:
            # emergency solution: command is unknown, print bytes
            s = ''
            s += '%-20s%c %02X %s\n' % ('command', VDELIM,
                                        self.__command, self.str_command(self.__command))
            if len(self.__data) > 0:
                s += '%-20s%c %s' % ('data', VDELIM,
                                     ''.join('%02X ' % self.__data[i] for i in range(0, len(self.__data))))

        return s
