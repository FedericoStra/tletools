from math import pi
import attr

import pandas as pd

from poliastro.core.angles import M_to_nu
from poliastro.twobody import Orbit
from poliastro.bodies import Earth

from astropy.time import Time, TimeDelta
import astropy.units as u


DEG2RAD = pi / 180.
RAD2DEG = 180. / pi

# def_unit(['cycle', 'cy'], 2.0 * _numpy.pi * si.rad,
#          namespace=_ns, prefixes=False,
#          doc="cycle: angular measurement, a full turn or rotation")


def _conv_ecc(s):
    return float("." + s)


def _conv_year(s):
    if isinstance(s, int):
        return s
    y = int(s)
    return y + (1900 if y >= 57 else 2000)


def _conv_float(s):
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
    df['epoch'] = (
        Time(df.epoch_year.map(lambda y: str(y)+'-01-01').values.astype(dtype='<U10'))
        + TimeDelta(df.epoch_day-1))
    df.epoch = df.epoch.apply(lambda e: e.datetime64)
    return df


@attr.s
class TLE:
    name = attr.ib(converter=str.strip)
    norad = attr.ib(converter=str.strip)
    int_desig = attr.ib(converter=str.strip)
    epoch_year = attr.ib(converter=_conv_year)
    epoch_day = attr.ib()
    mm_dt = attr.ib()
    mm_dt2 = attr.ib()
    bstar = attr.ib()
    set_num = attr.ib(converter=int)
    inc = attr.ib()
    raan = attr.ib()
    ecc = attr.ib()
    argp = attr.ib()
    M = attr.ib()
    mm = attr.ib()
    rev_num = attr.ib(converter=int)

    a = attr.ib(init=False)
    nu = attr.ib(init=False)

    def __attrs_post_init__(self):
        self._epoch = None
        self.a = (Earth.k.value / (self.mm * pi / 43200) ** 2) ** (1/3) / 1000
        self.nu = M_to_nu(self.M * DEG2RAD, self.ecc) * RAD2DEG

    @property
    def epoch(self):
        if self._epoch is None:
            self._epoch = (Time(str(self.epoch_year)+'-01-01', scale='utc', format='iso')
                           + TimeDelta(self.epoch_day-1))
        return self._epoch

    @classmethod
    def from_lines(cls, name, line1, line2):
        return cls(
            name=name,
            norad=line1[2:8],
            int_desig=line1[9:17],
            epoch_year=line1[18:20],
            epoch_day=float(line1[20:32]),
            mm_dt=float(line1[33:43]),
            mm_dt2=_conv_float(line1[44:52]),
            bstar=_conv_float(line1[53:61]),
            set_num=line1[64:68],
            inc=float(line2[8:16]),
            raan=float(line2[17:25]),
            ecc=_conv_ecc(line2[26:33]),
            argp=float(line2[34:42]),
            M=float(line2[43:51]),
            mm=float(line2[52:63]),
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
                df = pd.DataFrame(cls.from_lines(*l012).asdict()
                                  for l012 in partition(fp, 3))
                if epoch:
                    add_epoch(df)
                return df
        else:
            df = pd.concat([cls.load_dataframe(fn, epoch=False) for fn in filename],
                           ignore_index=True, join='inner', copy=False)
            df.drop_duplicates(inplace=True)
            df.reset_index(drop=True, inplace=True)
            add_epoch(df)
            return df

    def to_orbit(self, attractor=Earth):
        return Orbit.from_classical(
            attractor=attractor,
            a=self.a * u.km,
            ecc=self.ecc * u.one,
            inc=self.inc * u.deg,
            raan=self.raan * u.deg,
            argp=self.argp * u.deg,
            nu=self.nu * u.deg,
            epoch=self.epoch)

    def asdict(self, extra=False):
        d = attr.asdict(self)
        if extra:
            d.update(epoch=self.epoch)
        return d


@attr.s
class TLEu(TLE):
    def __attrs_post_init__(self):
        self._epoch = None
        self.a = (Earth.k.to_value(u.m**3/u.s**2) / self.mm.to_value(u.rad/u.s) ** 2) ** (1/3) * u.m
        self.nu = M_to_nu(self.M.to_value(u.rad), self.ecc) * u.rad

    @classmethod
    def from_lines(cls, name, line1, line2):
        return cls(
            name=name,
            norad=line1[2:8],
            int_desig=line1[9:17],
            epoch_year=line1[18:20],
            epoch_day=float(line1[20:32]),
            mm_dt=float(line1[33:43]),
            mm_dt2=_conv_float(line1[44:52]),
            bstar=_conv_float(line1[53:61]),
            set_num=line1[64:68],
            inc=float(line2[8:16]) * u.deg,
            raan=float(line2[17:25]) * u.deg,
            ecc=_conv_ecc(line2[26:33]) * u.one,
            argp=float(line2[34:42]) * u.deg,
            M=float(line2[43:51]) * u.deg,
            mm=float(line2[52:63]) * 2*pi * u.rad / u.day,
            rev_num=line2[63:68])

    def to_orbit(self):
        return Orbit.from_classical(
            Earth,
            a=self.a,
            ecc=self.ecc,
            inc=self.inc,
            raan=self.raan,
            argp=self.argp,
            nu=self.nu,
            epoch=self.epoch)


# class TLE_:
#     def __init__(
#         self,
#         name,
#         norad,
#         int_desig,
#         epoch_year,
#         epoch_day,
#         mm_dt,
#         mm_dt2,
#         bstar,
#         set_no,
#         incl,
#         raan,
#         ecc,
#         ap,
#         ma,
#         mm,
#         rev_no
#         ):
#         self.name = _strip(name)
#         self.norad = _strip(norad)
#         self.int_desig = _strip(int_desig)
#         self.epoch_year = _conv_year(epoch_year)
#         self.epoch_day = float(epoch_day)
#         self.mm_dt = float(mm_dt)
#         self.mm_dt2 = _conv_float(mm_dt2)
#         self.bstar = _conv_float(bstar)
#         self.set_no = int(set_no)
#         self.incl = float(incl)
#         self.raan = float(raan)
#         self.ecc = _conv_ecc(ecc)
#         self.ap = float(ap)
#         self.ma = float(ma)
#         self.mm = float(mm)
#         self.rev_no = int(rev_no)
#         self._attrs_post_init__()

#     def __attrs_post_init__(self):
#         epoch = (time.Time(str(self.epoch_year)+'-01-01', scale='ut1')
#                  + time.TimeDelta(self.epoch_day-1))
#         self.epoch = epoch.utc

#     @classmethod
#     def from_tle_lines(cls, name, line1, line2):
#         return cls(
#             name=name,
#             norad=line1[2:8],
#             int_desig=line1[9:17],
#             epoch_year=line1[18:20],
#             epoch_day=line1[20:32],
#             mm_dt=line1[33:43],
#             mm_dt2=line1[44:52],
#             bstar=line1[53:61],
#             set_no=line1[64:68],
#             incl=line2[8:16],
#             raan=line2[17:25],
#             ecc=line2[26:33],
#             ap=line2[34:42],
#             ma=line2[43:51],
#             mm=line2[53:63],
#             rev_no=line2[63:68]
#             )


# def parse_line1(line1):
#     assert line1[1] == '1'
#     return {
#         'norad': line1[2:7],
#         'classification': line1[7],
#         'cospar': line1[9:17],
#         'ep_year': line1[18:20],
#         'ep_day': line1[20:32],
#         'mm_dt': line1[33:43],
#         'mm_dt2': line1[44:52],
#         'bstar': line1[53:61]
#     }


# def parse_line2(line2):
#     assert line2[1] == '2'
#     return {
#         'incl': line2[8:16],
#         'raan': line2[17:25]
#     }
