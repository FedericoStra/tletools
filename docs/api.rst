.. _api:

API Documentation
*****************

This part of the documentation covers all the interfaces of :mod:`tletools`.
For guides on how to use them, pleas consult the tutorials.

TLE Classes
===========

.. automodule:: tletools.tle

Interoperability
================

Pandas
------

.. automodule:: tletools.pandas
    :members:

Poliastro
---------

Use the :meth:`.TLE.to_orbit` method like this::

    >>> tle_string = """ISS (ZARYA)
    ... 1 25544U 98067A   19249.04864348  .00001909  00000-0  40858-4 0  9990
    ... 2 25544  51.6464 320.1755 0007999  10.9066  53.2893 15.50437522187805"""
    >>> tle = TLE.from_lines(*tle_string.splitlines())
    >>> tle.to_orbit()
    6788 x 6799 km x 51.6 deg (GCRS) orbit around Earth (♁) at epoch 2019-09-06T01:10:02.796672000 (UTC)

Utils
=====

.. automodule:: tletools.utils
    :members:
