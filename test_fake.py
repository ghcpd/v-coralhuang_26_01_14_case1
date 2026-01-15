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

        with pytest.raises(TypeError):
            UserAgent(safe_attrs=[66])

    def test_fake_safe_attrs(self):
        ua = UserAgent(safe_attrs=("__injections__",))

        with pytest.raises(AttributeError):
            ua.__injections__  # noqa: B018

    def test_fake_version(self):
        assert VERSION == "1.0.0"

    def test_fake_aliases(self):
        assert FakeUserAgent is UserAgent


class TestMutableDefaultRegression(unittest.TestCase):
    """
    Regression tests to ensure mutable default parameter anti-pattern is fixed.
    
    These tests verify that each instance gets its own independent copy of
    list/set attributes, preventing cross-instance state leakage.
    """

    def test_no_shared_browsers_default(self):
        """Mutating browsers on one instance should not affect another instance."""
        ua1 = FakeUserAgent()
        original_browsers = ua1.browsers.copy()
        
        # Mutate the browsers list on ua1
        ua1.browsers.append("opera")
        
        # Create a second instance
        ua2 = FakeUserAgent()
        
        # ua2 should have the original default browsers, not including "opera"
        self.assertNotIn("opera", ua2.browsers)
        self.assertEqual(set(ua2.browsers), set(original_browsers))

    def test_no_shared_os_default(self):
        """Mutating os on one instance should not affect another instance."""
        ua1 = FakeUserAgent()
        original_os = ua1.os.copy()
        
        # Mutate the os list on ua1
        ua1.os.append("custom_os")
        
        # Create a second instance
        ua2 = FakeUserAgent()
        
        # ua2 should have the original default os, not including "custom_os"
        self.assertNotIn("custom_os", ua2.os)
        self.assertEqual(set(ua2.os), set(original_os))

    def test_no_shared_platforms_default(self):
        """Mutating platforms on one instance should not affect another instance."""
        ua1 = FakeUserAgent()
        original_platforms = ua1.platforms.copy()
        
        # Mutate the platforms list on ua1
        ua1.platforms.append("smart_tv")
        
        # Create a second instance
        ua2 = FakeUserAgent()
        
        # ua2 should have the original default platforms, not including "smart_tv"
        self.assertNotIn("smart_tv", ua2.platforms)
        self.assertEqual(set(ua2.platforms), set(original_platforms))

    def test_no_shared_safe_attrs_default(self):
        """Mutating safe_attrs on one instance should not affect another instance."""
        ua1 = FakeUserAgent()
        
        # Mutate the safe_attrs set on ua1
        ua1.safe_attrs.add("__custom_attr__")
        
        # Create a second instance
        ua2 = FakeUserAgent()
        
        # ua2 should have an empty safe_attrs, not including "__custom_attr__"
        self.assertNotIn("__custom_attr__", ua2.safe_attrs)
        self.assertEqual(ua2.safe_attrs, set())

    def test_multiple_instances_independent(self):
        """Create multiple instances and verify all are independent."""
        instances = [FakeUserAgent() for _ in range(5)]
        
        # Mutate each instance differently
        for i, ua in enumerate(instances):
            ua.browsers.append(f"browser_{i}")
            ua.os.append(f"os_{i}")
            ua.platforms.append(f"platform_{i}")
        
        # Create a fresh instance
        fresh_ua = FakeUserAgent()
        
        # Fresh instance should have no custom values
        for i in range(5):
            self.assertNotIn(f"browser_{i}", fresh_ua.browsers)
            self.assertNotIn(f"os_{i}", fresh_ua.os)
            self.assertNotIn(f"platform_{i}", fresh_ua.platforms)


class TestIterableFlexibility(unittest.TestCase):
    """Tests that different iterable types work correctly for list parameters."""

    def test_browsers_accepts_list(self):
        """browsers parameter accepts a list."""
        ua = FakeUserAgent(browsers=["chrome", "firefox"])
        self.assertEqual(ua.browsers, ["chrome", "firefox"])

    def test_browsers_accepts_tuple(self):
        """browsers parameter accepts a tuple."""
        ua = FakeUserAgent(browsers=("chrome", "firefox"))
        self.assertEqual(ua.browsers, ["chrome", "firefox"])

    def test_browsers_accepts_set(self):
        """browsers parameter accepts a set."""
        ua = FakeUserAgent(browsers={"chrome", "firefox"})
        self.assertEqual(set(ua.browsers), {"chrome", "firefox"})

    def test_browsers_accepts_string(self):
        """browsers parameter accepts a single string."""
        ua = FakeUserAgent(browsers="chrome")
        self.assertEqual(ua.browsers, ["chrome"])

    def test_os_accepts_list(self):
        """os parameter accepts a list."""
        ua = FakeUserAgent(os=["linux", "macos"])
        self.assertEqual(ua.os, ["linux", "macos"])

    def test_os_accepts_tuple(self):
        """os parameter accepts a tuple."""
        ua = FakeUserAgent(os=("linux", "macos"))
        self.assertEqual(ua.os, ["linux", "macos"])

    def test_os_accepts_set(self):
        """os parameter accepts a set."""
        ua = FakeUserAgent(os={"linux", "macos"})
        self.assertEqual(set(ua.os), {"linux", "macos"})

    def test_os_accepts_string(self):
        """os parameter accepts a single string."""
        ua = FakeUserAgent(os="linux")
        self.assertEqual(ua.os, ["linux"])

    def test_platforms_accepts_list(self):
        """platforms parameter accepts a list."""
        ua = FakeUserAgent(platforms=["pc", "mobile"])
        self.assertEqual(ua.platforms, ["pc", "mobile"])

    def test_platforms_accepts_tuple(self):
        """platforms parameter accepts a tuple."""
        ua = FakeUserAgent(platforms=("pc", "mobile"))
        self.assertEqual(ua.platforms, ["pc", "mobile"])

    def test_platforms_accepts_set(self):
        """platforms parameter accepts a set."""
        ua = FakeUserAgent(platforms={"pc", "mobile"})
        self.assertEqual(set(ua.platforms), {"pc", "mobile"})

    def test_platforms_accepts_string(self):
        """platforms parameter accepts a single string."""
        ua = FakeUserAgent(platforms="pc")
        self.assertEqual(ua.platforms, ["pc"])

    def test_safe_attrs_accepts_list(self):
        """safe_attrs parameter accepts a list."""
        ua = FakeUserAgent(safe_attrs=["attr1", "attr2"])
        self.assertEqual(ua.safe_attrs, {"attr1", "attr2"})

    def test_safe_attrs_accepts_tuple(self):
        """safe_attrs parameter accepts a tuple."""
        ua = FakeUserAgent(safe_attrs=("attr1", "attr2"))
        self.assertEqual(ua.safe_attrs, {"attr1", "attr2"})

    def test_safe_attrs_accepts_set(self):
        """safe_attrs parameter accepts a set."""
        ua = FakeUserAgent(safe_attrs={"attr1", "attr2"})
        self.assertEqual(ua.safe_attrs, {"attr1", "attr2"})

    def test_generator_expression_works(self):
        """Iterable from generator expression should work."""
        ua = FakeUserAgent(browsers=(b for b in ["chrome", "firefox"]))
        self.assertEqual(ua.browsers, ["chrome", "firefox"])


class TestErrorTypeCorrectness(unittest.TestCase):
    """
    Tests that proper exception types are raised instead of AssertionError.
    
    This ensures that the assert statements have been replaced with proper
    validation that raises TypeError or ValueError.
    """

    def test_browsers_invalid_type_raises_typeerror(self):
        """Invalid browsers type should raise TypeError, not AssertionError."""
        with pytest.raises(TypeError):
            UserAgent(browsers=123)
        
        with pytest.raises(TypeError):
            UserAgent(browsers=12.5)
        
        with pytest.raises(TypeError):
            UserAgent(browsers=True)

    def test_browsers_invalid_contents_raises_typeerror(self):
        """browsers containing non-strings should raise TypeError."""
        with pytest.raises(TypeError):
            UserAgent(browsers=[123, "chrome"])
        
        with pytest.raises(TypeError):
            UserAgent(browsers=["chrome", None])

    def test_browsers_empty_raises_valueerror(self):
        """Empty browsers should raise ValueError."""
        with pytest.raises(ValueError):
            UserAgent(browsers=[])
        
        with pytest.raises(ValueError):
            UserAgent(browsers="")

    def test_os_invalid_type_raises_typeerror(self):
        """Invalid os type should raise TypeError, not AssertionError."""
        with pytest.raises(TypeError):
            UserAgent(os=123)
        
        with pytest.raises(TypeError):
            UserAgent(os=True)

    def test_os_empty_raises_valueerror(self):
        """Empty os should raise ValueError."""
        with pytest.raises(ValueError):
            UserAgent(os=[])

    def test_platforms_invalid_type_raises_typeerror(self):
        """Invalid platforms type should raise TypeError, not AssertionError."""
        with pytest.raises(TypeError):
            UserAgent(platforms=123)

    def test_platforms_empty_raises_valueerror(self):
        """Empty platforms should raise ValueError."""
        with pytest.raises(ValueError):
            UserAgent(platforms=[])

    def test_min_percentage_invalid_type_raises_typeerror(self):
        """Invalid min_percentage type should raise TypeError."""
        with pytest.raises(TypeError):
            UserAgent(min_percentage="invalid")
        
        with pytest.raises(TypeError):
            UserAgent(min_percentage=[1.0])
        
        with pytest.raises(TypeError):
            UserAgent(min_percentage=True)

    def test_min_version_invalid_type_raises_typeerror(self):
        """Invalid min_version type should raise TypeError."""
        with pytest.raises(TypeError):
            UserAgent(min_version="invalid")
        
        with pytest.raises(TypeError):
            UserAgent(min_version=[1.0])
        
        with pytest.raises(TypeError):
            UserAgent(min_version=False)

    def test_fallback_invalid_type_raises_typeerror(self):
        """Invalid fallback type should raise TypeError, not AssertionError."""
        with pytest.raises(TypeError):
            UserAgent(fallback=123)
        
        with pytest.raises(TypeError):
            UserAgent(fallback=["string"])
        
        with pytest.raises(TypeError):
            UserAgent(fallback=None)

    def test_safe_attrs_invalid_type_raises_typeerror(self):
        """Invalid safe_attrs type should raise TypeError, not AssertionError."""
        with pytest.raises(TypeError):
            UserAgent(safe_attrs="not_a_collection")
        
        with pytest.raises(TypeError):
            UserAgent(safe_attrs=123)

    def test_safe_attrs_invalid_contents_raises_typeerror(self):
        """safe_attrs containing non-strings should raise TypeError."""
        with pytest.raises(TypeError):
            UserAgent(safe_attrs=[123])
        
        with pytest.raises(TypeError):
            UserAgent(safe_attrs=[None])

    def test_no_assertion_errors_raised(self):
        """Verify that AssertionError is never raised for common invalid inputs."""
        invalid_inputs = [
            {"browsers": 123},
            {"os": 456},
            {"platforms": 789},
            {"min_percentage": "bad"},
            {"min_version": "bad"},
            {"fallback": 999},
            {"safe_attrs": "bad"},
        ]
        
        for kwargs in invalid_inputs:
            try:
                UserAgent(**kwargs)
                self.fail(f"Expected exception for {kwargs}")
            except AssertionError:
                self.fail(f"AssertionError raised for {kwargs}, should be TypeError/ValueError")
            except (TypeError, ValueError):
                pass  # Expected


class TestOSReplacement(unittest.TestCase):
    """Tests that OS replacement logic still works correctly after refactoring."""

    def test_windows_expanded(self):
        """'windows' should be expanded to ['win10', 'win7']."""
        ua = FakeUserAgent(os="windows")
        self.assertIn("win10", ua.os)
        self.assertIn("win7", ua.os)
        self.assertNotIn("windows", ua.os)

    def test_windows_in_list_expanded(self):
        """'windows' in a list should be expanded."""
        ua = FakeUserAgent(os=["windows", "linux"])
        self.assertIn("win10", ua.os)
        self.assertIn("win7", ua.os)
        self.assertIn("linux", ua.os)
        self.assertNotIn("windows", ua.os)

    def test_non_replaced_os_unchanged(self):
        """OS values not in replacements should remain unchanged."""
        ua = FakeUserAgent(os=["linux", "macos"])
        self.assertEqual(ua.os, ["linux", "macos"])


if __name__ == "__main__":
    unittest.main()
