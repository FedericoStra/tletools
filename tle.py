'''
**TLE-tools** is a small library to work with `two-line element set`_ files.

.. _`two-line element set`: https://en.wikipedia.org/wiki/Two-line_element_set

The module :mod:`tle` defines the class :class:`TLE`.

Example
-------

>>> tle_string = """
... ISS (ZARYA)
... 1 25544U 98067A   19249.04864348  .00001909  00000-0  40858-4 0  9990
... 2 25544  51.6464 320.1755 0007999  10.9066  53.2893 15.50437522187805
... """
>>> tle_lines = tle_string.strip().splitlines()
>>> TLE.from_lines(*tle_lines)
TLE(name='ISS (ZARYA)', norad='25544', ..., n=15.50437522, rev_num=18780)
'''

import attr as _attr

import numpy as _np
import pandas as _pd

from poliastro.core.angles import M_to_nu as _M_to_nu
from poliastro.twobody import Orbit as _Orbit
from poliastro.bodies import Earth as _Earth

from astropy.time import Time as _Time
import astropy.units as _u


_dt_dt64_Y = _np.dtype('datetime64[Y]')
_dt_td64_us = _np.dtype('timedelta64[us]')

DEG2RAD = _np.pi / 180.
RAD2DEG = 180. / _np.pi

_u_rev = _u.def_unit(['rev', 'revolution'], 2.0 * _np.pi * _u.rad,
                     prefixes=False,
                     doc="revolution: angular measurement, a full turn or rotation")


def _conv_year(s):
    """Interpret a two-digit year string."""
    if isinstance(s, int):
        return s
    y = int(s)
    return y + (1900 if y >= 57 else 2000)


def _parse_decimal(s):
    """Parse a floating point with implicit leading dot.

    >>> _parse_decimal('378')
    0.378
    """
    return float('.' + s)


def _parse_float(s):
    """Parse a floating point with implicit dot and exponential notation.

    >>> _parse_float(' 12345-3')
    0.00012345
    >>> _parse_float('+12345-3')
    0.00012345
    >>> _parse_float('-12345-3')
    -0.00012345
    """
    return float(s[0] + '.' + s[1:6] + 'e' + s[6:8])


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


def add_epoch(df):
    """Add a column ``'epoch'`` to a dataframe.

    `df` must have columns ``'epoch_year'`` and ``'epoch_day'``, from which the
    column ``'epoch'`` is computed.

    :param pandas.DataFrame df: :class:`pandas.DataFrame` instance to modify.

    **Example**

    >>> from pandas import DataFrame
    >>> df = DataFrame([[2018, 31.2931], [2019, 279.3781]],
    ...                columns=['epoch_year', 'epoch_day'])
    >>> add_epoch(df)
    >>> df
       epoch_year  epoch_day                   epoch
    0        2018    31.2931 2018-01-31 07:02:03.840
    1        2019   279.3781 2019-10-06 09:04:27.840
    """
    df['epoch'] = ((df.epoch_year.values - 1970).astype(_dt_dt64_Y)
                   + ((df.epoch_day.values - 1) * 86400 * 10**6).astype(_dt_td64_us))


def load_dataframe(filename, *, epoch=True):
    """Load multiple TLEs from one or more files and return a :class:`pandas.DataFrame`."""
    if isinstance(filename, str):
        with open(filename) as fp:
            df = _pd.DataFrame(TLE.from_lines(*l012).asdict()
                               for l012 in partition(fp, 3))
            if epoch:
                add_epoch(df)
            return df
    else:
        df = _pd.concat([TLE.load_dataframe(fn, epoch=False) for fn in filename],
                        ignore_index=True, join='inner', copy=False)
        df.drop_duplicates(inplace=True)
        df.reset_index(drop=True, inplace=True)
        add_epoch(df)
        return df


