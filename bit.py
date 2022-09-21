#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  bit.py
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
"""Simulate a bit (1 or 0) of data"""
import copy

class bit():
    """Simulation of a single bit"""
    def __init__(self, parity=False):
        """Simulate a single bit

        With parity set to False, no parity bit or checks are done. This can
        increase performance, but decrease stability.

        For most use cases, leaving parity as False is safe.
        """
        # set the parity setting. Default to False
        if isinstance(parity, bool):
            self._parity= parity
        else:
            self._parity= False

        if self._parity:
            self._data = {"data": False, "parity": False}
        else:
            self._data = {"data": False}

        if self._parity:
            # define parity check if parity is enabled
            def check_parity():
                """Manually perform a parity check.

                True if parity is good.
                Else, False
                """
                return self._data["parity"] == self._data["data"]

            self.check_parity = check_parity

    def get_bit(self):
        """Get current value of bit

        If parity was set to True, if the parity bit and data bit do not match,
        a ValueError is raised
        """
        if self._parity:
            if self._data["data"] == self._data["parity"]:
                return self._data["data"]
            raise ValueError("Parity bit does not match Value Bit!")
        return self._data["data"]

    def set_bit(self, data):
        """Set current value of bit

        No parity checks performed
        """
        new_data = bool(data)
        # bits must be 100% independent of one another. Prevent Pass by Address
        if self._parity:
            self._data["parity"] = copy.deepcopy(new_data)
        self._data["data"] = copy.deepcopy(new_data)

    def bit_flip(self, parity=True):
        """Flip the bit

        Parity in this context means whether to honor the initially set parity
        setting. This can be useful for simulating cosmic rays and the like.
        """
        if parity and self._parity:
            self._data["parity"] = not self._data["parity"]
        self._data["data"] = not self._data["data"]
