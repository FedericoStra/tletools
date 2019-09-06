import attr as _attr

import numpy as _np
import pandas as _pd

from poliastro.core.angles import M_to_nu as _M_to_nu
from poliastro.twobody import Orbit as _Orbit
from poliastro.bodies import Earth as _Earth

from astropy.time import Time as _Time, TimeDelta as _TimeDelta
import astropy.units as _u


_dtype_datetime64_Y = _np.dtype('datetime64[Y]')
_dtype_timedelta64_us = _np.dtype('timedelta64[us]')

DEG2RAD = _np.pi / 180.
RAD2DEG = 180. / _np.pi

_u_rev = _u.def_unit(['rev', 'revolution'], 2.0 * _np.pi * _u.rad,
                     prefixes=False,
                     doc="revolution: angular measurement, a full turn or rotation")


def _conv_year(s):
    if isinstance(s, int):
        return s
    y = int(s)
    return y + (1900 if y >= 57 else 2000)


def _parse_decimal(s):
    return float("." + s)


def _parse_float(s):
    return float(s[0] + '.' + s[1:6] + 'e' + s[6:8])


def partition(iterable, n):
    it = iter(iterable)
    while True:
        res = []
        try:
            for _ in range(n):
                res.append(next(it))
        except StopIteration:
            return
        yield tuple(res)


def add_epoch(df):
    df['epoch'] = ((df.epoch_year.values - 1970).astype(_dtype_datetime64_Y)
                   + ((df.epoch_day.values-1) * 86400*10**6).astype(_dtype_timedelta64_us))


@_attr.s
class TLE:
    name = _attr.ib(converter=str.strip)
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

    def ___attrs_post_init__(self):
        self._epoch = None
        self._a = None
        self._nu = None

    @property
    def epoch(self):
        if self._epoch is None:
            dt = (_np.datetime64(self.epoch_year-1970, 'Y')
                  + _np.timedelta64(int((self.epoch_day-1) * 86400*10**6), 'us'))
            self._epoch = _Time(dt, format='datetime64', scale='utc')
        return self._epoch

    @property
    def a(self):
        if self._epoch is None:
            self._a = (_Earth.k.value / (self.mm * _np.pi / 43200) ** 2) ** (1/3) / 1000
        return self._a

    @property
    def nu(self):
        if self._nu is None:
            self._nu = _M_to_nu(self.M * DEG2RAD, self.ecc) * RAD2DEG
        return self._nu

    @classmethod
    def from_lines(cls, name, line1, line2):
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
        if isinstance(filename, str):
            with open(filename) as fp:
                return [cls.from_lines(*l012)
                        for l012 in partition(fp, 3)]
        else:
            return [tle for fn in filename for tle in cls.load(fn)]

    @classmethod
    def loads(cls, string):
        return [cls.from_lines(*l012) for l012 in partition(string.split('\n'), 3)]

    @classmethod
    def load_dataframe(cls, filename, *, epoch=True):
        if isinstance(filename, str):
            with open(filename) as fp:
                df = _pd.DataFrame(cls.from_lines(*l012).asdict()
                                  for l012 in partition(fp, 3))
                if epoch:
                    add_epoch(df)
                return df
        else:
            df = _pd.concat([cls.load_dataframe(fn, epoch=False) for fn in filename],
                           ignore_index=True, join='inner', copy=False)
            df.drop_duplicates(inplace=True)
            df.reset_index(drop=True, inplace=True)
            add_epoch(df)
            return df

    def to_orbit(self, attractor=_Earth):
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
        return _attr.astuple(self)

    def asdict(self, computed=False, epoch=False):
        d = _attr.asdict(self)
        if computed:
            d.update(a=self.a, nu=self.nu)
        if epoch:
            d.update(epoch=self.epoch)
        return d


@_attr.s
class TLEu(TLE):
    @property
    def a(self):
        if self._epoch is None:
            self._a = (_Earth.k.value / self.mm.to_value(_u.rad/_u.s) ** 2) ** (1/3) * _u.m
        return self._a

    @property
    def nu(self):
        if self._nu is None:
            self._nu = _M_to_nu(self.M.to_value(_u.rad), self.ecc.to_value(_u.one)) * RAD2DEG * _u.deg
        return self._nu

    @classmethod
    def from_lines(cls, name, line1, line2):
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
        return _Orbit.from_classical(
            attractor=attractor,
            a=self.a,
            ecc=self.ecc,
            inc=self.inc,
            raan=self.raan,
            argp=self.argp,
            nu=self.nu,
            epoch=self.epoch)
