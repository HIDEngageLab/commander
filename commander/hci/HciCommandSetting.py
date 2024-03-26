# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


def firmware(cmd_line):
    """
    Keypad firmware revision request

    syntax:
        <ALIAS[, ALIAS[...]]|all> firmware
    """

    from commander.hci.setting.IdentityReq import IdentityReq
    return IdentityReq('get', 'firmware')


def hardware(cmd_line):
    """
    Keypad hardware revision request

    syntax:
        <ALIAS[, ALIAS[...]]|all> hardware
    """

    from commander.hci.setting.IdentityReq import IdentityReq
    return IdentityReq('get', 'hardware')


def serial(cmd_line):
    """
    Keypad serial number

    syntax:
        <ALIAS[, ALIAS[...]]|all> serial [get|set NUMBER]

    parameter:
        get             returns permanent stored serial number (default option)
        set             store NUMBER as a new serial number
        NUMBER          12 hex bytes long array like: 00 11 22 33 44 55 66 77 88 99 aa bb

    Attention: please change the serial number only if you exactly know, what you do.
    """

    from commander.hci.GenericCmd import GenericCmd
    from commander.hci.setting.IdentityCmd import IdentityCmd
    from commander.hci.setting.IdentityReq import IdentityReq
    if len(cmd_line) == 0:
        return IdentityReq('get', 'serial')
    elif len(cmd_line) > 0:
        return IdentityReq(cmd_line[0], 'serial', cmd_line[1:])
    output.show_error('not enough parameter')
    output.show_doc(identity)
    return None


def identity(cmd_line):
    """
    Keypad application identity

    syntax:
        <ALIAS[, ALIAS[...]]|all> identity <product|platform>

    parameter:
        product         application identifier
        platform        platform configuration
    """

    from commander.hci.GenericCmd import GenericCmd
    from commander.hci.setting.IdentityCmd import IdentityCmd
    from commander.hci.setting.IdentityReq import IdentityReq
    if len(cmd_line) > 0:
        return IdentityReq('get', cmd_line[0])
    output.show_error('not enough parameter')
    output.show_doc(identity)
    return None


def parameter(cmd_line):
    """
    HIL adapter parameter request

    syntax:
        <ALIAS[, ALIAS[...]]|all> parameter [list|[help] PARAMETER|get PARAMETER|set PARAMETER VALUE>]

    parameter:
        list            shows all available parameters (default option)
        help            prints some documentation to a parameter
        PARAMETER       parameter name ("list" option)
        get             returns permanent stored parameter value for PARAMETER
        set VALUE       set parameter value to VALUE and store it permanently
                        attention: command reset current value to the stored value
    """

    from commander.hci.setting.ParameterReq import ParameterReq
    from commander.hci.setting.parameter.GenericParam import GenericParam
    if len(cmd_line) == 0:
        GenericParam.list_all()
        return None
    elif len(cmd_line) == 1:
        sub_cmd = cmd_line[0].upper().strip()
        if sub_cmd == 'LIST':
            GenericParam.list_all()
            return None
        else:
            value = GenericParam.search(sub_cmd)
            if value is not None:
                output.show_text('Parameter:')
                output.show_doc(value)
                return None
    elif len(cmd_line) > 1:
        sub_cmd = cmd_line[0].upper().strip()
        if sub_cmd == 'HELP':
            identifier = cmd_line[1].upper().strip()
            value = GenericParam.search(identifier)
            if value is not None:
                output.show_text('Parameter:')
                output.show_doc(value)
                return None
        else:
            request = ParameterReq(cmd_line[0], cmd_line[1], cmd_line[2:])
            return request
    else:
        output.show_error('not enough parameter')


    output.show_doc(parameter)
    return None
