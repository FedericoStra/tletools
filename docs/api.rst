.. _api:

API Documentation (auto)
========================

This part of the documentation covers all the interfaces of :mod:`tle`. For
parts where Requests depends on external libraries, we document the most
important right here and provide links to the canonical documentation.

.. automodule:: tle
   :members:


API Documentation
=================

TLE Classes
-----------

The library offers two classes to represent a single TLE.
There is the untless version :class:`TLE`, whose attributes are expressed in the same units
that are used in the TLE format, and there is the unitful version :class:`TLEu`,
whose attributes are quantities (:class:`astropy.units.Quantity`), a type able to represent
a value with an associated unit taken from :mod:`astropy.units`.

.. autoclass:: TLE
.. autoclass:: TLEu

Module functions
----------------

.. autofunction:: load_dataframe

Convenience functions
~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: partition
.. autofunction:: add_epoch
