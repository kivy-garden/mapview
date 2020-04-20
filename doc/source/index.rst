.. Flower documentation master file, created by
   sphinx-quickstart on Wed Jun 19 14:32:58 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Mapview's documentation!
===================================

:class:`MapView` is a Kivy widget specialized into tiles-based map rendering.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started.rst
   api.rst


Current limitations
-------------------

- The API is still moving, it may contain errors.
- Some providers can be slow or timeout. This is not an issue from MapView.
- If a tile is not correctly downloaded or missing from the provider, the error
  will be showed on the console, but nothing happen on the map itself. This can
  lead to a defect user experience.
- When leaving, `concurrent.futures` are joining all the threads created. It can
  stuck the application at a maximum time of 5 seconds (requests timeout). More
  if the network is unstable. There is no way to force it yet.
- The cache is not controlable, if the user move the map a lot, it can fill the
  disk easily. More control will be given later.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
