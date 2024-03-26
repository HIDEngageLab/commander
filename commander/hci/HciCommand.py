# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


class HciCommand:
    """
    create and send a HCI command
    """

    command_dict = dict()

    def __init__(self):
        pass

    def help(self):
        from commander.utilities.PrettyPrint import header

        output.show_text(header('HCI commands'))
        for key, value in HciCommand.command_dict.items():
            output.show_text('%s' % key)
            output.show_doc(value)

    def interpret(self, cmd_line):
        if len(cmd_line) > 0:
            entered_cmd = cmd_line[0].lower().strip()

            if entered_cmd in HciCommand.command_dict:
                return HciCommand.command_dict[entered_cmd](cmd_line[1:])

            else:
                output.show_text('unknown HCI command: %s' %
                                 (' '.join(entered_cmd)))

        return None
