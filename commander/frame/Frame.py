# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.frame.Trash import Trash
from commander.utilities.PrettyPrint import SLINE, wd
from commander.frame.CheckSum import CheckSum


class Frame:
    DEFAULT_VERBOSITY = 0

    ESCAPE = {0x7d: [0x7d, 0x5d], 0x7e: [0x7d, 0x5e]}
    DEESCAPE = [0x7d, {0x5d: 0x7d, 0x5e: 0x7e}]
    DELIM = 0x7e
    PARSERS = {}  # 0x20

    def __init__(self):
        # self.CRTL = 0x01  # legacy
        self.trash = Trash()

        self.verbosity = Frame.DEFAULT_VERBOSITY
        from commander.config import verbosity
        self.verbosity = verbosity()

    def __print(self, byte_string):
        # Achtung: gibt kompletten buffer aus
        # print 'byte_string:', ''.join('%02X ' % byte_string[i] for i in range(0, len(byte_string)) )
        pass

    def register(self, address, parser):
        Frame.PARSERS[address] = parser
        if self.verbosity >= 0x0f:
            print('frame payload parser reg: %d' % address)

    def serialize(self, address, unserialized_data):
        if address not in Frame.PARSERS:
            if self.verbosity >= 0x0f:
                print('frame check: unknown address')
            return False

        ctrl, serialized_data = self.PARSERS[address].serialize(
            unserialized_data)

        checksum = CheckSum('crc16').perform(serialized_data)

        command = [address, ctrl] + serialized_data + \
            [checksum >> 8, checksum & 0xff]
        checked_command = []

        for byte in command:
            if byte in Frame.ESCAPE:
                checked_command = checked_command + Frame.ESCAPE[byte]
            else:
                checked_command = checked_command + [byte]

        tmp_buffer = [Frame.DELIM] + checked_command + [Frame.DELIM]
        bytes_string = b''.join(b'%c' % byte for byte in tmp_buffer)

        if self.verbosity >= 0x0f:
            print(SLINE * wd)
            print('tx HDLC: %s' % (b' '.join(b'%02X' %
                  byte for byte in bytes_string)).upper())

        return bytes_string

    def check(self, data):
        if len(data) < 6:
            return False

        frame_start = 0
        while len(data[frame_start:]) > 0 and data[frame_start] != Frame.DELIM:
            frame_start += 1

        while len(data[frame_start:]) > 0 and data[frame_start] == Frame.DELIM:
            if len(data[frame_start:]) > 1 and data[frame_start+1] == Frame.DELIM:
                frame_start += 1
            else:
                break

        # find next frame end marker
        delim_found = False
        dlen = 0
        for byte in data[frame_start+3:]:
            dlen += 1
            if byte == Frame.DELIM:
                delim_found = True
                break
        if not delim_found:
            return False
        dlen -= 3

        if dlen < 0:
            return False

        # un-escape
        a = []
        for byte in data[frame_start:dlen + 6 + frame_start]:
            a = a + [byte]

        b = [a[0]]
        for i in range(1, len(a)):
            if a[i - 1] == Frame.DEESCAPE[0] and a[i] in Frame.DEESCAPE[1]:
                b[-1] = Frame.DEESCAPE[1][a[i]]
                dlen -= 1
                continue
            else:
                b = b + [a[i]]

        if b[0] != Frame.DELIM:
            if self.verbosity >= 0x0f:
                print('frame check: wrong start delimiter')
            return False

        in_calc_check = CheckSum('crc16').perform(b[3:dlen + 3])

        check = (b[dlen + 3] << 8) + b[dlen + 4]
        if check != in_calc_check:
            if self.verbosity >= 0x0f:
                print('%s' % (b''.join(b'%02X' % byte for byte in b)))
                print('frame check: wrong checksum: %04X %04X' %
                      (check, in_calc_check))
            return False

        if b[dlen + 5] != Frame.DELIM:
            if self.verbosity >= 0x0f:
                print('frame check: wrong stop delimiter')
            return False

        return True

    def next_frame(self, byte_string):
        if len(byte_string) == 0:
            return False

        if byte_string[0] != Frame.DELIM:
            self.__print(byte_string)
            print('frame next_frame: wrong delimiter')
            return False

        delim_found = False
        dlen = 3
        for byte in byte_string[3:]:
            dlen += 1
            if byte == Frame.DELIM:
                delim_found = True
                break

        if not delim_found:
            self.__print(byte_string)
            print('frame next_frame: incomplete message')
            return 0

        return dlen

    def skip(self, byte_string):
        if len(byte_string) == 0:
            return 0
        elif len(byte_string) == 1:
            if byte_string[0] == Frame.DELIM:
                return 0
            else:
                return 1

        delim_found = False
        dlen = 1
        for byte in byte_string[1:]:
            if byte == Frame.DELIM:
                delim_found = True
                break
            dlen += 1

        # print 'dlen', dlen,
        if not delim_found:
            self.__print(byte_string)
            return 0

        return dlen

    def deserialize(self, byte_string):
        if self.verbosity >= 0x0f:
            print(SLINE * wd)
            print('HDLC rx: %s' %
                  (' '.join('%02X' % byte for byte in byte_string)).upper())

        if len(byte_string) < 6:
            if self.verbosity >= 0x0f:
                print('hdlc deserialize: wrong hdlc length: %d', len(byte_string))
            return False

        if byte_string[0] != Frame.DELIM:
            self.__print(byte_string)
            if self.verbosity >= 0x0f:
                print('hdlc deserialize: wrong start delimiter')

        frame_start = 0
        while len(byte_string[frame_start:]) > 0 and byte_string[frame_start] != Frame.DELIM:
            frame_start += 1

        while len(byte_string[frame_start:]) > 0 and byte_string[frame_start] == Frame.DELIM:
            if len(byte_string[frame_start:]) > 1 and byte_string[frame_start+1] == Frame.DELIM:
                frame_start += 1
            else:
                break

        delim_found = False
        dlen = 0
        for byte in byte_string[frame_start+3:]:
            dlen += 1
            if byte == Frame.DELIM:
                delim_found = True
                break
        dlen -= 3

        if not delim_found:
            self.__print(byte_string)
            if self.verbosity >= 0x0f:
                print('hdlc deserialize: incomplete message')

        a = []
        for byte in byte_string[frame_start:dlen + 6 + frame_start]:
            a = a + [byte]
        b = [a[0]]
        for i in range(1, len(a)):
            if a[i - 1] == Frame.DEESCAPE[0] and a[i] in Frame.DEESCAPE[1]:
                b[-1] = Frame.DEESCAPE[1][a[i]]
                dlen -= 1
                continue
            else:
                b = b + [a[i]]
        byte_string = b''.join([b'%c' % i for i in b])

        address = byte_string[1]
        parser = self.trash
        if address in Frame.PARSERS:
            parser = Frame.PARSERS[address]

        ctrl = byte_string[2]

        payload = b[3:dlen + 3]

        in_calc_check = CheckSum('crc16').perform(payload)

        check = (b[dlen + 3] << 8) + b[dlen + 4]

        if check != in_calc_check:
            if self.verbosity >= 0x0f:
                print('hdlc deserialize: wrong checksum: check:%x calc:%x' %
                      (check, in_calc_check))

        if b[dlen + 5] != Frame.DELIM:
            if self.verbosity >= 0x0f:
                print('hdlc deserialize: wrong stop delimiter')

        return {'address': address, 'ctrl': ctrl, 'payload': parser.deserialize(ctrl, payload)}
