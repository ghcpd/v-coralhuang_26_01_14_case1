import unittest

import pytest

import settings
from fake import FakeUserAgent, UserAgent

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

    def test_platform_filtering_string(self):
        ua = UserAgent(platforms="mobile")
        # Should only return mobile user agents
        for _ in range(10):  # Test multiple times to ensure consistency
            ua_str = ua.random
            browser_data = ua.getRandom
            self.assertEqual(browser_data["type"], "mobile")

    def test_platform_filtering_list(self):
        ua = UserAgent(platforms=["mobile", "tablet"])
        # Should only return mobile or tablet user agents
        for _ in range(10):
            browser_data = ua.getRandom
            self.assertIn(browser_data["type"], ["mobile", "tablet"])

    def test_platform_filtering_invalid(self):
        with pytest.raises(AssertionError):
            UserAgent(platforms="invalid")

    def test_min_version_filtering_int(self):
        ua = UserAgent(min_version=120)
        for _ in range(10):
            browser_data = ua.getRandom
            self.assertGreaterEqual(browser_data["version"], 120.0)

    def test_min_version_filtering_float(self):
        ua = UserAgent(min_version=120.5)
        for _ in range(10):
            browser_data = ua.getRandom
            self.assertGreaterEqual(browser_data["version"], 120.5)

    def test_min_version_filtering_invalid(self):
        with pytest.raises(AssertionError):
            UserAgent(min_version="120")

    def test_combined_filtering(self):
        ua = UserAgent(platforms="pc", min_version=120)
        for _ in range(10):
            browser_data = ua.getRandom
            self.assertEqual(browser_data["type"], "pc")
            self.assertGreaterEqual(browser_data["version"], 120.0)

    def test_backward_compatibility(self):
        # Test that existing functionality still works without new parameters
        ua = UserAgent()
        self.assertTrue(ua.chrome)
        self.assertTrue(ua.random)
        browser_data = ua.getRandom
        self.assertIsInstance(browser_data, dict)
        self.assertIn("useragent", browser_data)
