import numpy as np

dt_dt64_Y = np.dtype('datetime64[Y]')
dt_td64_us = np.dtype('timedelta64[us]')

def partition(iterable, n, rest=False):
    """Partition an iterable into tuples.

    The iterable `iterable` is progressively consumed `n` items at a time in order to
    produce tuples of length `n`.

    :param iterable iterable: The iterable to partition.
    :param int n: Length of the desired tuples.
    :param bool rest: Whether to return a possibly incomplete tuple at the end.
    :returns: A generator which yields subsequent n-uples from the original iterable.

    **Examples**

    >>> list(partition(range(8), 3))
    [(0, 1, 2), (3, 4, 5)]
    >>> list(partition(range(8), 3, rest=True))
    [(0, 1, 2), (3, 4, 5), (6, 7)]
    """
    it = iter(iterable)
    while True:
        res = []
        try:
            for _ in range(n):
                res.append(next(it))
        except StopIteration:
            if rest:
                yield tuple(res)
            return
        yield tuple(res)
