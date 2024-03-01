# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.HciCommand import HciCommand
from commander.hci import HciCommandAdapter
from commander.hci import HciCommandEvent
from commander.hci import HciCommandMacro
from commander.hci import HciCommandTarget

HciCommand.command_dict['reset'] = HciCommandAdapter.reset
HciCommand.command_dict['status'] = HciCommandAdapter.status
HciCommand.command_dict['temperature'] = HciCommandAdapter.temperature
HciCommand.command_dict['firmware'] = HciCommandAdapter.firmware
HciCommand.command_dict['hardware'] = HciCommandAdapter.hardware
HciCommand.command_dict['identity'] = HciCommandAdapter.identity
HciCommand.command_dict['parameter'] = HciCommandAdapter.parameter
HciCommand.command_dict['key'] = HciCommandAdapter.key

HciCommand.command_dict['event'] = HciCommandEvent.event

HciCommand.command_dict['macro'] = HciCommandMacro.macro

HciCommand.command_dict['power'] = HciCommandTarget.power
HciCommand.command_dict['target'] = HciCommandTarget.target
