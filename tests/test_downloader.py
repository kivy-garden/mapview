from unittest import mock

from kivy.clock import Clock

from kivy_garden.mapview.constants import CACHE_DIR
from kivy_garden.mapview.downloader import Downloader
from tests.utils import patch_requests_get


class TestDownloader:
    def teardown_method(self):
        Downloader._instance = None

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

    def test_download(self):
        """Checks download() callback."""
        callback = mock.Mock()
        url = "https://ifconfig.me/"
        downloader = Downloader.instance()
        assert len(downloader._futures) == 0
        with patch_requests_get() as m_get:
            downloader.download(url, callback)
        assert m_get.call_args_list == [mock.call(url)]
        assert callback.call_args_list == []
        assert len(downloader._futures) == 1
        Clock.tick()
        assert callback.call_args_list == [mock.call(url, mock.ANY)]
        assert len(downloader._futures) == 0

    def test_download_status_error(self):
        """
        Error status code should be checked.
        Callback function will not be invoked on error.
        """
        callback = mock.Mock()
        url = "https://httpstat.us/404"
        status_code = 404
        downloader = Downloader.instance()
        assert len(downloader._futures) == 0
        with patch_requests_get(status_code=status_code) as m_get:
            downloader.download(url, callback)
        assert m_get.call_args_list == [mock.call(url)]
        assert len(downloader._futures) == 1
        assert callback.call_args_list == []
        while len(downloader._futures) > 0:
            Clock.tick()
        assert callback.call_args_list == []
        assert len(downloader._futures) == 0
