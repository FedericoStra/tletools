# TLE-tools

`TLE-tools` is a small library to work with [two-line element
set](https://en.wikipedia.org/wiki/Two-line_element_set) files.

## Purpose

The purpose of the library is to parse TLE sets into convenient `TLE` objects,
load entire TLE set files into `pandas.DataFrame`'s, convert `TLE` objects into
`poliastro.twobody.Orbit`'s, and more.

From [Wikipedia](https://en.wikipedia.org/wiki/Two-line_element_set):

> A two-line element set (TLE) is a data format encoding a list of orbital
elements of an Earth-orbiting object for a given point in time, the epoch.
The TLE data representation is specific to the [simplified perturbations
models](https://en.wikipedia.org/wiki/Simplified_perturbations_models) (SGP,
SGP4, SDP4, SGP8 and SDP8), so any algorithm using a TLE as a data source must
implement one of the SGP models to correctly compute the state at a time of
interest. TLEs can describe the trajectories only of Earth-orbiting objects.

Example:

```
ISS (ZARYA)
1 25544U 98067A   19249.04864348  .00001909  00000-0  40858-4 0  9990
2 25544  51.6464 320.1755 0007999  10.9066  53.2893 15.50437522187805
```

Here is a minimal example on how to load the previous TLE:

```python
from tletools import tle

tle_string = """
ISS (ZARYA)
1 25544U 98067A   19249.04864348  .00001909  00000-0  40858-4 0  9990
2 25544  51.6464 320.1755 0007999  10.9066  53.2893 15.50437522187805
"""

tle_lines = tle_string.strip().splitlines()

tle = TLE.from_lines(*tle_lines)
```

Then `tle` is:

```python
TLE(name='ISS (ZARYA)', norad='25544', classification='U', int_desig='98067A',
epoch_year=2019, epoch_day=249.04864348, dn_o2=1.909e-05, ddn_o6=0.0, bstar=4.0858e-05,
set_num=999, inc=51.6464, raan=320.1755, ecc=0.0007999, argp=10.9066, M=53.2893,
n=15.50437522, rev_num=18780)
```

and you can then access its attributes like `t.argp`, `t.epoch`...

### TLE format specification

Some more or less complete TLE format specifications can be found on the following websites:

- [Wikipedia](https://en.wikipedia.org/wiki/Two-line_element_set#Format)
- [NASA](https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html)
- [CelesTrak](https://celestrak.com/columns/v04n03/)
- [Space-Track](https://www.space-track.org/documentation#tle)

## Installation

Install and update using [pip](https://pip.pypa.io/en/stable/):
```bash
pip install -U TLE-tools
```

## Links

- Website: https://github.com/FedericoStra/tletools
- Documentation: https://tletools.readthedocs.io/
- Releases: https://pypi.org/project/TLE-tools/
- Code: https://github.com/FedericoStra/tletools
- Issue tracker: https://github.com/FedericoStra/tletools/issues
