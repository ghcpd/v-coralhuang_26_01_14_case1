import random
import warnings
from collections.abc import Iterable
from typing import Any, Optional, Union

from utils import BrowserUserAgentData, load, str_types

# Built-in settings
class Settings:
    OS_REPLACEMENTS = {"windows": ["win10", "win7"]}
    REPLACEMENTS = {"googlechrome": "chrome", "chromium": "chrome", "ff": "firefox"}
    SHORTCUTS = {"google": "chrome", "ie": "edge"}

settings = Settings()

# Built-in logger
class SimpleLogger:
    def warning(self, msg, *args, **kwargs):
        warnings.warn(msg, stacklevel=2)

logger = SimpleLogger()


def _ensure_iterable(value: Optional[Union[str, Iterable[str]]], *, name: str) -> list[str]:
    """
    Convert input to a list of strings, handling None, str, and iterables.
    
    Args:
        value: The input value to convert (None, str, or Iterable[str])
        name: The parameter name for error messages
    
    Returns:
        A new list of strings
    
    Raises:
        TypeError: If value is not None, str, or an iterable
        ValueError: If the iterable is empty or contains non-string values
    """
    if value is None:
        return []
    
    if isinstance(value, str):
        return [value]
    
    # Check if it's iterable (but not a string, which we already handled)
    try:
        # Convert to list to create a new mutable copy
        result = list(value)
    except TypeError:
        raise TypeError(f"{name} must be None, str, or an iterable of strings")
    
    # Validate all elements are strings
    if not all(isinstance(item, str) for item in result):
        raise ValueError(f"{name} must contain only string values")
    
    return result


