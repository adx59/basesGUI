#!/usr/bin/env python3

# Binary Object

__author__ = "Adam Xu"


class Bin:
    def __init__(self, binstr):
        """Bin.__init__(binvalue) -> None
            initializes a new Bin, or Binary object, with the value
            of the integer in the parameter given
            methods include: find_bin(), shift_r(), and shift_l()"""
        self.bv = 0
        self.binstr = binstr

    def __str__(self):
        """Bin.__str__() -> str(duh)
            returns a string with integer val and
            binstring val"""
        return "INTEGER " + str(self.bv) + " BINSTRING " + self.binstr

    def find_bin(self):
        """Bin.find_bin() -> str
            returns a string of the binary value of the integer
            provided"""
        return self.binstr

    def update_int(self):
        new_value = 0
        b = self.binstr[::-1]
        for ind in range(len(b)):
            if int(b[ind]) == 1:
                new_value += 2 ** ind
        self.bv = new_value
