import plyvel
from cStringIO import StringIO
import numpy as np

from db import HashDB


class Level(HashDB):

    def __init__(self, path):
        self.db = plyvel.DB(path, create_if_missing=True)

    def index(self, files):
        with self.db.write_batch() as wb:
            for path, dhash in self.hash(files):
                wb.put(path, dhash.tostring())

    def values(self):
        names = []
        buff = StringIO()
        for path, h in self.db.iterator():
            names.append(path)
            buff.write(h)
        buff.seek(0)
        hashes = np.fromstring(buff.read(), dtype=np.int64)
        return names, hashes
