.. TLE-tools documentation master file, created by
   sphinx-quickstart on Fri Sep  6 16:54:20 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to TLE-tools's documentation!
=====================================

**TLE-tools** is a small library to work with `two-line element set`_ files.

.. _`two-line element set`: https://en.wikipedia.org/wiki/Two-line_element_set

Purpose
-------

The purpose of the library is to parse TLE sets into convenient :class:`TLE`
objects, load entire TLE set files into :class:`pandas.DataFrame`'s, convert
:class:`TLE` objects into :class:`poliastro.twobody.Orbit`'s, and more.

From Wikipedia_:

   A two-line element set (TLE) is a data format encoding a list of orbital
   elements of an Earth-orbiting object for a given point in time, the epoch.
   The TLE data representation is specific to the
   `simplified perturbations models`_ (SGP, SGP4, SDP4, SGP8 and SDP8),
   so any algorithm using a TLE as a data source must implement one of the SGP
   models to correctly compute the state at a time of interest. TLEs can
   describe the trajectories only of Earth-orbiting objects.

.. _Wikipedia: https://en.wikipedia.org/wiki/Two-line_element_set
.. _simplified perturbations models: https://en.wikipedia.org/wiki/Simplified_perturbations_models

Example::

   ISS (ZARYA)
   1 25544U 98067A   19249.04864348  .00001909  00000-0  40858-4 0  9990
   2 25544  51.6464 320.1755 0007999  10.9066  53.2893 15.50437522187805


Installation
------------

Install and update using pip_::

   pip install -U TLE-tools

.. _pip: https://pip.pypa.io/en/stable/

Links
-----

- Website: https://github.com/FedericoStra/tletools
- Documentation: https://tletools.readthedocs.io/
- Releases: https://pypi.org/project/TLE-tools/
- Code: https://github.com/FedericoStra/tletools
- Issue tracker: https://github.com/FedericoStra/tletools/issues


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::
   :maxdepth: 2
   :caption: Contents:

API Documentation
-----------------

If you are looking for information on a specific function, class, or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api
