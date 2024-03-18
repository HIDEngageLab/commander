# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


def backlight(cmd_line):
    """
    backlight control request

    syntax:
        <ALIAS[, ALIAS[...]]|all> backlight PROGRAM
        <ALIAS[, ALIAS[...]]|all> backlight <set|morph> RRGGBB RRGGBB

        PROGRAM         alert, const, medium, mount, off, slow, suspend or turbo
        set             set the left anr right RGB-values
        morph           morph slowly to the left anr right RGB-values
        RRGGBB          6 digit hex coded RGB color value          
    """

    from commander.hci.feature.BacklightReq import BacklightReq
    try:
        if len(cmd_line) > 0:
            return BacklightReq(*cmd_line)
        output.show_error('not enough parameter')
    except Exception as msg:
        output.show_error(str(msg))

    output.show_doc(backlight)
    return None


def display(cmd_line):
    """
    power request

    syntax:
        <ALIAS[, ALIAS[...]]|all> display clean
        <ALIAS[, ALIAS[...]]|all> display position LINE COLUMN
        <ALIAS[, ALIAS[...]]|all> display font FONT_IDENTIFIER
        <ALIAS[, ALIAS[...]]|all> display icon ICON_IDENTIFIER
        <ALIAS[, ALIAS[...]]|all> display text MESSAGE

    parameter:
        LINE            0-3 
        COLUMN          0-127
        FONT            small, normal, big, huge and symbol
        ICON            frame, logo1, logo2, heart
        MESSAGE         max. 19 bytes long text message        
    """

    from commander.hci.feature.DisplayReq import DisplayReq
    try:
        if len(cmd_line) > 0:
            return DisplayReq(*cmd_line)
        output.show_error('not enough parameter')
    except Exception as msg:
        output.show_error(str(msg))

    output.show_doc(display)
    return None


def gpio(cmd_line):
    """
    GPIO control request

    syntax:
        <ALIAS[, ALIAS[...]]|all> gpio NUMBER <direction|in|out>
        <ALIAS[, ALIAS[...]]|all> gpio NUMBER <value|high|low>
        <ALIAS[, ALIAS[...]]|all> gpio NUMBER <enable|disable>

    parameter:
        NUMBER          0-3 GPIO pin number
        direction       get pis direction
        in, out         set pin direction
        value           get pin value
        high, low       set pin value
        enable, disable control pin level events
    """

    from commander.hci.feature.GpioReq import GpioReq
    try:
        if len(cmd_line) > 1:
            return GpioReq(*cmd_line)        
        output.show_error('not enough parameter')
    except Exception as msg:
        output.show_error(str(msg))

    output.show_doc(gpio)
    return None


def keypad(cmd_line):
    """
    Keypad control request

    send a keypad request to the embedded device

    syntax:
        <ALIAS[, ALIAS[...]]|all> keypad <enable|disable> <hci|hid>
        <ALIAS[, ALIAS[...]]|all> keypad <click|push|press|release> MODIFIER KEY
        <ALIAS[, ALIAS[...]]|all> keypad <set TABLE|get>

    parameter:
        TABLE               CUSTOM, FUNCTIONAL, MULTIMEDIA, NAVIGATION, NUMBER (default) and TELEFON
        MODIFIER            hex value like: 00, added by masks: 
                            +- - - - - - - -+
                             ------+ | | | +--- left ctrl
                                   | | | +----- left shift
                                   | | +------- left alt
                                   | +--------- left meta
                                   +----------- reserved
        KEY                 hex value like 11 (17); 0x00-0x09 (0-9) keys, 0x0a-0x0c (10-12) and 
                            0x0d-0x0f (13-15) wheels I+II up, dn and switch
                            0x10-0x13 (16-19) and 0x14-0x17 (20-23) joystick i+II dn, left, right and up
    """

    from commander.hci.feature.KeypadReq import KeypadReq
    try:
        if len(cmd_line) > 0:
            return KeypadReq(*cmd_line)
        output.show_error('not enough parameter')
    except Exception as msg:
        output.show_error(str(msg))

    output.show_doc(keypad)
    return None
