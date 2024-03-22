# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.frame.Trash import Trash
from commander.utilities.PrettyPrint import SLINE, wd
from commander.frame.CheckSum import CheckSum
from commander.config import verbosity


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
        self.verbosity = verbosity()

        self.__start = 0
        self.__stop = 0
        self.__data = None

    @property
    def data(self):
        return self.__data

    @property
    def start(self):
        return self.__start

    @property
    def stop(self):
        return self.__stop

    def __print(self, byte_string):
        # Achtung: gibt kompletten buffer aus
        # print 'byte_string:', ''.join('%02X ' % byte_string[i] for i in range(0, len(byte_string)) )
        pass

    def register(self, address, parser):
        Frame.PARSERS[address] = parser
        if self.verbosity >= 0x0f:
            print('frame payload parser reg: %d' % address)

    def serialize(self, address, _data):
        if address not in Frame.PARSERS:
            if self.verbosity >= 0x0f:
                print('frame check: unknown address')
            return False

        ctrl, data = self.PARSERS[address].serialize(_data)

        checksum = CheckSum('crc16').perform(data)

        command = [address, ctrl] + data + \
            [checksum >> 8, checksum & 0xff]

        escaped_command = []
        for byte in command:
            if byte in Frame.ESCAPE:
                escaped_command = escaped_command + Frame.ESCAPE[byte]
            else:
                escaped_command = escaped_command + [byte]

        tmp_buffer = [Frame.DELIM] + escaped_command + [Frame.DELIM]
        bytes_string = b''.join(b'%c' % byte for byte in tmp_buffer)

        if self.verbosity >= 0x0f:
            print(SLINE * wd)
            print('tx HDLC: %s' % (b' '.join(b'%02X' %
                  byte for byte in bytes_string)).upper())

        return bytes_string

    def check(self, data):
        self.__start = 0
        self.__stop = 0
        self.__data = None

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

        self.__start = frame_start
        data = data[frame_start:]

        # find next frame end marker
        delim_found = False
        data_len = 0
        for byte in data[3:]:
            data_len += 1
            if byte == Frame.DELIM:
                delim_found = True
                break
        if not delim_found:
            return False
        data_len -= 3

        if data_len < 0:
            return False

        self.__stop = self.__start + data_len + 6

        # un-escape
        a = [byte for byte in data[:data_len + 6]]
        b = [a[0]]
        for i in range(1, len(a)):
            if a[i - 1] == Frame.DEESCAPE[0] and a[i] in Frame.DEESCAPE[1]:
                b[-1] = Frame.DEESCAPE[1][a[i]]
                data_len -= 1
                continue
            else:
                b = b + [a[i]]
        if b[0] != Frame.DELIM:
            if self.verbosity >= 0x0f:
                print('frame check: wrong start delimiter')
            return False

        in_calc_check = CheckSum('crc16').perform(b[3:data_len + 3])

        check = (b[data_len + 3] << 8) + b[data_len + 4]
        if check != in_calc_check:
            if self.verbosity >= 0x0f:
                print('%s' % (b''.join(b'%02X' % byte for byte in b)))
                print('frame check: wrong checksum: %04X %04X' %
                      (check, in_calc_check))
            return False

        if b[data_len + 5] != Frame.DELIM:
            if self.verbosity >= 0x0f:
                print('frame check: wrong stop delimiter')
            return False

        self.__data = b

        return True

    def deserialize(self, _frame):
        print('HDLC rx:', ' '.join('%02X' % byte for byte in _frame))

        address = _frame[1]
        parser = self.trash
        if address in Frame.PARSERS:
            parser = Frame.PARSERS[address]

        ctrl = _frame[2]

        payload = _frame[3:-3]

        return {'address': address, 'ctrl': ctrl, 'payload': parser.deserialize(ctrl, payload)}
