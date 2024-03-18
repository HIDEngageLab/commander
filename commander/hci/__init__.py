# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.HciCommand import HciCommand
from commander.hci import HciCommandControl
from commander.hci import HciCommandFeature
from commander.hci import HciCommandSetting

HciCommand.command_dict['gadget'] = HciCommandControl.gadget
HciCommand.command_dict['hash'] = HciCommandControl.crc_hash
HciCommand.command_dict['reset'] = HciCommandControl.reset
HciCommand.command_dict['temperature'] = HciCommandControl.temperature

HciCommand.command_dict['backlight'] = HciCommandFeature.backlight
HciCommand.command_dict['display'] = HciCommandFeature.display
HciCommand.command_dict['gpio'] = HciCommandFeature.gpio
HciCommand.command_dict['keypad'] = HciCommandFeature.keypad

HciCommand.command_dict['firmware'] = HciCommandSetting.firmware
HciCommand.command_dict['hardware'] = HciCommandSetting.hardware
HciCommand.command_dict['identity'] = HciCommandSetting.identity
HciCommand.command_dict['parameter'] = HciCommandSetting.parameter
HciCommand.command_dict['serial'] = HciCommandSetting.serial
