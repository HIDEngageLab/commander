# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


def event(cmd_line):
    """
    Event request

    send a event request to the embedded device

    syntax:
        <ALIAS[, ALIAS[...]]|all> event key KEY_IDENTIFIER <press|release|click|push>
        <ALIAS[, ALIAS[...]]|all> event wheel POSITION
        <ALIAS[, ALIAS[...]]|all> event debug DEBUG_IDENTIFIER <enable|disable>
        <ALIAS[, ALIAS[...]]|all> event led LED_IDENTIFIER <enable|disable>

    parameter:
        POSITION            a wheel position in %%
        KEY_IDENTIFIER      s[0-9] for hard key (s0-s5, top down) and soft key (s5-s9 top down); example: s0 
        DEBUG_IDENTIFIER    d[1-4] for debug identifier; example: d1
        LED_IDENTIFIER      l[1-2] for LED identifier; example: l1

    Debug and LED event default state is disabled. 
    """

    if len(cmd_line) > 1:
        payload = cmd_line[1:]
        from commander.hci.feature.EventReq import EventReq
        return EventReq(payload)

    output.show_doc(event)
    return None
