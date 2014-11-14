import numpy as np
from skimage.transform import resize
from skimage.color import rgb2grey


"""
Differents implementations of dhash with Numpy.

http://www.hackerfactor.com/blog/?/archives/529-Kind-of-Like-That.html
"""

TWOS = np.array([2 ** n for n in range(7, -1, -1)])
BIGS = np.array([256 ** n for n in range(7, -1, -1)], dtype=np.uint64)


def dhash(picture):
    "Compute dhash as uint64."
    img = rgb2grey(resize(picture, (9, 8)))
    h = np.zeros([8], dtype=np.uint8)
    for a in range(8):
        h[a] = TWOS[img[a] > img[a + 1]].sum()
    return (BIGS * h).sum()


def dhash_hex(picture):
    "Compute dhash as hex."
    img = rgb2grey(resize(picture, (9, 8)))
    return ''.join(["%02x" % TWOS[img[a] > img[a + 1]].sum() for a in range(8)])


def cardinality8(number):
    "Number of 1 in a uint8 binary representation."
    if number > 255:
        raise Exception("Too big")
    c = 0
    for a in TWOS:
        if a & number == a:
            c += 1
    return c

HEIGHTBITS = np.array([cardinality8(a) for a in range(256)], int)


def cardinality(number, acc=0):
    "Number of 1 in a uint binary representation."
    div = number / 256
    rest = number % 256
    card = cardinality8(rest)
    if div == 0:
        return acc + card
    else:
        return cardinality(div, acc + card)


def cardinality_str(number):
    return sum([int(a) for a in bin(number)[2:]])


def cardinality_dtype(number):
    return sum(HEIGHTBITS[ord(a)] for a in number.data)


def ncardinality(array):
    "Cardinality of an array of uint64"
    c = np.zeros([len(array)], dtype=int)
    for n in range(array.dtype.itemsize * 8):
        c += array >> n & 1
    return c


if __name__ == "__main__":
    from skimage.data import imread
    p = imread('Alyson_Hannigan_200512.jpg')
    d = dhash(p)
    print d
