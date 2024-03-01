# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.HciStatusInd import HciStatusInd
from commander.hci.setting.FirmwareCfm import FirmwareCfm
from commander.hci.setting.HardwareCfm import HardwareCfm
from commander.hci.setting.IdentityCfm import IdentityCfm
from commander.hci.setting.ParamCfm import ParamCfm
from commander.hci.control.PowerCfm import PowerCfm
from commander.hci.control.PowerInd import PowerInd
from commander.hci.control.ResetInd import ResetInd
from commander.hci.control.StatusCfm import StatusCfm
from commander.hci.control.StatusInd import StatusInd
from commander.hci.control.TargetBootCfm import TargetBootCfm
from commander.hci.control.TargetResetCfm import TargetResetCfm
from commander.hci.control.TemperatureCfm import TemperatureCfm
from commander.hci.control.TemperatureInd import TemperatureInd
from commander.hci.feature.EventCfm import EventCfm
from commander.hci.feature.EventInd import EventInd
from commander.hci.feature.KeyCfm import KeyCfm
from commander.hci.feature.MacroCleanCfm import MacroCleanCfm
from commander.hci.feature.MacroLoadCfm import MacroLoadCfm
from commander.hci.feature.MacroLoadInd import MacroLoadInd
from commander.hci.feature.MacroStoreCfm import MacroStoreCfm
from commander.hci.feature.MacroStoreInd import MacroStoreInd
from commander.utilities.PrettyPrint import VDELIM


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

        self.value_obj = None
        self.command_obj = self.__check_command()

    @property
    def data(self):
        return self.__data

    def __check_command(self):
        if self.__command == GenericCmd.COMMANDS['BACKLIGHT'] + GenericCmd.DIRECTION['CFM']:
            return PowerCfm(self.__payload)
        elif self.__command == GenericCmd.COMMANDS['DISPLAY'] + GenericCmd.DIRECTION['CFM']:
            return MacroStoreCfm(self.__payload)
        elif self.__command == GenericCmd.COMMANDS['GADGET'] + GenericCmd.DIRECTION['CFM']:
            return StatusCfm(self.__payload)
        elif self.__command == GenericCmd.COMMANDS['GADGET'] + GenericCmd.DIRECTION['IND']:
            return StatusInd(self.__payload)
        elif self.__command == GenericCmd.COMMANDS['GPIO'] + GenericCmd.DIRECTION['CFM']:
            return TargetBootCfm(self.__payload)
        elif self.__command == GenericCmd.COMMANDS['GPIO'] + GenericCmd.DIRECTION['IND']:
            return TargetBootCfm(self.__payload)
        elif self.__command == GenericCmd.COMMANDS['HASH'] + GenericCmd.DIRECTION['CFM']:
            return KeyCfm(self.__payload)
        elif self.__command == GenericCmd.COMMANDS['IDENTITY'] + GenericCmd.DIRECTION['CFM']:
            return IdentityCfm(self.__payload)
        elif self.__command == GenericCmd.COMMANDS['KEYPAD'] + GenericCmd.DIRECTION['IND']:
            return EventInd(self.__payload)
        elif self.__command == GenericCmd.COMMANDS['KEYPAD'] + GenericCmd.DIRECTION['CFM']:
            return EventCfm(self.__payload)
        elif self.__command == GenericCmd.COMMANDS['PARAMETER'] + GenericCmd.DIRECTION['CFM']:
            param_obj = ParamCfm(self.__payload)
            if param_obj is not None:
                self.value_obj = self.__check_param(param_obj.identifier)
                if self.value_obj is not None:
                    self.value_obj.serialize(param_obj.value)
            return param_obj
        elif self.__command == GenericCmd.COMMANDS['PROTOCOL'] + GenericCmd.DIRECTION['IND']:
            return HciStatusInd(self.__payload)
        elif self.__command == GenericCmd.COMMANDS['RESET'] + GenericCmd.DIRECTION['IND']:
            return ResetInd(self.__payload)
        elif self.__command == GenericCmd.COMMANDS['TEMPERATURE'] + GenericCmd.DIRECTION['CFM']:
            return TemperatureCfm(self.__payload)
        elif self.__command == GenericCmd.COMMANDS['TEMPERATURE'] + GenericCmd.DIRECTION['IND']:
            return TemperatureInd(self.__payload)
        return None

    def __check_param(self, identifier):
        from commander.hci.setting.parameter.GenericParam import GenericParam
        if identifier == GenericParam.PARAM_ID['BACKLIGHT']:
            from commander.hci.setting.parameter.Backlight import Backlight
            return Backlight()
        elif identifier == GenericParam.PARAM_ID['DISPLAY']:
            from commander.hci.setting.parameter.Display import Display
            return Display()
        elif identifier == GenericParam.PARAM_ID['FEATURES']:
            from commander.hci.setting.parameter.Features import Features
            return Features()
        elif identifier == GenericParam.PARAM_ID['KEYPAD']:
            from commander.hci.setting.parameter.Keypad import Keypad
            return Keypad()
        elif identifier == GenericParam.PARAM_ID['MAINTAINER']:
            from commander.hci.setting.parameter.Maintainer import Maintainer
            return Maintainer()
        elif identifier == GenericParam.PARAM_ID['MAPPING']:
            from commander.hci.setting.parameter.Mapping import Mapping
            return Maintainer()
        elif identifier == GenericParam.PARAM_ID['POSITION']:
            from commander.hci.setting.parameter.Position import Position
            return Position()
        elif identifier == GenericParam.PARAM_ID['SERIAL_NUMBER']:
            from commander.hci.setting.parameter.SerialNumber import SerialNumber
            return SerialNumber()
        elif identifier == GenericParam.PARAM_ID['USER']:
            from commander.hci.setting.parameter.UserRegister import UserRegister
            return UserRegister()
        return None

    def get_command(self):
        return self.command_obj

    def __str__(self):
        if self.command_obj is not None:
            s = self.command_obj.__str__()

            if self.value_obj is not None:
                s += ' ' + self.value_obj.__str__()

        else:
            # emergency solution: command is unknown, print bytes
            s = ''
            s += '%-20s%c %02X %s\n' % ('command', VDELIM,
                                        self.__command, self.str_command(self.__command))
            if len(self.__data) > 0:
                s += '%-20s%c %s' % ('data', VDELIM,
                                     ''.join('%02X ' % self.__data[i] for i in range(0, len(self.__data))))

        return s
