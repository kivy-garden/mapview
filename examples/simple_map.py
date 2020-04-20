import sys

from kivy.base import runTouchApp

from kivy_garden.mapview import MapSource, MapView

kwargs = {}
if len(sys.argv) > 1:
    kwargs["map_source"] = MapSource(url=sys.argv[1], attribution="")

runTouchApp(MapView(**kwargs))
