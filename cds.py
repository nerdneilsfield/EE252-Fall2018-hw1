#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__: "Dengqi"

import itertools
import math
import sys
import ctypes
import os
import sys

# Try to locate the .so file in the same directory as this file
_file = 'libzhe.so'
_path = os.path.join(*(os.path.split(__file__)[:-1] + (_file, )))
_mod = ctypes.cdll.LoadLibrary(_path)

gcd = _mod.gcd
gcd.argtype = ctypes.c_int
gcd.restype = ctypes.POINTER(ctypes.c_int * 10)


def isprime(n):
    """Returns True if n is prime."""
    if n == 2:
        return True
    if n == 3:
        return True
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False

    i = 5
    w = 2

    while i * i <= n:
        if n % i == 0:
            return False

        i += w
        w = 6 - w

    return True


def cost(realCost):
    res = [i for i in gcd(realCost).contents]
    cost = res[0]
    size = res[1]
    sets = res[2:2 + size]
    return {"cost": cost, "sets": sets}


def doubleAdd(x, y):
    return x + 1, y + 1


COST = [
    [1, 2, 4, 8, 16, 32, 64, 128, 256],
    [
        3, 5, 6, 7, 9, 10, 12, 14, 15, 17, 18, 20, 24, 28, 30, 31, 33, 34, 36,
        40, 48, 56, 60, 62, 63, 65, 66, 68, 72, 80, 96, 112, 120, 124, 126,
        127, 129, 130, 132, 136, 144, 160, 192, 224, 240, 248, 252, 254, 255
    ],
    [
        11, 13, 19, 21, 22, 23, 25, 26, 27, 29, 35, 37, 38, 39, 41, 42, 44, 46,
        47, 49, 50, 52, 54, 55, 57, 58, 59, 61, 67, 69, 70, 71, 73, 74, 76, 78,
        79, 81, 82, 84, 88, 92, 94, 95, 97, 98, 100, 104, 108, 110, 111, 113,
        114, 116, 118, 119, 121, 122, 123, 125, 131, 133, 134, 135, 137, 138,
        140, 142, 143, 145, 146, 148, 152, 156, 158, 159, 161, 162, 164, 168,
        176, 184, 188, 190, 191, 193, 194, 196, 200, 208, 216, 220, 222, 223,
        225, 226, 228, 232, 236, 238, 239, 241, 242, 244, 246, 247, 249, 250,
        251, 253
    ],
    [
        43, 45, 51, 53, 75, 77, 83, 85, 86, 87, 89, 90, 91, 93, 99, 101, 102,
        103, 105, 106, 107, 109, 115, 117, 139, 141, 147, 149, 150, 151, 153,
        154, 155, 157, 163, 165, 166, 167, 169, 170, 172, 174, 175, 177, 178,
        180, 182, 183, 185, 186, 187, 189, 195, 197, 198, 199, 201, 202, 204,
        206, 207, 209, 210, 212, 214, 215, 217, 218, 219, 221, 227, 229, 230,
        231, 233, 234, 235, 237, 243, 245
    ], [171, 173, 179, 181, 203, 205, 211, 213]
]


class SD(object):
    def __init__(self, num):
        self.B = 1 << 63
        self._num = num
        x, bit, signs, sds = 0, 0, 0, []
        x = -num if num < 0 else num

        for i in itertools.count():
            while (bit < 64 and ((x & (1 << bit)) == 0)):
                bit = bit + 1
            if bit == 64:
                break
            first = bit
            ones = 0
            while bit < 64 and (x & (1 << bit) == (1 << bit)):
                bit, ones = doubleAdd(bit, ones)
                sds.append((x, signs))

            if bit == 64:
                break
            if ones > 1:
                x = x + (1 << first)
                x = x | (1 << first)
                signs = signs | (1 << first)

        if num < 0:
            signs = signs ^ x
        self._bin = x
        self._signs = signs
        self._sds = set(sds)

    def _get_ones(self, sd):
        return len([i for i in bin(sd)[2:] if i == '1'])

    def ones(self):
        return self._get_ones(self._bin)

    def __str__(self):
        return self.__print(self._bin, self._signs)

    def get_msds_str(self):
        return [self.__print(i[0], i[1]) for i in self.get_msds()]

    def print_msds(self):
        for i in self.get_msds():
            print(self.__print(i[0], i[1]))

    def get_msds(self):
        return filter(lambda i: self._is_msd(i[0]), self._sds)

    def addOne(self, bits){
        num_temp = int("0b"+bits)
        return bin(num_bits+1)[2:]
    }

    def get_MSD(self):
        msd = []
        bits = bin(self._num)[2:]
        for i in range(len(bits) -1, 0, -1):
            if bits[d] == '1' and bits[d-1] == '1':
                bits = self.addOne(bits[0:d-1]) + "0-" +
                bits[d+1:]
                msd.append(bits)
        res = []
        for i in msd:
            if self._is_msd(i):
                res.append(i.replace('1','+'))
        return res
    
    def __print(self, bin, signs):
        s, bit, _bin, _signs = "", 0, bin, signs

        while bit < 64 and (_bin & self.B == 0):
            _bin = _bin * 2
            _signs = _signs * 2
            bit = bit + 1
        if bit == 64:
            return "0"

        while bit < 64:
            if _bin & self.B == 0:
                s = s + "0"
            else:
                s = s + "-" if _signs & self.B != 0 else s + "+"
            _bin = _bin * 2
            _signs = _signs * 2
            bit = bit + 1
        return s

    def get_ops(self):
        ops = []
        s = 0
        _bin = self._bin
        _signs = self._signs
        while _bin != 0:
            while _bin & 1 == 0:
                s = s + 1
                _bin = _bin >> 1
                _signs = _signs >> 1
            sign = 0
            if _signs & 1 == 1:
                sign = -1
            else:
                sign = 1
            ops.append((s, sign))
            s = s + 1
            _bin = _bin >> 1
            _signs = _signs >> 1
        return ops

    def expr(self, ops=[]):
        if len(ops) == 0:
            ops = self.get_ops()
        expr = ""
        for i in ops:
            sign = ""
            if i[1] < 0:
                sign = "-"
            else:
                sign = "+"
            expr = expr + "%s(x<<%d)" % (sign, i[0])
        return expr

    #Determine whether a sign digital representation
    # is a msd representation
    def _is_msd(self, sd):
        return self._get_ones(sd) == self.ones()


class MinCostSD(SD):

    def cost(self, num):
        num = int(num)
        sd_num = SD(num)
        for i in COST:
            if num in i:
                return COST.index(i)

        return len([i for i in sd_num.expr() if i != '0'])

    def __find_min_cost(self, num):
        heap = []
        d = 0
        cost = self.cost(num)
        # if isprime(num):
        #     return [num]
        for i in range(3, int(math.sqrt(num)) + 2):
            if num % i == 0:
                temp_cost = self.cost(i) + self.cost(num / i)
                if temp_cost <= cost:
                    d = i;
                    cost = temp_cost


        if d == 0:
            heap.append(num)
        else:
            heap = self.__find_min_cost(d)  + self.__find_min_cost(int(num / d))

        return heap

    def min_cost(self):
        # heap = self.__find_min_cost(self._num)
        # # print("*".join([str(i) for i in heap]))
        # return sum([self.cost(i) for i in heap])
        return cost(self._num)

if __name__ == "__main__":
    # ix = input("You input?\n")
    x = MinCostSD(int(sys.argv[1]))
    # print(x)
    # print(x.expr())
    # x.print_msds()
    print(x._num, ":", x.min_cost())
