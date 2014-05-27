#!/usr/bin/env python

import numpy as np
from dhash import cardinality_dtype, dhash, ncardinality
from skimage.data import imread

import os
import sys


def list_folder(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if name[0] == ".":
                continue
            yield "%s/%s" % (root, name)


class HashDB(object):

    def values(self):
        raise NotImplementedError()

    def index(self):
        raise NotImplementedError()

    def hash(self, files):
        i = 0
        for path in files:
            i += 1
            try:
                p = imread(path)
            except IOError as e:
                print "oups", e
                continue
            d = dhash(p)
            if i == 100:
                print('#')
                i = 0
            yield path, d

    def find_similarity(self):
        names, hashes = self.values()

        size = len(hashes)
        ref = np.zeros([size], dtype=np.int64)
        l = np.arange(size)
        for i in range(1, size):
            ref[:] = hashes[i - 1]
            c = ncardinality(hashes[i:] ^ ref[i:])
            mask = c <= 4
            if mask.any():
                yield i, c[mask], l[mask]


class FlatDB(HashDB):

    def __init__(self, path):
        self.path = path

    def index(self, files):
        names = open("%s.names" % self.path, 'w')
        hashes = open("%s.hashes" % self.path, 'w')
        for path, dhash in self.hash(files):
            names.write(path)
            names.write(':')
            hashes.write(dhash.tostring())

    def values(self):
        names = open("%s.names" % self.path, 'r').read().split(':')[:-1]
        hashes = np.fromfile("%s.hashes" % self.path, dtype=np.int64)
        return names, hashes




db = FlatDB('test')
#db.index(list_folder(sys.argv[1]))

for a in db.find_similarity():
    print a

"""
for i, h1 in enumerate(hashes):
    for j in range(i + 1, size):
        h2 = hashes[j]
        c = cardinality_dtype(h1 ^ h2)
        if c <= 4:
           print c, names[i], names[j]
"""
