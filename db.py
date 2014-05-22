#!/usr/bin/env python

import plyvel
import numpy as np
from dhash import cardinality_dtype, dhash
from skimage.data import imread
from cStringIO import StringIO

import os
import sys


def list_folder(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if name[0] == ".":
                continue
            yield "%s/%s" % (root, name)


def index(db, files):
    i = 0
    with db.write_batch() as wb:
        for path in files:
            i += 1
            try:
                p = imread(path)
            except IOError as e:
                print "oups", e
                continue
            d = dhash(p)
            wb.put(path, d.tostring())
            if i == 100:
                print('#')
                i = 0


def double(db):
    names = []
    buff = StringIO()
    for path, h in db.iterator():
        names.append(path)
        buff.write(h)
    buff.seek(0)
    hashes = np.fromstring(buff.read(), dtype=np.int64)
    return names, hashes


db = plyvel.DB('/tmp/testdb/', create_if_missing=True)
#index(db, list_folder(sys.argv[1]))
names, hashes = double(db)

for i, h1 in enumerate(hashes):
    for j, h2 in enumerate(hashes):
        if i == j:
            continue
        c = cardinality_dtype(h1 ^ h2)
        if c <= 4:
            print c, names[i], names[j]
