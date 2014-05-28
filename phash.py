from IPython.parallel import Client
from db import FlatDB

db = FlatDB('test')

rc = Client()
dview = rc[:]

def split_list(steps, workers):
    step = steps / workers
    total = 0
    while total < steps:
        if steps - total >= step:
            yield total, total + step - 1
        else:
            yield total, steps -1
        total += step


@dview.parallel(block=True)
def task((start, end)):
    from db import FlatDB
    db = FlatDB('test')
    return list(db.find_similarity(start, end))

similar = task.map(split_list(len(db), len(rc)))
print similar
