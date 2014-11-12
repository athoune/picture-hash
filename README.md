Picture hashing with Numpy
==========================

Find similar pictures in a large collection.
Not exactly same file, but similar ones, resized, or light corrections.

All explaination can be find on this site :
http://www.hackerfactor.com/blog/?/archives/529-Kind-of-Like-That.html

Use it
------

Install Numpy, Scipy, Pillow Skimage.

Index a folder full of pictures :

    python db.py path/to/pictures

Build thumbnails :

    python thumbs.py

Build an ugly webpage with similar pictures

    python show.py

Luigi demo
----------

    Use on worker per CPU, and twice shards.

    ./workflow.py --shards 16 --workers 8 --local-scheduler

TODO
----

 - reverse index with arity
 - index with subdivision, and its arity

Licence
-------

© Mathieu Lecarme, 2014, BSD 3 terms Licence.
