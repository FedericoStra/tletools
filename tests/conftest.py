import pytest

from tletools import TLE


@pytest.fixture
def tle_string():
    return """ISS (ZARYA)
1 25544U 98067A   19249.04864348  .00001909  00000-0  40858-4 0  9990
2 25544  51.6464 320.1755 0007999  10.9066  53.2893 15.50437522187805"""

@pytest.fixture
def tle_string2():
    # This TLE tests high mean anomaly value.
    return """NOAA 18
1 28654U 05018A   20098.54037539  .00000075  00000-0  65128-4 0  9992
2 28654  99.0522 154.2797 0015184  73.2195 287.0641 14.12501077766909"""

@pytest.fixture
def tle_lines(tle_string):
    return tle_string.splitlines()

@pytest.fixture
def tle_lines2(tle_string2):
    return tle_string2.splitlines()

@pytest.fixture
def tle():
    return TLE('ISS (ZARYA)', '25544', 'U', '98067A',
               # year, day
               2019, 249.04864348,
               # dn_o2, ddn_o6, bstar, set_num
               1.909e-05, 0.0, 4.0858e-05, 999,
               # inc, raan, ecc, argp
               51.6464, 320.1755, 0.0007999, 10.9066,
               # M, n, rev_num
               53.2893, 15.50437522, 18780)
