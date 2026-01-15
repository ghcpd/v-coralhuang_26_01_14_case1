import json
import sys
import warnings
from typing import TypedDict, Union

# Built-in error class
class FakeUserAgentError(Exception):
    pass

# Built-in logger
class SimpleLogger:
    def warning(self, msg, *args, **kwargs):
        warnings.warn(msg, stacklevel=2)

logger = SimpleLogger()

str_types = (str,)


class BrowserUserAgentData(TypedDict):
    useragent: str
    """The user agent string."""
    percent: float
    """Sampling probability for this user agent when random sampling. Currently has no effect."""
    type: str
    """The device type for this user agent."""
    system: str
    """System name for the user agent."""
    browser: str
    """Browser name for the user agent."""
    version: float
    """Version of the browser."""
    os: str
    """OS name for the user agent."""


# Load all lines from browser.json file
# Returns array of objects
def load() -> list[BrowserUserAgentData]:
    """Load sample user agent data (embedded for standalone use)"""
    return [
        {"useragent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "percent": 15.5, "type": "pc", "system": "Chrome 120.0 Win10", "browser": "chrome", "version": 120.0, "os": "win10"},
        {"useragent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0", "percent": 8.2, "type": "pc", "system": "Firefox 121.0 Win10", "browser": "firefox", "version": 121.0, "os": "win10"},
        {"useragent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0", "percent": 5.3, "type": "pc", "system": "Edge 120.0 Win10", "browser": "edge", "version": 120.0, "os": "win10"},
        {"useragent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "percent": 12.1, "type": "pc", "system": "Chrome 120.0 MacOS", "browser": "chrome", "version": 120.0, "os": "macos"},
        {"useragent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15", "percent": 6.7, "type": "pc", "system": "Safari 17.1 MacOS", "browser": "safari", "version": 17.1, "os": "macos"},
        {"useragent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "percent": 3.8, "type": "pc", "system": "Chrome 120.0 Linux", "browser": "chrome", "version": 120.0, "os": "linux"},
        {"useragent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0", "percent": 2.1, "type": "pc", "system": "Firefox 121.0 Linux", "browser": "firefox", "version": 121.0, "os": "linux"},
        {"useragent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.43 Mobile Safari/537.36", "percent": 18.4, "type": "mobile", "system": "Chrome 120.0 Android", "browser": "chrome", "version": 120.0, "os": "android"},
        {"useragent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1", "percent": 9.3, "type": "mobile", "system": "Safari 17.1 iOS", "browser": "safari", "version": 17.1, "os": "ios"},
        {"useragent": "Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1", "percent": 4.2, "type": "tablet", "system": "Safari 17.1 iOS", "browser": "safari", "version": 17.1, "os": "ios"},
    ]
