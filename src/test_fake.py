import unittest

import pytest

from . import settings
from .fake import FakeUserAgent, UserAgent

VERSION = settings.__version__


class TestFake(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_fake_init(self):
        ua = UserAgent()

        self.assertTrue(ua.chrome)
        self.assertIsInstance(ua.chrome, str)
        self.assertTrue(ua.edge)
        self.assertIsInstance(ua.edge, str)
        self.assertTrue(ua["internet explorer"])
        self.assertIsInstance(ua["internet explorer"], str)
        self.assertTrue(ua.firefox)
        self.assertIsInstance(ua.firefox, str)
        self.assertTrue(ua.safari)
        self.assertIsInstance(ua.safari, str)
        self.assertTrue(ua.random)
        self.assertIsInstance(ua.random, str)

        self.assertTrue(ua.getChrome)
        self.assertIsInstance(ua.getChrome, dict)
        self.assertTrue(ua.getEdge)
        self.assertIsInstance(ua.getEdge, dict)
        self.assertTrue(ua.getFirefox)
        self.assertIsInstance(ua.getFirefox, dict)
        self.assertTrue(ua.getSafari)
        self.assertIsInstance(ua.getSafari, dict)
        self.assertTrue(ua.getRandom)
        self.assertIsInstance(ua.getRandom, dict)

    def test_fake_probe_user_agent_browsers(self):
        ua = UserAgent()
        ua.edge  # noqa: B018
        ua.google  # noqa: B018
        ua.chrome  # noqa: B018
        ua.googlechrome  # noqa: B018
        ua.google_chrome  # noqa: B018
        ua["google chrome"]  # noqa: B018
        ua.firefox  # noqa: B018
        ua.ff  # noqa: B018
        ua.safari  # noqa: B018
        ua.random  # noqa: B018
        ua["random"]  # noqa: B018
        ua.getEdge  # noqa: B018
        ua.getChrome  # noqa: B018
        ua.getFirefox  # noqa: B018
        ua.getSafari  # noqa: B018
        ua.getRandom  # noqa: B018

    def test_fake_data_browser_type(self):
        ua = UserAgent()
        assert isinstance(ua.data_browsers, list)

    def test_fake_fallback(self):
        fallback = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

        ua = UserAgent()
        self.assertEqual(ua.non_existing, fallback)
        self.assertEqual(ua["non_existing"], fallback)

    def test_fake_fallback_dictionary(self):
        fallback = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

        ua = UserAgent()
        self.assertIsInstance(ua.getBrowser("non_existing"), dict)
        self.assertEqual(ua.getBrowser("non_existing").get("useragent"), fallback)

    def test_fake_fallback_str_types(self):
        with pytest.raises(AssertionError):
            UserAgent(fallback=True)

    def test_fake_browser_str_or_list_types(self):
        with pytest.raises(AssertionError):
            UserAgent(browsers=52)

    def test_fake_os_str_or_list_types(self):
        with pytest.raises(AssertionError):
            UserAgent(os=23.4)

    def test_fake_percentage_float_types(self):
        with pytest.raises(AssertionError):
            UserAgent(min_percentage="")

    def test_fake_safe_attrs_iterable_str_types(self):
        with pytest.raises(AssertionError):
            UserAgent(safe_attrs={})

        with pytest.raises(AssertionError):
            UserAgent(safe_attrs=[66])

    def test_fake_safe_attrs(self):
        ua = UserAgent(safe_attrs=("__injections__",))

        with pytest.raises(AttributeError):
            ua.__injections__  # noqa: B018

    def test_fake_version(self):
        assert VERSION == settings.__version__

    def test_fake_aliases(self):
        assert FakeUserAgent is UserAgent

    def test_platform_filter_string_and_list(self):
        # string input
        ua = UserAgent(platforms="mobile")
        result = ua.getRandom
        assert result.get("type") == "mobile"

        # list input
        ua2 = UserAgent(platforms=["tablet"])
        result2 = ua2.getRandom
        assert result2.get("type") == "tablet"

    def test_min_version_supports_int_and_float(self):
        ua = UserAgent(min_version=122)
        assert float(ua.getRandom.get("version")) >= 122.0

        ua2 = UserAgent(min_version=121.5)
        assert float(ua2.getRandom.get("version")) >= 121.5

    def test_combined_platform_and_version_filtering(self):
        ua = UserAgent(platforms=["mobile"], min_version=121)
        entry = ua.getBrowser("chrome")
        assert entry.get("type") == "mobile"
        assert float(entry.get("version")) >= 121.0

    def test_default_behavior_unchanged_when_no_new_params(self):
        ua = UserAgent()
        # should return some UA and include supported types from data
        entry = ua.getRandom
        assert entry.get("type") in ("pc", "mobile", "tablet")

