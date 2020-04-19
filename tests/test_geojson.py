from kivy_garden.mapview.geojson import GeoJsonMapLayer


class TestGeoJsonMapLayer:
    def test_init_simple(self):
        """Makes sure we can initialize a simple GeoJsonMapLayer object."""
        kwargs = {}
        maplayer = GeoJsonMapLayer(**kwargs)
        assert maplayer.source == ""
        assert maplayer.geojson is None
        assert maplayer.cache_dir == "cache"
