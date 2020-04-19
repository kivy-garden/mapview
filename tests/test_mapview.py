from kivy_garden.mapview import MapView


class TestMapView:
    def test_init_simple_map(self):
        """Makes sure we can initialize a simple MapView object."""
        kwargs = {}
        mapview = MapView(**kwargs)
        assert len(mapview.children) == 2
