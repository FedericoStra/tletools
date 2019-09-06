.. _api:

Developer Interface
===================

.. module:: tle

This part of the documentation covers all the interfaces of Requests. For
parts where Requests depends on external libraries, we document the most
important right here and provide links to the canonical documentation.


Main Interface
--------------

All of Requests' functionality can be accessed by these 7 methods.
They all return an instance of the :class:`Response <Response>` object.

.. autofunction:: partition


Request Sessions
----------------

.. _sessionapi:

.. autoclass:: TLE
   :inherited-members:
