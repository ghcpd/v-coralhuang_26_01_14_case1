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

class TestMutableDefaults(unittest.TestCase):
    """Tests to ensure mutable default parameters don't cause state leakage."""

    def test_browsers_not_shared_between_instances(self):
        """Verify that modifying browsers on one instance doesn't affect others."""
        ua1 = UserAgent()
        original_browsers_1 = ua1.browsers.copy()
        
        # Mutate the first instance
        ua1.browsers.append("opera")
        
        # Create a second instance
        ua2 = UserAgent()
        
        # Verify the second instance is not affected
        assert "opera" not in ua2.browsers
        assert ua2.browsers == original_browsers_1
    
    def test_os_not_shared_between_instances(self):
        """Verify that modifying os on one instance doesn't affect others."""
        ua1 = UserAgent()
        original_os_1 = ua1.os.copy()
        
        # Mutate the first instance
        ua1.os.append("custom_os")
        
        # Create a second instance
        ua2 = UserAgent()
        
        # Verify the second instance is not affected
        assert "custom_os" not in ua2.os
        assert ua2.os == original_os_1
    
    def test_platforms_not_shared_between_instances(self):
        """Verify that modifying platforms on one instance doesn't affect others."""
        ua1 = UserAgent()
        original_platforms_1 = ua1.platforms.copy()
        
        # Mutate the first instance
        ua1.platforms.append("console")
        
        # Create a second instance
        ua2 = UserAgent()
        
        # Verify the second instance is not affected
        assert "console" not in ua2.platforms
        assert ua2.platforms == original_platforms_1
    
    def test_multiple_mutations_isolated(self):
        """Verify that multiple instances can be mutated independently."""
        ua1 = UserAgent()
        ua2 = UserAgent()
        ua3 = UserAgent()
        
        # Mutate each instance differently
        ua1.browsers.append("custom1")
        ua2.browsers.append("custom2")
        ua3.browsers.append("custom3")
        
        # Verify each instance has only its own mutation
        assert "custom1" in ua1.browsers
        assert "custom1" not in ua2.browsers
        assert "custom1" not in ua3.browsers
        
        assert "custom2" not in ua1.browsers
        assert "custom2" in ua2.browsers
        assert "custom2" not in ua3.browsers
        
        assert "custom3" not in ua1.browsers
        assert "custom3" not in ua2.browsers
        assert "custom3" in ua3.browsers