@_attr.s
class TLE:
    """Data class representing a single TLE.

    A two-line element set (TLE) is a data format encoding a list of orbital
    elements of an Earth-orbiting object for a given point in time, the epoch.

    All the attributes parsed from the TLE are expressed in the same units that
    are used in the TLE format.
    
    :ivar str name:
        Name of the satellite.
    :ivar str norad:
        NORAD catalog number (https://en.wikipedia.org/wiki/Satellite_Catalog_Number).
    :ivar str classification:
        'U', 'C', 'S' for unclassified, classified, secret.
    :ivar str int_desig:
        International designator (https://en.wikipedia.org/wiki/International_Designator),
    :ivar int epoch_year:
        Year of the epoch.
    :ivar float epoch_day:
        Day of the year plus fraction of the day.
    :ivar float dn_o2:
        First time derivative of the mean motion divided by 2.
    :ivar float ddn_o6:
        Second time derivative of the mean motion divided by 6.
    :ivar float bstar:
        BSTAR coefficient (https://en.wikipedia.org/wiki/BSTAR).
    :ivar int set_num:
        Element set number.
    :ivar float inc:
        Inclination.
    :ivar float raan:
        Right ascension of the ascending node.
    :ivar float ecc:
        Eccentricity.
    :ivar float argp:
        Argument of perigee.
    :ivar float M:
        Mean anomaly.
    :ivar float n:
        Mean motion.
    :ivar int rev_num:
        Revolution number.
    """

    # name of the satellite
    name = _attr.ib(converter=str.strip)
    # NORAD catalog number (https://en.wikipedia.org/wiki/Satellite_Catalog_Number)
    norad = _attr.ib(converter=str.strip)
    classification = _attr.ib()
    int_desig = _attr.ib(converter=str.strip)
    epoch_year = _attr.ib(converter=_conv_year)
    epoch_day = _attr.ib()
    dn_o2 = _attr.ib()
    ddn_o6 = _attr.ib()
    bstar = _attr.ib()
    set_num = _attr.ib(converter=int)
    inc = _attr.ib()
    raan = _attr.ib()
    ecc = _attr.ib()
    argp = _attr.ib()
    M = _attr.ib()
    n = _attr.ib()
    rev_num = _attr.ib(converter=int)

    def __attrs_post_init__(self):
        self._epoch = None
        self._a = None
        self._nu = None

    @property
    def epoch(self):
        """Epoch of the TLE."""
        if self._epoch is None:
            dt = (_np.datetime64(self.epoch_year - 1970, 'Y')
                  + _np.timedelta64(int((self.epoch_day - 1) * 86400 * 10**6), 'us'))
            self._epoch = _Time(dt, format='datetime64', scale='utc')
        return self._epoch

    @property
    def a(self):
        """Semi-major axis."""
        if self._epoch is None:
            self._a = (_Earth.k.value / (self.n * _np.pi / 43200) ** 2) ** (1/3) / 1000
        return self._a

    @property
    def nu(self):
        """True anomaly."""
        if self._nu is None:
            self._nu = _M_to_nu(self.M * DEG2RAD, self.ecc) * RAD2DEG
        return self._nu

    @classmethod
    def from_lines(cls, name, line1, line2):
        """Parse a TLE from its constituent lines.

        All the attributes parsed from the TLE are expressed in the same units that
        are used in the TLE format.
        """
        return cls(
            name=name,
            norad=line1[2:7],
            classification=line1[7],
            int_desig=line1[9:17],
            epoch_year=line1[18:20],
            epoch_day=float(line1[20:32]),
            dn_o2=float(line1[33:43]),
            ddn_o6=_parse_float(line1[44:52]),
            bstar=_parse_float(line1[53:61]),
            set_num=line1[64:68],
            inc=float(line2[8:16]),
            raan=float(line2[17:25]),
            ecc=_parse_decimal(line2[26:33]),
            argp=float(line2[34:42]),
            M=float(line2[43:51]),
            n=float(line2[52:63]),
            rev_num=line2[63:68])

    @classmethod
    def load(cls, filename):
        """Load multiple TLEs from a file."""
        if isinstance(filename, str):
            with open(filename) as fp:
                return [cls.from_lines(*l012)
                        for l012 in partition(fp, 3)]
        else:
            return [tle for fn in filename for tle in cls.load(fn)]

    @classmethod
    def loads(cls, string):
        """Load multiple TLEs from a string."""
        return [cls.from_lines(*l012) for l012 in partition(string.split('\n'), 3)]

    def to_orbit(self, attractor=_Earth):
        """Convert to an orbit around the attractor."""
        return _Orbit.from_classical(
            attractor=attractor,
            a=_u.Quantity(self.a, _u.km),
            ecc=_u.Quantity(self.ecc, _u.one),
            inc=_u.Quantity(self.inc, _u.deg),
            raan=_u.Quantity(self.raan, _u.deg),
            argp=_u.Quantity(self.argp, _u.deg),
            nu=_u.Quantity(self.nu, _u.deg),
            epoch=self.epoch)

    def astuple(self):
        """Return a tuple of the attributes."""
        return _attr.astuple(self)

    def asdict(self, computed=False, epoch=False):
        """Return a dict of the attributes."""
        d = _attr.asdict(self)
        if computed:
            d.update(a=self.a, nu=self.nu)
        if epoch:
            d.update(epoch=self.epoch)
        return d


@_attr.s
class TLEu(TLE):
    """Unitful data class representing a single TLE.

    This is a subclass of :class:`TLE`, so refer to that class for a description
    of the attributes, properties and methods.

    The only difference here is that all the attributes are quantities
    (:class:`astropy.units.Quantity`), a type able to represent a value with
    an associated unit taken from :mod:`astropy.units`.
    """

    @property
    def a(self):
        """Semi-major axis."""
        if self._epoch is None:
            self._a = (_Earth.k.value / self.n.to_value(_u.rad/_u.s) ** 2) ** (1/3) * _u.m
        return self._a

    @property
    def nu(self):
        """True anomaly."""
        if self._nu is None:
            nu_rad = _M_to_nu(self.M.to_value(_u.rad), self.ecc.to_value(_u.one))
            self._nu = nu_rad * RAD2DEG * _u.deg
        return self._nu

    @classmethod
    def from_lines(cls, name, line1, line2):
        """Parse a TLE from its constituent lines."""
        return cls(
            name=name,
            norad=line1[2:7],
            classification=line1[7],
            int_desig=line1[9:17],
            epoch_year=line1[18:20],
            epoch_day=float(line1[20:32]),
            dn_o2=_u.Quantity(float(line1[33:43]), _u_rev / _u.day**2),
            ddn_o6=_u.Quantity(_parse_float(line1[44:52]), _u_rev / _u.day**3),
            bstar=_u.Quantity(_parse_float(line1[53:61]), 1 / _u.earthRad),
            set_num=line1[64:68],
            inc=_u.Quantity(float(line2[8:16]), _u.deg),
            raan=_u.Quantity(float(line2[17:25]), _u.deg),
            ecc=_u.Quantity(_parse_decimal(line2[26:33]), _u.one),
            argp=_u.Quantity(float(line2[34:42]), _u.deg),
            M=_u.Quantity(float(line2[43:51]), _u.deg),
            n=_u.Quantity(float(line2[52:63]), _u_rev / _u.day),
            rev_num=line2[63:68])

    def to_orbit(self, attractor=_Earth):
        """Convert to an orbit around the attractor."""
        return _Orbit.from_classical(
            attractor=attractor,
            a=self.a,
            ecc=self.ecc,
            inc=self.inc,
            raan=self.raan,
            argp=self.argp,
            nu=self.nu,
            epoch=self.epoch)
