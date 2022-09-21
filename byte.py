#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  byte.py
#
#  Copyright 2022 Thomas Castleman <contact@draugeros.org>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
"""Simulate a byte of data (8 bits)"""
from bit import bit

class byte():
    """Simulation of a single byte"""
    def __init__(self, parity=1):
        """Simulate a single bit

        Parity can be set in levels: 0-3
        level 0: no parity what-so-ever, best performance, least stability
        level 1: byte-level parity, adds extra parity bit to the byte.
                 Slightly slower performance.
        level 2: bit-level parity, compares the data bit to a second bit which
                 should always be the same. Significantly slower.
        level 3: Combined bit- and byte-level parity. Maximum stability, worst
                 performance

        For most use cases, leaving parity as 1 is safe.
        """
        self._parity = int(parity)
        count = 8
        self._data = {"data": []}
        for each in range(0, count):
            if self._parity >= 2:
                self._data["data"].append(bit(parity=True))
            else:
                self._data["data"].append(bit())

        if (self._parity % 2) == 1:
            if self._parity >= 2:
                self._data["parity"] = bit(parity=True)
            else:
                self._data["parity"] = bit()
            # set parity bit to true since 0 is even
            self._data["parity"].bit_flip()

        if self._parity:
            # define parity check if parity is enabled
            def check_parity():
                """Manually perform a parity check.

                True if parity is good.
                Else, False
                """
                # how do you check parity on a byte?
                # check number of 1s and 0s
                num_1s = 0
                for each in self._data["data"]:
                    if each.get_bit():
                        num_1s += 1
                if (num_1s % 2) == 1:
                    return not self._data["parity"].get_bit()
                return self._data["parity"].get_bit()

            self.check_parity = check_parity

            def recalculate_parity():
                """recalculate parity bit value"""
                num_1s = 0
                for each in self._data["data"]:
                    if each.get_bit():
                        num_1s += 1
                if (num_1s % 2) == 1:
                    self._data["parity"].set_bit(False)
                else:
                    self._data["parity"].set_bit(True)

            self.recalculate_parity = recalculate_parity


    def get_byte(self, override_parity=False):
        """Get state of all bits, excluding parity

        Setting override_parity to True bypasses parity checks in order
        to attempt data repair or ignore issues
        """
        if self._parity and not override_parity:
            if not self.check_parity():
                raise ValueError("Parity issue detected!")
        output = []
        for each in self._data["data"]:
            output.append(each.get_bit(override_parity=override_parity))
        return output

    def set_bit(self, index, value):
        """Change a single bit at the given index"""
        new_value = bool(value)
        self._data["data"][index].set_bit(value)
        if self._parity:
            self.recalculate_parity()

    def get_bit(self, index, override_parity=False):
        """get the value of a single bit at a given index"""
        op = bool(override_parity)
        return self._data["data"][index].get_bit(override_parity=op)

    def set_byte(self, value, endian=True):
        """Set entire byte's data at once.

        value should be a list up to 8 values long, and will be converted to
        booleans before writing. Missing values will be filled with 0s.

        endian controls whether data is stored on the byte-level in
        little-endian or big-endian format. True is little-endian and the
        default, False is big-endian
        """
        filler = 8 - len(value)
        data = []
        # Fill missing data with 0s
        for each in range(0, filler):
            data.append(False)
        for each in value:
            if endian:
                data.insert(0, bool(each))
            else:
                data.append(bool(each))
        for each in enumerate(data):
            self.set_bit(each[0], each[1])
