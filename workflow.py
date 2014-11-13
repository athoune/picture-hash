#!/usr/bin/env python

import luigi

from db import list_folder, FlatDB


def chunking(l, size):
    "Split a list in chunks"
    i = 0
    chunk = len(l) / float(size)
    for a in range(size):
        n = i + chunk
        yield l[int(i):int(n)]
        i = n


class ImageIndex(luigi.Task):

    shards = luigi.IntParameter()

    def requires(self):
        for a in range(self.shards):
            yield Images(shard=a, shards=self.shards)

    def complete(self):
        return False


class Images(luigi.Task):

    shard = luigi.IntParameter()
    shards = luigi.IntParameter()

    def requires(self):
        return ImagesList(shards=self.shards)

    def _images(self):
        with self.requires().output()[self.shard].open('r') as images:
            for i, image in enumerate(images.readlines()):
                if image[-1] == "\n":
                    image = image[:-1]
                yield image

    def run(self):
        db = FlatDB('data/db_%i' % self.shard)
        db.index(self._images())

    def output(self):
        return luigi.LocalTarget("data/db_%i.hashes" % self.shard)


class ImagesList(luigi.Task):

    shards = luigi.IntParameter()

    def output(self):
        return [luigi.LocalTarget("data/images_%i.txt" % a)
                for a in range(self.shards)]

    def run(self):
        images = list(list_folder('images'))
        outs = self.output()
        for i, imgs in enumerate(chunking(images, self.shards)):
            with outs[i].open('w') as f:
                f.write("\n".join(imgs))


if __name__ == '__main__':

    luigi.run(main_task_cls=ImageIndex)
