# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd


class KeypadCmd(GenericCmd):
    """
    keypad command base class
    """

    STATE = {
        'PRESS': 0x00,
        'RELEASE': 0x01,
        'CLICK': 0x02,
        'PUSH': 0x03,

        'UNDEFINED': 0xff,
    }

    CONTROL = {
        'BUTTON': 0x01,
        'JOYSTICK_1': 0x04,
        'JOYSTICK_2': 0x05,
        'KEYPAD': 0x06,
        'WHEEL_1': 0x02,
        'WHEEL_2': 0x03,

        'UNDEFINED': 0xff,
    }

    KEY_ID = {
        'KEY_01': 0x00,
        'KEY_02': 0x01,
        'KEY_03': 0x02,
        'KEY_04': 0x03,
        'KEY_05': 0x04,
        'KEY_06': 0x05,
        'KEY_07': 0x06,
        'KEY_08': 0x07,
        'KEY_09': 0x08,
        'KEY_10': 0x09,

        'KEY_70': 0x0a,
        'KEY_71': 0x0b,
        'KEY_72': 0x0c,
        'KEY_73': 0x0d,
        'KEY_74': 0x0e,
        'KEY_75': 0x0f,

        'KEY_80': 0x10,
        'KEY_81': 0x11,
        'KEY_82': 0x12,
        'KEY_83': 0x13,
        'KEY_84': 0x14,
        'KEY_85': 0x15,
        'KEY_86': 0x16,
        'KEY_87': 0x17,

        'UNDEFINED': 0xff,
    }

    TABLE = {
        'CUSTOM': 0x05,
        'FUNCTIONAL': 0x01,
        'MULTIMEDIA': 0x04,
        'NAVIGATION': 0x02,
        'NUMBER': 0x00,
        'TELEFON': 0x03,

        'UNDEFINED': 0xff,
    }

    IDENTIFIER = {
        'HCI': 0x00,
        'HID': 0x01,
        'KEYCODE': 0x02,
        'MAPPING': 0x03,

        'UNDEFINED': 0xff,
    }

    FUNCTION = {
        'DISABLE': GenericCmd.FUNCTION['DISABLE'],
        'ENABLE': GenericCmd.FUNCTION['ENABLE'],
        'GET': GenericCmd.FUNCTION['GET'],
        'SET': GenericCmd.FUNCTION['SET'],
        'CLEAN': GenericCmd.FUNCTION['CLEAN'],

        'CLICK': GenericCmd.FUNCTION['CUSTOM'],
        'PRESS': GenericCmd.FUNCTION['CUSTOM'] + 1,
        'PUSH': GenericCmd.FUNCTION['CUSTOM'] + 2,
        'RELEASE': GenericCmd.FUNCTION['CUSTOM'] + 3,

        'UNDEFINED': 0xff,
    }

    RESULT = {
        'SUCCESS': GenericCmd.RESULT['SUCCESS'],
        'FAILURE': GenericCmd.RESULT['FAILURE'],
        'ERROR': GenericCmd.RESULT['ERROR'],
        'UNKNOWN': GenericCmd.RESULT['UNKNOWN'],
        'UNSUPPORTED': GenericCmd.RESULT['UNSUPPORTED'],

        'UNKNOWN_FUNCTION': GenericCmd.RESULT['CUSTOM'] + 1,
        'UNKNOWN_IDENTIFIER': GenericCmd.RESULT['CUSTOM'],
        'UNKNOWN_SOURCE': GenericCmd.RESULT['CUSTOM'] + 3,
        'WRONG_VALUE': GenericCmd.RESULT['CUSTOM'] + 2,
    }

    @staticmethod
    def show_modifier(_modifier):
        s = ''
        s += 'right '
        s += 'meta:%d ' % (1 if _modifier & 0x80 else 0)
        s += 'alt:%d ' % (1 if _modifier & 0x40 else 0)
        s += 'shift:%d ' % (1 if _modifier & 0x20 else 0)
        s += 'ctrl:%d ' % (1 if _modifier & 0x10 else 0)
        s += 'left '
        s += 'meta:%d ' % (1 if _modifier & 0x08 else 0)
        s += 'alt:%d ' % (1 if _modifier & 0x04 else 0)
        s += 'shift:%d ' % (1 if _modifier & 0x02 else 0)
        s += 'ctrl:%d' % (1 if _modifier & 0x01 else 0)
        return s

    def __init__(self, direction):
        GenericCmd.__init__(self, GenericCmd.COMMANDS['KEYPAD'], direction)
