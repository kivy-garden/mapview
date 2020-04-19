from unittest import mock

from kivy.clock import Clock

from kivy_garden.mapview.geojson import GeoJsonMapLayer


def patch_requests_get(response_json=None):
    response = mock.Mock()
    response.return_value.json.return_value = response_json
    return mock.patch("requests.get", response)


class TestGeoJsonMapLayer:
    def test_init_simple(self):
        """Makes sure we can initialize a simple GeoJsonMapLayer object."""
        kwargs = {}
        maplayer = GeoJsonMapLayer(**kwargs)
        assert maplayer.source == ""
        assert maplayer.geojson is None
        assert maplayer.cache_dir == "cache"

    def test_http_source(self):
        """Pulls the source from http(s)."""
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
