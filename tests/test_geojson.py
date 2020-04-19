import json
import os
from unittest import mock

from kivy.clock import Clock

from kivy_garden.mapview import MapView
from kivy_garden.mapview.geojson import GeoJsonMapLayer


def patch_requests_get(response_json=None):
    response = mock.Mock()
    response.return_value.json.return_value = response_json
    return mock.patch("requests.get", response)


def load_json(filename):
    test_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(test_dir, filename)
    with open(json_file_path) as f:
        json_file_content = f.read()
    return json.loads(json_file_content)


class TestGeoJsonMapLayer:
    def test_init_simple(self):
        """Makes sure we can initialize a simple GeoJsonMapLayer object."""
        kwargs = {}
        maplayer = GeoJsonMapLayer(**kwargs)
        assert maplayer.source == ""
        assert maplayer.geojson is None
        assert maplayer.cache_dir == "cache"

    def test_init_source(self):
        """
        Providing the source from http(s).
        The json object should get downloaded using the requests library.
        """
        source = "https://storage.googleapis.com/maps-devrel/google.json"
        kwargs = {"source": source}
        response_json = {
            "type": "FeatureCollection",
        }
        with patch_requests_get(response_json) as m_get:
            maplayer = GeoJsonMapLayer(**kwargs)
        assert maplayer.source == source
        assert maplayer.geojson is None
        Clock.tick()
        assert maplayer.geojson == response_json
        assert m_get.call_args_list == [mock.call(source)]

    def test_init_geojson(self):
        """Providing the geojson directly, polygons should get added."""
        options = {}
        mapview = MapView(**options)
        geojson = {}
        kwargs = {"geojson": geojson}
        maplayer = GeoJsonMapLayer(**kwargs)
        mapview.add_layer(maplayer)
        Clock.tick()
        assert maplayer.source == ""
        assert maplayer.geojson == geojson
        assert len(maplayer.canvas_line.children) == 0
        assert len(maplayer.canvas_polygon.children) == 3
        assert len(maplayer.g_canvas_polygon.children) == 0
        geojson = load_json("maps-devrel-google.json")
        kwargs = {"geojson": geojson}
        maplayer = GeoJsonMapLayer(**kwargs)
        mapview = MapView(**options)
        mapview.add_layer(maplayer)
        Clock.tick()
        assert maplayer.source == ""
        assert maplayer.geojson == geojson
        assert len(maplayer.canvas_line.children) == 0
        assert len(maplayer.canvas_polygon.children) == 3
        assert len(maplayer.g_canvas_polygon.children) == 132
