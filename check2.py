# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 13:25:35 2016

@author: svyatoslav
"""

import numpy as np
import struct


def write_bin(fname, s):
    f = open(fname, "wb")
    myfmt = 'b' * len(s)
    bin = struct.pack(myfmt, *(s))
    f.write(bin)
    f.close()


angles = np.loadtxt('angles1.txt')
point = np.loadtxt('heartbin1.txt')
for i in xrange(len(point)):
    if point[i] == 0 and angles[i, 1] > 0:
        print "wrong angles"
angl = np.reshape(angles, 3 * len(point))
angles1 = np.floor(np.reshape(angles, 3 * len(point)) * 127 + 0.5)
write_bin('p.bin', point)
write_bin('v.bin', angles1)
a = []
with open("angles1.bin", "rb") as f:
    byte = f.read()
    text = struct.unpack("b" * 4096 * 3, byte)
    #    while byte != "":
    #        byte = f.read(1)
    #        text = struct.unpack("b", byte)
    a.append(text)
a = (np.array(a)) / 127.0
a = np.reshape(a, (4096, 3))