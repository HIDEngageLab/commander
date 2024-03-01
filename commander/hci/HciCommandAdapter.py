# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


def reset(cmd_line):
    """
    HIL adapter reset request

    syntax:
        <ALIAS[, ALIAS[...]]|all> reset <[SHUTDOWN]|FORMAT>

        SHUTDOWN        optional
        FORMAT          reset stored adapter parameter to the default values
    """

    from commander.hci.control.ResetReq import ResetReq
    if len(cmd_line) == 1:
        return ResetReq('shutdown')
    elif len(cmd_line) > 1:
        sub_cmd = cmd_line[1].upper().strip()
        from commander.hci.GenericCmd import GenericCmd
        from commander.hci.control.ResetCmd import ResetCmd
        if GenericCmd.find_field(sub_cmd, ResetCmd.FUNCTION):
            return ResetReq(sub_cmd)

    output.show_doc(reset)
    return None


def status(cmd_line):
    """
    HIL adapter status request
    syntax:
        <ALIAS[, ALIAS[...]]|all> status <get|record|play|start|stop>

    parameter:
        get             current operation mode
        record, play    set the record or play operation
        start, stop     set and reset application mode
    """

    if len(cmd_line) > 1:
        sub_cmd = cmd_line[1].upper().strip()
        from commander.hci.GenericCmd import GenericCmd
        from commander.hci.control.StatusCmd import StatusCmd
        from commander.hci.control.StatusReq import StatusReq
        if GenericCmd.find_field(sub_cmd, StatusCmd.FUNCTION):
            if sub_cmd in ['GET', 'START', 'STOP', 'RECORD', 'PLAY']:
                return StatusReq(sub_cmd)

    output.show_doc(status)
    return None


def temperature(cmd_line):
    """
    HIL adapter temperature request

    syntax:
        <ALIAS[, ALIAS[...]]|all> temperature
    """

    from commander.hci.control.TemperatureReq import TemperatureReq
    return TemperatureReq()


def firmware(cmd_line):
    """
    HIL adapter firmware revision request

    syntax:
        <ALIAS[, ALIAS[...]]|all> firmware
    """

    from commander.hci.setting.FirmwareReq import FirmwareReq
    return FirmwareReq()


def hardware(cmd_line):
    """
    HIL adapter hardware revision request

    syntax:
        <ALIAS[, ALIAS[...]]|all> hardware
    """

    from commander.hci.setting.HardwareReq import HardwareReq
    return HardwareReq()


def identity(cmd_line):
    """
    HIL adapter identity request

    syntax:
        <ALIAS[, ALIAS[...]]|all> identity <[serial]|platform>

    parameter:
        serial          optional, is a part of the node serial number
        platform        hardware platform identifier
    """

    from commander.hci.GenericCmd import GenericCmd
    from commander.hci.setting.IdentityCmd import IdentityCmd
    from commander.hci.setting.IdentityReq import IdentityReq
    if len(cmd_line) == 0:
        if GenericCmd.find_field(IdentityCmd.PART['SERIAL'], IdentityCmd.PART):
            return IdentityReq(sub_cmd)
    elif len(cmd_line) > 1:
        sub_cmd = cmd_line[1].upper().strip()
        if GenericCmd.find_field(sub_cmd, IdentityCmd.PART):
            return IdentityReq(sub_cmd)

    output.show_doc(identity)
    return None


def parameter(cmd_line):
    """
    HIL adapter parameter request

    syntax:
        <ALIAS[, ALIAS[...]]|all> parameter <list|PARAMETER <get|set VALUE>>

    parameter:
        list            shows all available parameters
        PARAMETER       parameter name ("list" option)
        get             returns permanent stored parameter value for PARAMETER
        set VALUE       set parameter value to VALUE and store it permanently
                        attention: command reset current value to the stored value
    """

    if len(cmd_line) > 1:
        sub_cmd = cmd_line[1].upper().strip()

        from commander.hci.setting.ParamReq import ParamReq
        from commander.hci.setting.parameter.GenericParam import GenericParam

        if sub_cmd == 'LIST':
            GenericParam.list_all()
            return None
        else:
            identifier = sub_cmd.strip().upper()
            parameter = GenericParam.search(identifier)
            if parameter is None:
                output.show_text('parameter %s not found' % identifier)
                return None

            if len(cmd_line) > 2:
                sub_cmd = cmd_line[2].upper().strip()

                if sub_cmd == 'GET':
                    p = parameter()
                    return ParamReq(identifier, sub_cmd, p)

                elif sub_cmd == 'SET' or sub_cmd == 'SAVE':
                    if len(cmd_line) > 3:
                        value = cmd_line[3:]
                        p = parameter(value)
                        return ParamReq(identifier, sub_cmd, p)

            output.show_text('Parameter:')
            output.show_doc(parameter)
            from commander.utilities.PrettyPrint import doctrim
            output.show_text(doctrim('Default: ' + parameter().__str__()))
            return None

    output.show_doc(parameter)
    return None


def key(cmd_line):
    """
    key request

    adapter algorithm calculates a 32 bit hash value from a data array or a string

    syntax:
        <ALIAS[, ALIAS[...]]|all> key <DATA|'STRING'>

    parameter:
        DATA            hex coded byte string, separated by comma (0x62, 0x6c, 0x61),
                        with spaces (0x62 0x6c 0x61) or compact (626c61)
        STRING          something like 'bla'
    """

    if len(cmd_line) > 1:
        cmd_line = [cmd_line[0], ' '.join(cmd_line[1:]).strip()]
        if len(cmd_line) == 2:
            data = cmd_line[1]
            from commander.hci.feature.KeyReq import KeyReq
            return KeyReq(data)

    output.show_doc(key)
    return None
