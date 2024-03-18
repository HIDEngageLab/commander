# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


class GenericParam(object):
    from commander.hci.setting.parameter.Backlight import Backlight
    from commander.hci.setting.parameter.Display import Display
    from commander.hci.setting.parameter.Features import Features
    from commander.hci.setting.parameter.Keypad import Keypad
    from commander.hci.setting.parameter.Maintainer import Maintainer
    from commander.hci.setting.parameter.Mapping import Mapping
    from commander.hci.setting.parameter.Position import Position
    from commander.hci.setting.parameter.SerialNumber import SerialNumber
    from commander.hci.setting.parameter.UserRegister import UserRegister

    PARAM_ID = {
        'BACKLIGHT': 0xA1,
        'DISPLAY': 0xA3,
        'FEATURES': 0x51,
        'KEYPAD': 0xA2,
        'MAINTAINER': 0x23,
        'MAPPING': 0xB0,
        'POSITION': 0x24,
        'SERIAL_NUMBER': 0x11,
        'USER': 0x70,
    }

    PARAM = {'MAINTAINER': {}, 'ADMINISTRATOR': {}, 'USER': {}}
    PARAM['MAINTAINER']['BACKLIGHT'] = Backlight
    PARAM['MAINTAINER']['DISPLAY'] = Display
    PARAM['MAINTAINER']['FEATURES'] = Features
    PARAM['MAINTAINER']['KEYPAD'] = Keypad
    PARAM['MAINTAINER']['MAINTAINER'] = Maintainer
    PARAM['MAINTAINER']['MAPPING'] = Mapping
    PARAM['USER']['POSITION'] = Position
    PARAM['MAINTAINER']['SERIAL_NUMBER'] = SerialNumber
    PARAM['USER']['USER'] = UserRegister

    def __init__(self):
        pass

    # @staticmethod
    # def check_param(identifier):
    #     from commander.hci.setting.parameter.GenericParam import GenericParam
    #     if identifier == GenericParam.PARAM_ID['BACKLIGHT']:
    #         from commander.hci.setting.parameter.Backlight import Backlight
    #         return Backlight()
    #     elif identifier == GenericParam.PARAM_ID['DISPLAY']:
    #         from commander.hci.setting.parameter.Display import Display
    #         return Display()
    #     elif identifier == GenericParam.PARAM_ID['FEATURES']:
    #         from commander.hci.setting.parameter.Features import Features
    #         return Features()
    #     elif identifier == GenericParam.PARAM_ID['KEYPAD']:
    #         from commander.hci.setting.parameter.Keypad import Keypad
    #         return Keypad()
    #     elif identifier == GenericParam.PARAM_ID['MAINTAINER']:
    #         from commander.hci.setting.parameter.Maintainer import Maintainer
    #         return Maintainer()
    #     elif identifier == GenericParam.PARAM_ID['MAPPING']:
    #         from commander.hci.setting.parameter.Mapping import Mapping
    #         return Maintainer()
    #     elif identifier == GenericParam.PARAM_ID['POSITION']:
    #         from commander.hci.setting.parameter.Position import Position
    #         return Position()
    #     elif identifier == GenericParam.PARAM_ID['SERIAL_NUMBER']:
    #         from commander.hci.setting.parameter.SerialNumber import SerialNumber
    #         return SerialNumber()
    #     elif identifier == GenericParam.PARAM_ID['USER']:
    #         from commander.hci.setting.parameter.UserRegister import UserRegister
    #         return UserRegister()
    #     return None

    @staticmethod
    def list_all():
        from commander.utilities.PrettyPrint import DLINE, SLINE, sp, wd, DNCON, CRCON, UPCON, VDELIM
        output.show_text('parameter list')
        for operation, paramlist in sorted(GenericParam.PARAM.items()):
            if len(paramlist) > 0:
                output.show_text(DLINE * wd)
                output.show_text('operation: %s' % operation)
                output.show_text(SLINE * sp + DNCON + SLINE * (wd - sp - 1))
                output.show_text('%-15s%c%s' %
                                 ('name', VDELIM, 'default value'))
                output.show_text(SLINE * sp + CRCON + SLINE * (wd - sp - 1))
                for name, param in sorted(paramlist.items()):
                    output.show_text('%-15s%c%s' % (name, VDELIM, param()))
                output.show_text(SLINE * sp + UPCON + SLINE * (wd - sp - 1))

    @staticmethod
    def search(name):
        for parameter_list in GenericParam.PARAM.values():
            for identifier, parameter in parameter_list.items():
                if identifier == name:
                    return parameter
        return None
