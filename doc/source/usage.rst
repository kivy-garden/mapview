.. _usage:

*****
Usage
*****


Basic Usage
-----------

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
