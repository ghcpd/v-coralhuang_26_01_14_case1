import unittest

import pytest

from fake import FakeUserAgent, UserAgent, settings

VERSION = "1.0.0"


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
        fallback = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
        )

        ua = UserAgent()
        self.assertEqual(ua.non_existing, fallback)
        self.assertEqual(ua["non_existing"], fallback)

    def test_fake_fallback_dictionary(self):
        fallback = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
        )

        ua = UserAgent()
        self.assertIsInstance(ua.getBrowser("non_existing"), dict)
        self.assertEqual(ua.getBrowser("non_existing").get("useragent"), fallback)

    def test_fake_fallback_str_types(self):
        with pytest.raises(TypeError):
            UserAgent(fallback=True)

    def test_fake_browser_str_or_list_types(self):
        with pytest.raises(TypeError):
            UserAgent(browsers=52)

    def test_fake_os_str_or_list_types(self):
        with pytest.raises(TypeError):
            UserAgent(os=23.4)

    def test_fake_platform_str_or_list_types(self):
        with pytest.raises(TypeError):
            UserAgent(platforms=5.0)

    def test_fake_percentage_float_types(self):
        with pytest.raises(TypeError):
            UserAgent(min_percentage="")

    def test_fake_safe_attrs_iterable_str_types(self):
        with pytest.raises(TypeError):
            UserAgent(safe_attrs={})

        with pytest.raises(ValueError):
            UserAgent(safe_attrs=[66])

    def test_fake_safe_attrs(self):
        ua = UserAgent(safe_attrs=("__injections__",))

        with pytest.raises(AttributeError):
            ua.__injections__  # noqa: B018

    def test_fake_version(self):
        assert VERSION == "1.0.0"

    def test_fake_aliases(self):
        assert FakeUserAgent is UserAgent

    def test_no_shared_mutable_defaults(self):
        ua1 = UserAgent()
        ua1.browsers.append("opera")
        ua1.os.append("beos")
        ua1.platforms.append("console")

        ua2 = UserAgent()

        assert "opera" not in ua2.browsers
        assert "beos" not in ua2.os
        assert "console" not in ua2.platforms

    def test_iterable_inputs_and_invalid_types(self):
        ua = UserAgent(
            browsers=["chrome", "edge"],
            os=("windows", "linux"),
            platforms={"pc", "mobile"},
        )

        assert {"chrome", "edge"} == set(ua.browsers)
        assert {"windows", "linux", "win10", "win7"} >= set(ua.os)
        assert {"pc", "mobile"} == set(ua.platforms)

        with pytest.raises(ValueError):
            UserAgent(browsers=[])

        with pytest.raises(TypeError):
            UserAgent(min_version=None)

        with pytest.raises(ValueError):
            UserAgent(platforms={1})
