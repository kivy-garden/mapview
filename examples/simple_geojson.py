import sys

from kivy.base import runTouchApp

from kivy_garden.mapview import MapMarker, MapView
from kivy_garden.mapview.geojson import GeoJsonMapLayer
from kivy_garden.mapview.utils import get_zoom_for_radius, haversine

if len(sys.argv) > 1:
    source = sys.argv[1]
else:
    source = "https://storage.googleapis.com/maps-devrel/google.json"

options = {}
layer = GeoJsonMapLayer(source=source)

if layer.geojson:
    # try to auto center the map on the source
    lon, lat = layer.center
    options["lon"] = lon
    options["lat"] = lat
    min_lon, max_lon, min_lat, max_lat = layer.bounds
    radius = haversine(min_lon, min_lat, max_lon, max_lat)
    zoom = get_zoom_for_radius(radius, lat)
    options["zoom"] = zoom

view = MapView(**options)
view.add_layer(layer)

if layer.geojson:
    # create marker if they exists
    count = 0

    def create_marker(feature):
        global count
        geometry = feature["geometry"]
        if geometry["type"] != "Point":
            return
        lon, lat = geometry["coordinates"]
        marker = MapMarker(lon=lon, lat=lat)
        view.add_marker(marker)
        count += 1

    layer.traverse_feature(create_marker)
    if count:
        print("Loaded {} markers".format(count))

runTouchApp(view)
