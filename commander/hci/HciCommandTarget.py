# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


def power(cmd_line):
    """
    power request

    syntax:
        <ALIAS[, ALIAS[...]]|all> power get
        <ALIAS[, ALIAS[...]]|all> power observer set VOLTAGE LOW_LIMIT
        <ALIAS[, ALIAS[...]]|all> power observer reset VOLTAGE
        <ALIAS[, ALIAS[...]]|all> power observer interval MS

    parameter:
        VOLTAGE         <1V8|3V2|5V0|SER_VBUS>
        LOW_LIMIT       float value (with 0<limit<voltage)
        HIGH_LIMIT      float value (with voltage<limit)
        MS              check interval in ms
    """

    from commander.hci.control.PowerReq import PowerReq
    if len(cmd_line) > 1:
        sub_cmd = cmd_line[1].upper().strip()
        if sub_cmd == 'GET':
            return PowerReq(sub_cmd, None)
        elif sub_cmd == 'OBSERVER':
            if len(cmd_line) > 2:
                observer_cmd = cmd_line[2].upper().strip()
                if observer_cmd == 'SET':
                    return PowerReq('OBSERVER_SET', cmd_line[3:])
                elif observer_cmd == 'RESET':
                    return PowerReq('OBSERVER_RESET', cmd_line[3:])
                elif observer_cmd == 'INTERVAL':
                    return PowerReq('OBSERVER_INTERVAL', cmd_line[3:])

    output.show_doc(power)
    return None


def target(cmd_line):
    """
    target restart request
    start target in 50ms after stop

    syntax:
        <ALIAS[, ALIAS[...]]|all> target restart


    toggle target reset button

    syntax:
        <ALIAS[, ALIAS[...]]|all> target reset <START|STOP>

        START           set the reset state (push reset button)
        STOP            release the reset state (reset button)
    """

    if len(cmd_line) > 1:
        sub_cmd = cmd_line[1].upper().strip()

        from commander.hci.control.TargetResetCmd import TargetResetCmd
        from commander.hci.control.TargetResetReq import TargetResetReq
        from commander.hci.control.TargetBootCmd import TargetBootCmd
        from commander.hci.control.TargetBootReq import TargetBootReq

        from commander.hci.GenericCmd import GenericCmd
        if sub_cmd == 'RESET':
            if len(cmd_line) > 2:
                sub_cmd = cmd_line[2].upper().strip()
                if GenericCmd.find_field(sub_cmd, TargetResetCmd.FUNCTION):
                    return TargetResetReq(sub_cmd)

            output.show_doc(target)
            return None

        elif sub_cmd == 'RESTART':
            if GenericCmd.find_field(sub_cmd, TargetResetCmd.FUNCTION):
                return TargetResetReq(sub_cmd)

            output.show_doc(target)
            return None

        if sub_cmd == 'BOOT':
            if len(cmd_line) > 2:
                sub_cmd = cmd_line[2].upper().strip()
                if GenericCmd.find_field(sub_cmd, TargetBootCmd.FUNCTION):
                    return TargetBootReq(sub_cmd)

            output.show_doc(target)
            return None

    output.show_doc(target)
    return None
