# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


def reset(cmd_line):
    """
    Keypad soft reset
    syntax:
        <ALIAS[, ALIAS[...]]|all> reset [shutdown|format]

        shutdown        soft reset keypad firmware (default option)
        format          reset settings to default values

    Attention: "format" also reset the serial number value.
    """

    try:
        from commander.hci.control.ResetReq import ResetReq
        if len(cmd_line) == 0:
            return ResetReq('shutdown')
        elif len(cmd_line) > 0:
            return ResetReq(cmd_line[0])
        output.show_error('not enough parameter')
    except Exception as msg:
        output.show_failure(msg)

    output.show_doc(reset)
    return None


def gadget(cmd_line):
    """
    Keypad status request
    syntax:
        <ALIAS[, ALIAS[...]]|all> gadget <get|COMMAND>

    parameter:
        get             current operation mode (default option)
        COMMAND         set operation mode with MOUNT, SUSPEND, RESUME and UNMOUNT
    """

    try:
        from commander.hci.control.GadgetReq import GadgetReq
        if len(cmd_line) == 0:
            return GadgetReq('get')
        elif len(cmd_line) > 0:
            return GadgetReq(cmd_line[0])
        output.show_error('not enough parameter')
    except Exception as msg:
        output.show_error(str(msg))

    output.show_doc(gadget)
    return None


def crc_hash(cmd_line):
    """
    hash request

    adapter algorithm calculates a 16 bit hash value from a data array or a string

    syntax:
        <ALIAS[, ALIAS[...]]|all> hash <DATA|'STRING'>

    parameter:
        DATA            hex coded byte string, separated by comma (0x62, 0x6c, 0x61),
                        with spaces (0x62 0x6c 0x61) or compact (626c61)
        STRING          something like 'bla'
    """

    from commander.hci.control.HashReq import HashReq

    try:
        if len(cmd_line) == 0:
            from datetime import datetime
            from commander.hci.GenericCmd import GenericCmd
            data = '\'' + datetime.utcnow().__str__()[-GenericCmd.MAX_PAYLOAD_LEN+2:] + '\''
            return HashReq(data)
        elif len(cmd_line) > 0:
            data = ' '.join(cmd_line).strip()
            return HashReq(data)
        output.show_error('not enough parameter')
    except Exception as msg:
        output.show_error(str(msg))

    output.show_doc(crc_hash)
    return None


def temperature(cmd_line):
    """
    Keypad MCU temperature

    syntax:
        <ALIAS[, ALIAS[...]]|all> temperature [get|alarm MAX_VALUE]

        get             get current temperature (default option)
        alarm           set a "red line" for the temperature max value 
                        (overflow results in an indication)
    """

    try:
        from commander.hci.control.TemperatureReq import TemperatureReq
        if len(cmd_line) == 0:
            return TemperatureReq('get')
        elif len(cmd_line) > 0:
            return TemperatureReq(*cmd_line)
        output.show_error('not enough parameter')
    except Exception as msg:
        output.show_error(str(msg))

    output.show_doc(temperature)
    return None
