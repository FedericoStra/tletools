from tletools import TLE
from tletools.tle import TLEu


def test_from_lines(tle_lines):
    t = TLE.from_lines(*tle_lines)
    assert isinstance(t, TLE)


def test_from_lines_with_units(tle_lines):
    t = TLEu.from_lines(*tle_lines)
    assert isinstance(t, TLEu)


def test_to_orbit(tle):
    assert tle.to_orbit().ecc == tle.ecc


def test_asdict(tle):
    assert type(tle)(**tle.asdict()) == tle


def test_astuple(tle):
    assert type(tle)(*tle.astuple()) == tle