def _ensure_float(value: Union[int, float], *, name: str) -> float:
    """
    Convert input to float, accepting int or float.
    
    Args:
        value: The input value to convert (int or float)
        name: The parameter name for error messages
    
    Returns:
        The value as a float
    
    Raises:
        TypeError: If value is not int or float
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be int or float")
    
    return float(value)


class FakeUserAgent:
    def __init__(  # noqa: PLR0913
        self,
        browsers: Optional[Iterable[str]] = None,
        os: Optional[Iterable[str]] = None,
        min_version: float = 0.0,
        min_percentage: float = 0.0,
        platforms: Optional[Iterable[str]] = None,
        fallback: str = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
        ),
        safe_attrs: Union[tuple[str], list[str], set[str]] = tuple(),
    ):
        # Validate and convert browsers parameter
        if browsers is None:
            self.browsers = ["chrome", "edge", "firefox", "safari"]
        else:
            self.browsers = _ensure_iterable(browsers, name="browsers")
            if not self.browsers:
                raise ValueError("browsers cannot be empty")

        # Validate and convert os parameter
        if os is None:
            os_list = ["windows", "macos", "linux", "android", "ios"]
        else:
            os_list = _ensure_iterable(os, name="os")
            if not os_list:
                raise ValueError("os cannot be empty")
        
        # OS replacement (windows -> [win10, win7])
        self.os: list[str] = []
        for os_name in os_list:
            if os_name in settings.OS_REPLACEMENTS:
                self.os.extend(settings.OS_REPLACEMENTS[os_name])
            else:
                self.os.append(os_name)

        # Validate and convert min_percentage
        self.min_percentage = _ensure_float(min_percentage, name="min_percentage")

        # Validate and convert min_version
        self.min_version = _ensure_float(min_version, name="min_version")

        # Validate and convert platforms parameter
        if platforms is None:
            self.platforms = ["pc", "mobile", "tablet"]
        else:
            self.platforms = _ensure_iterable(platforms, name="platforms")
            if not self.platforms:
                raise ValueError("platforms cannot be empty")

        # Validate fallback
        if not isinstance(fallback, str):
            raise TypeError("fallback must be string")
        self.fallback = fallback

        # Validate safe_attrs
        if not isinstance(safe_attrs, (list, set, tuple)):
            raise TypeError("safe_attrs must be list, tuple, or set of strings")

        if safe_attrs:
            if not all(isinstance(attr, str_types) for attr in safe_attrs):
                raise ValueError("safe_attrs must contain only strings")
        self.safe_attrs: set[str] = set(safe_attrs)

        # Next, load our local data file into memory (browsers.json)
        self.data_browsers = load()

    # This method will return a filtered list of user agents.
    # The request parameter can be used to specify a browser.
    def _filter_useragents(
        self, request: Union[str, None] = None
    ) -> list[BrowserUserAgentData]:
        # filter based on browser, os, platform and version.
        filtered_useragents = list(
            filter(
                lambda x: x["browser"] in self.browsers
                and x["os"] in self.os
                and x["type"] in self.platforms
                and x["version"] >= self.min_version
                and x["percent"] >= self.min_percentage,
                self.data_browsers,
            )
        )
        # filter based on a specific browser request
        if request:
            filtered_useragents = list(
                filter(lambda x: x["browser"] == request, filtered_useragents)
            )

        return filtered_useragents

    # This method will return an object
    # Usage: ua.getBrowser('firefox')
    def getBrowser(self, request: str) -> BrowserUserAgentData:
        try:
            # Handle request value
            for value, replacement in settings.REPLACEMENTS.items():
                request = request.replace(value, replacement)
            request = request.lower()
            request = settings.SHORTCUTS.get(request, request)

            if request == "random":
                # Filter the browser list based on the browsers array using lambda
                # And based on OS list
                # And percentage is bigger then min percentage
                # And convert the iterator back to a list
                filtered_browsers = self._filter_useragents()
            else:
                # Or when random isn't select, we filter the browsers array based on the 'request' using lamba
                # And based on OS list
                # And percentage is bigger then min percentage
                # And convert the iterator back to a list
                filtered_browsers = self._filter_useragents(request=request)

            # Pick a random browser user-agent from the filtered browsers
            # And return the full dict
            return random.choice(filtered_browsers)  # noqa: S311
        except (KeyError, IndexError):
            logger.warning(
                f"Error occurred during getting browser: {request}, "
                "but was suppressed with fallback.",
            )
            # Return fallback object
            return {
                "useragent": self.fallback,
                "percent": 100.0,
                "type": "pc",
                "system": "Chrome 122.0 Win10",
                "browser": "chrome",
                "version": 122.0,
                "os": "win10",
            }

    # This method will use the method below, returning a string
    # Usage: ua['random']
    def __getitem__(self, attr: str) -> Union[str, Any]:
        return self.__getattr__(attr)

    # This method will returns a string
    # Usage: ua.random
    def __getattr__(self, attr: str) -> Union[str, Any]:
        if attr in self.safe_attrs:
            return super(UserAgent, self).__getattribute__(attr)

        try:
            # Handle input value
            for value, replacement in settings.REPLACEMENTS.items():
                attr = attr.replace(value, replacement)
            attr = attr.lower()
            attr = settings.SHORTCUTS.get(attr, attr)

            if attr == "random":
                # Filter the browser list based on the browsers array using lambda
                # And based on OS list
                # And percentage is bigger then min percentage
                # And convert the iterator back to a list
                filtered_browsers = self._filter_useragents()
            else:
                # Or when random isn't select, we filter the browsers array based on the 'attr' using lamba
                # And based on OS list
                # And percentage is bigger then min percentage
                # And convert the iterator back to a list
                filtered_browsers = self._filter_useragents(request=attr)

            # Pick a random browser user-agent from the filtered browsers
            # And return the useragent string.
            return random.choice(filtered_browsers).get("useragent")  # noqa: S311
        except (KeyError, IndexError):
            logger.warning(
                f"Error occurred during getting browser: {attr}, "
                "but was suppressed with fallback.",
            )
            return self.fallback

    @property
    def chrome(self) -> str:
        return self.__getattr__("chrome")

    @property
    def googlechrome(self) -> str:
        return self.chrome

    @property
    def edge(self) -> str:
        return self.__getattr__("edge")

    @property
    def firefox(self) -> str:
        return self.__getattr__("firefox")

    @property
    def ff(self) -> str:
        return self.firefox

    @property
    def safari(self) -> str:
        return self.__getattr__("safari")

    @property
    def random(self) -> str:
        return self.__getattr__("random")

    # The following 'get' methods return an object rather than only the UA string
    @property
    def getFirefox(self) -> BrowserUserAgentData:
        return self.getBrowser("firefox")

    @property
    def getChrome(self) -> BrowserUserAgentData:
        return self.getBrowser("chrome")

    @property
    def getEdge(self) -> BrowserUserAgentData:
        return self.getBrowser("edge")

    @property
    def getSafari(self) -> BrowserUserAgentData:
        return self.getBrowser("safari")

    @property
    def getRandom(self) -> BrowserUserAgentData:
        return self.getBrowser("random")


# common alias
UserAgent = FakeUserAgent
