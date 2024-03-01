# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.hci.GenericCmd import GenericCmd
from commander.hci.feature.EventCmd import EventCmd

import commander.termbase as output

class EventReq(EventCmd):
    def __init__(self, data):
        EventCmd.__init__(self, GenericCmd.DIRECTION['REQ'])

        if len(data) < 1:
            data = ['key', 's0', 'press']

        self.__event = EventCmd.EVENT['UNDEFINED']
        self.__value = []

        event_id = data[0].strip().upper()
        if event_id in EventCmd.EVENT:
            self.__event = EventCmd.EVENT[event_id]
            if event_id == 'HASH':
                key_id = data[1].strip().upper()
                if key_id in EventCmd.KEY_ID:
                    self.__value.append(EventCmd.KEY_ID[key_id])
                else:
                    output.show_error(
                        'event request: unknown key id %d' % key_id)
                key_level = data[2].strip().upper()
                if key_level in EventCmd.KEY_LEVEL:
                    self.__value.append(EventCmd.KEY_LEVEL[key_level])
                else:
                    output.show_error(
                        'event request: unknown key level %d' % key_level)
            elif event_id == 'WHEEL':
                from commander.utilities.floats import convert_to_long
                wheel_position = float(data[1])
                while wheel_position > 100.0:
                    wheel_position -= 100.0
                wheel_value = convert_to_long(wheel_position / 100.0)
                self.__value += [(wheel_value >> 24) & 0xff, (wheel_value >> 16) & 0xff,
                                 (wheel_value >> 8) & 0xff, wheel_value & 0xff]
            elif event_id == 'DEBUG':
                index = int(data[1])-1
                identifier = ('DEBUG_PIN%d' % index).strip().upper()
                if identifier in EventCmd.DEBUG_ID:
                    self.__value.append(EventCmd.DEBUG_ID[identifier])
                else:
                    output.show_error(
                        'event request: unknown debug id %d' % identifier)
                filter = data[2].strip().upper()
                if filter in EventCmd.FILTER:
                    self.__value.append(EventCmd.FILTER[filter])
                else:
                    output.show_error(
                        'event request: unknown filter %s' % filter)

            elif event_id == 'LED':
                index = int(data[1])-1
                identifier = ('LED_TEST%d' % index).strip().upper()
                if identifier in EventCmd.LED_ID:
                    self.__value.append(EventCmd.LED_ID[identifier])
                else:
                    output.show_error('event request: unknown led id %d' %
                                      identifier)
                filter = data[2].strip().upper()
                if filter in EventCmd.FILTER:
                    self.__value.append(EventCmd.FILTER[filter])
                else:
                    output.show_error('event request: unknown filter %s' %
                                      filter)

            else:
                output.show_error('event request: wrong event')
        else:
            output.show_error('event request: unknown parameter')

    @property
    def sdu(self):
        return [self.command, self.event] + self.value

    @property
    def event(self):
        return self.__event

    @property
    def value(self):
        return self.__value

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s\n' % ('event', VDELIM, self.event,
                                    GenericCmd.str_field(self.event, EventCmd.EVENT))

        if self.event == EventCmd.EVENT['HASH']:
            s += '%-20s%c %02X %s\n' % (
                'key', VDELIM, self.value[0], self.str_field(self.value[0], EventCmd.KEY_ID))
            s += '%-20s%c %02X %s' % ('level', VDELIM, self.value[1], self.str_field(
                self.value[1], EventCmd.KEY_LEVEL))
        elif self.event == EventCmd.EVENT['WHEEL']:
            from commander.utilities.floats import convert_to_float
            event_str = '%5.2f%%' % (convert_to_float(self.value) * 100.0)
            s += '%-20s%c %s' % ('wheel', VDELIM, event_str)
        else:
            s += '%-20s%c %s' % ('event', VDELIM,
                                 ' '.join(['%02X' % a for a in self.value]))

        return s
