import numpy as np
import astropy.units as u

#: :class:`numpy.dtype` for a date expressed as a year.
dt_dt64_Y = np.dtype('datetime64[Y]')
#: :class:`numpy.dtype` for a timedelta expressed in microseconds.
dt_td64_us = np.dtype('timedelta64[us]')

#: :class:`astropy.units.Unit` of angular measure: a full turn or rotation.
#: It is equivalent to :const:`astropy.units.cycle`.
rev = u.def_unit(
    ['rev', 'revolution'],
    2.0 * np.pi * u.rad,
    prefixes=False,
    doc="revolution: angular measurement, a full turn or rotation")

u.add_enabled_units(rev)


def partition(iterable, n, rest=False):
    """Partition an iterable into tuples.

    The iterable `iterable` is progressively consumed `n` items at a time in order to
    produce tuples of length `n`.

    :param iterable iterable: The iterable to partition.
    :param int n: Length of the desired tuples.
    :param bool rest: Whether to return a possibly incomplete tuple at the end.
    :returns: A generator which yields subsequent `n`-uples from the original iterable.

    **Examples**

    By default, any remaining items which are not sufficient to form
    a new tuple of length `n` are discarded.

    >>> list(partition(range(8), 3))
    [(0, 1, 2), (3, 4, 5)]

    You can ask to return the remaining items at the end by setting the flag `rest`
    to ``True``.

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


def _partition(iterable, n):
    """Partition an iterable into tuples."""
    it = iter(iterable)
    z = (it,) * n
    return zip(*z)
