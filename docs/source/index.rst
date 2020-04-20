.. Mapview documentation master file, created by
   sphinx-quickstart on Mon Aug 25 00:36:08 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Mapview's documentation!
===================================

:class:`MapView` is a Kivy widget specialized into tiles-based map rendering.

Requirements
------------

MapView is based on:

- `concurrent.futures <https://docs.python.org/3.4/library/concurrent.futures.html>`_:
  they are natives in Python 3.2. On previous Python
  version, you need to use `futures <https://pypi.python.org/pypi/futures>`_.
- `requests <https://pypi.python.org/pypi/requests>`_


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

Usage
-----

If you use Kivy garden, you can import the widget like this::

    from kivy.garden.mapview import MapView, MarkerMap
    map = MapView()

You can customize the default zoom and center the view on Lille by::

    map = MapView(zoom=9, lon=50.6394, lat=3.057)

Then, you can create marker and place them on the map. Normally, anything that
goes on a map should go on a :class:`MapLayer`. Hopefully, the :class:`MapView`
give an API for adding marker directly, and creates a :class:`MarkerMapLayer`
if you did'nt created one yet::

    m1 = MapMarker(lon=50.6394, lat=3.057)  # Lille
    m2 = MapMarker(lon=-33.867, lat=151.206)  # Sydney
    map.add_marker(m1)
    map.add_marker(m2)

You can also change the providers by:

1. using a provider key::

    map.map_source = "mapquest-osm"

2. using a new MapSource object::

    source = MapSource(url="http://my-custom-map.source.com/{z}/{x}/{y}.png",
                       cache_key="my-custom-map", tile_size=512,
                       image_ext="png", attribution="@ Myself")
    map.map_source = source


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
