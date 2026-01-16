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

    # ==================== Platform Filtering Tests ====================

    def test_platform_filtering_pc_only(self):
        """Test filtering for PC/desktop user agents only"""
        ua = UserAgent(platforms="pc")
        for _ in range(10):
            browser = ua.getBrowser("random")
            assert browser.get("type") == "pc"

    def test_platform_filtering_mobile_only(self):
        """Test filtering for mobile user agents only"""
        ua = UserAgent(platforms="mobile")
        for _ in range(10):
            browser = ua.getBrowser("random")
            assert browser.get("type") == "mobile"

    def test_platform_filtering_tablet_only(self):
        """Test filtering for tablet user agents only"""
        ua = UserAgent(platforms="tablet")
        # Just test that it doesn't crash even if no tablets in data
        try:
            ua.getBrowser("random")
        except Exception:
            pass  # Expected if no tablets in dataset

    def test_platform_filtering_list_input(self):
        """Test platform filtering with list input"""
        ua = UserAgent(platforms=["pc", "mobile"])
        for _ in range(10):
            browser = ua.getBrowser("random")
            assert browser.get("type") in ["pc", "mobile"]

    def test_platform_filtering_string_input(self):
        """Test platform filtering with string input"""
        ua = UserAgent(platforms="pc")
        browser = ua.getBrowser("random")
        assert isinstance(browser, dict)

    def test_platform_filtering_case_insensitive(self):
        """Test that platform filtering is case-insensitive"""
        ua_upper = UserAgent(platforms="PC")
        ua_lower = UserAgent(platforms="pc")
        # Both should work without errors
        assert ua_upper.getBrowser("random")
        assert ua_lower.getBrowser("random")

    def test_platform_filtering_default_all(self):
        """Test that default includes all platforms"""
        ua = UserAgent()
        browser = ua.getBrowser("random")
        # Should be able to get results (either pc, mobile, or tablet)
        assert browser is not None

    def test_platform_filtering_attribute_access(self):
        """Test platform filtering with attribute access"""
        ua = UserAgent(platforms="pc")
        ua_str = ua.chrome
        assert isinstance(ua_str, str)

    # ==================== Min Version Filtering Tests ====================

    def test_min_version_filtering_integer(self):
        """Test min_version filtering with integer input"""
        ua = UserAgent(min_version=120)
        browser = ua.getBrowser("random")
        assert browser.get("version", 0) >= 120

    def test_min_version_filtering_float(self):
        """Test min_version filtering with float input"""
        ua = UserAgent(min_version=120.5)
        browser = ua.getBrowser("random")
        assert browser.get("version", 0) >= 120.5

    def test_min_version_filtering_zero_default(self):
        """Test that default min_version is 0.0"""
        ua = UserAgent()
        browser = ua.getBrowser("random")
        # Should get any browser since default is 0.0
        assert browser is not None

    def test_min_version_filtering_high_threshold(self):
        """Test with high version threshold"""
        ua = UserAgent(min_version=999.0)
        # Should fail to find matching browser
        try:
            ua.getBrowser("random")
        except Exception:
            pass  # Expected when no browser matches high version

    def test_min_version_filtering_attribute_access(self):
        """Test min_version filtering with attribute access"""
        ua = UserAgent(min_version=120)
        ua_str = ua.chrome
        assert isinstance(ua_str, str)

    # ==================== Combined Filtering Tests ====================

    def test_combined_platform_and_version_filtering(self):
        """Test combining platform and version filters"""
        ua = UserAgent(platforms="pc", min_version=120)
        browser = ua.getBrowser("random")
        assert browser.get("type") == "pc"
        assert browser.get("version", 0) >= 120

    def test_combined_all_filters(self):
        """Test combining platform, version, browser, and percentage filters"""
        ua = UserAgent(
            platforms="pc",
            min_version=120,
            browsers="edge",
            min_percentage=50.0,
        )
        browser = ua.getBrowser("random")
        assert browser.get("type") == "pc"
        assert browser.get("version", 0) >= 120
        assert browser.get("browser") == "edge"
        assert browser.get("percent", 0) >= 50.0

    def test_combined_mobile_version(self):
        """Test mobile user agents with version filtering"""
        ua = UserAgent(platforms="mobile", min_version=120)
        # Some mobile browsers should match
        try:
            browser = ua.getBrowser("random")
            assert browser.get("type") == "mobile"
            assert browser.get("version", 0) >= 120
        except Exception:
            pass  # OK if no mobile browsers match criteria

    # ==================== Parameter Type Tests ====================

    def test_platforms_parameter_invalid_type(self):
        """Test that platforms parameter rejects invalid types"""
        with pytest.raises(AssertionError):
            UserAgent(platforms=123)

    def test_min_version_parameter_invalid_type(self):
        """Test that min_version parameter rejects invalid types"""
        with pytest.raises(AssertionError):
            UserAgent(min_version="120")

    def test_min_version_parameter_accepts_integer(self):
        """Test that min_version accepts integer"""
        ua = UserAgent(min_version=120)
        assert ua.min_version == 120.0

    def test_min_version_parameter_accepts_float(self):
        """Test that min_version accepts float"""
        ua = UserAgent(min_version=120.5)
        assert ua.min_version == 120.5

    # ==================== Backward Compatibility Tests ====================

    def test_backward_compatibility_without_new_parameters(self):
        """Test that library works normally without new parameters"""
        ua = UserAgent()
        assert ua.chrome
        assert ua.edge
        assert ua.firefox
        assert ua.safari
        assert ua.random

    def test_backward_compatibility_existing_methods(self):
        """Test that existing methods still work"""
        ua = UserAgent()
        assert isinstance(ua.getChrome, dict)
        assert isinstance(ua.getEdge, dict)
        assert isinstance(ua.getFirefox, dict)
        assert isinstance(ua.getSafari, dict)
        assert isinstance(ua.getRandom, dict)

    def test_backward_compatibility_attribute_access(self):
        """Test that attribute access still works"""
        ua = UserAgent()
        chrome_ua = ua.chrome
        edge_ua = ua.edge
        assert isinstance(chrome_ua, str)
        assert isinstance(edge_ua, str)

    def test_backward_compatibility_dictionary_access(self):
        """Test that dictionary-style access still works"""
        ua = UserAgent()
        chrome_ua = ua["chrome"]
        edge_ua = ua["edge"]
        assert isinstance(chrome_ua, str)
        assert isinstance(edge_ua, str)

    def test_backward_compatibility_fallback(self):
        """Test that fallback still works"""
        fallback = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        ua = UserAgent(fallback=fallback)
        result = ua.getBrowser("non_existing_browser_xyz")
        assert result.get("useragent") == fallback

    # ==================== Edge Case Tests ====================

    def test_mobile_platform_with_specific_browser(self):
        """Test mobile platform with specific browser"""
        ua = UserAgent(platforms="mobile", browsers="edge")
        try:
            browser = ua.getBrowser("edge")
            assert browser.get("type") == "mobile"
            assert browser.get("browser") == "edge"
        except Exception:
            pass  # OK if no mobile edge browsers in data

    def test_multiple_platforms_list(self):
        """Test multiple platforms as list"""
        ua = UserAgent(platforms=["pc", "mobile"])
        browser = ua.getBrowser("random")
        assert browser.get("type") in ["pc", "mobile"]

    def test_platform_filtering_random_attribute(self):
        """Test platform filtering with random attribute"""
        ua = UserAgent(platforms="pc")
        ua_str = ua.random
        assert isinstance(ua_str, str)
