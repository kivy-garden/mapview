from kivy_garden.mapview.downloader import Downloader
from kivy_garden.mapview.constants import CACHE_DIR


class TestDownloader:
    def test_instance(self):
        """Makes sure instance is a singleton."""
        assert Downloader._instance is None
        downloader = Downloader.instance()
        assert downloader == Downloader._instance
        assert type(downloader) == Downloader
        assert downloader.cache_dir == CACHE_DIR
        Downloader._instance = None
        new_cache_dir = "new_cache_dir"
        downloader = Downloader.instance(new_cache_dir)
        assert downloader.cache_dir == new_cache_dir