class TestIterableFlexibility(unittest.TestCase):
    """Tests to ensure different iterable types work correctly."""

    def test_browsers_accepts_list(self):
        """Verify that browsers parameter accepts list."""
        ua = UserAgent(browsers=["chrome", "firefox"])
        assert ua.browsers == ["chrome", "firefox"]
    
    def test_browsers_accepts_tuple(self):
        """Verify that browsers parameter accepts tuple."""
        ua = UserAgent(browsers=("chrome", "firefox"))
        assert ua.browsers == ["chrome", "firefox"]
        assert isinstance(ua.browsers, list)
    
    def test_browsers_accepts_set(self):
        """Verify that browsers parameter accepts set."""
        browsers_set = {"chrome", "firefox"}
        ua = UserAgent(browsers=browsers_set)
        # Set order is not guaranteed, so check membership
        assert set(ua.browsers) == browsers_set
        assert isinstance(ua.browsers, list)
    
    def test_browsers_accepts_string(self):
        """Verify that browsers parameter accepts string."""
        ua = UserAgent(browsers="chrome")
        assert ua.browsers == ["chrome"]
    
    def test_os_accepts_different_iterables(self):
        """Verify that os parameter accepts different iterable types."""
        ua_list = UserAgent(os=["windows", "linux"])
        ua_tuple = UserAgent(os=("windows", "linux"))
        ua_set = UserAgent(os={"windows", "linux"})
        
        # All should produce lists with the same content (after OS replacement)
        assert isinstance(ua_list.os, list)
        assert isinstance(ua_tuple.os, list)
        assert isinstance(ua_set.os, list)
    
    def test_platforms_accepts_different_iterables(self):
        """Verify that platforms parameter accepts different iterable types."""
        ua_list = UserAgent(platforms=["pc", "mobile"])
        ua_tuple = UserAgent(platforms=("pc", "mobile"))
        ua_set = UserAgent(platforms={"pc", "mobile"})
        
        assert isinstance(ua_list.platforms, list)
        assert isinstance(ua_tuple.platforms, list)
        assert isinstance(ua_set.platforms, list)
    
    def test_invalid_browsers_type_raises_typeerror(self):
        """Verify that invalid browsers type raises TypeError."""
        with pytest.raises(TypeError):
            UserAgent(browsers=123)
        
        with pytest.raises(TypeError):
            UserAgent(browsers=45.6)
        
        with pytest.raises(TypeError):
            UserAgent(browsers=True)
    
    def test_invalid_os_type_raises_typeerror(self):
        """Verify that invalid os type raises TypeError."""
        with pytest.raises(TypeError):
            UserAgent(os=123)
        
        with pytest.raises((TypeError, ValueError)):
            # Empty dict is technically iterable, so it may raise ValueError instead
            UserAgent(os={})
    
    def test_invalid_platforms_type_raises_typeerror(self):
        """Verify that invalid platforms type raises TypeError."""
        with pytest.raises(TypeError):
            UserAgent(platforms=123)
    
    def test_browsers_with_non_string_elements_raises_valueerror(self):
        """Verify that browsers with non-string elements raises ValueError."""
        with pytest.raises(ValueError):
            UserAgent(browsers=["chrome", 123])
        
        with pytest.raises(ValueError):
            UserAgent(browsers=[None, "firefox"])
    
    def test_empty_browsers_raises_valueerror(self):
        """Verify that empty browsers raises ValueError."""
        with pytest.raises(ValueError):
            UserAgent(browsers=[])
    
    def test_empty_os_raises_valueerror(self):
        """Verify that empty os raises ValueError."""
        with pytest.raises(ValueError):
            UserAgent(os=[])
    
    def test_empty_platforms_raises_valueerror(self):
        """Verify that empty platforms raises ValueError."""
        with pytest.raises(ValueError):
            UserAgent(platforms=[])


class TestErrorTypes(unittest.TestCase):
    """Tests to ensure correct error types are raised."""

    def test_no_assertionerror_from_init(self):
        """Verify that __init__ never raises AssertionError."""
        invalid_inputs = [
            {"browsers": 123},
            {"os": 45.6},
            {"platforms": True},
            {"min_percentage": "invalid"},
            {"min_version": "invalid"},
            {"fallback": 123},
            {"safe_attrs": {}},
        ]
        
        for kwargs in invalid_inputs:
            try:
                UserAgent(**kwargs)
                # If no exception, that's unexpected but not an AssertionError
            except AssertionError:
                self.fail(f"AssertionError raised for {kwargs}, should raise TypeError or ValueError")
            except (TypeError, ValueError):
                # Expected behavior
                pass
    
    def test_min_percentage_invalid_type_raises_typeerror(self):
        """Verify that invalid min_percentage type raises TypeError."""
        with pytest.raises(TypeError):
            UserAgent(min_percentage="invalid")
        
        with pytest.raises(TypeError):
            UserAgent(min_percentage=[])
    
    def test_min_version_invalid_type_raises_typeerror(self):
        """Verify that invalid min_version type raises TypeError."""
        with pytest.raises(TypeError):
            UserAgent(min_version="invalid")
        
        with pytest.raises(TypeError):
            UserAgent(min_version=None)
    
    def test_fallback_invalid_type_raises_typeerror(self):
        """Verify that invalid fallback type raises TypeError."""
        with pytest.raises(TypeError):
            UserAgent(fallback=123)
        
        with pytest.raises(TypeError):
            UserAgent(fallback=None)
    
    def test_safe_attrs_invalid_type_raises_typeerror(self):
        """Verify that invalid safe_attrs type raises TypeError."""
        with pytest.raises(TypeError):
            UserAgent(safe_attrs={})
        
        with pytest.raises(TypeError):
            UserAgent(safe_attrs="string")
    
    def test_safe_attrs_non_string_elements_raises_valueerror(self):
        """Verify that safe_attrs with non-string elements raises ValueError."""
        with pytest.raises(ValueError):
            UserAgent(safe_attrs=[123])
        
        with pytest.raises(ValueError):
            UserAgent(safe_attrs=(None, "valid"))