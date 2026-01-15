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


# Default values for mutable parameters (defined as constants to avoid mutable default args)
_DEFAULT_BROWSERS = ["chrome", "edge", "firefox", "safari"]
_DEFAULT_OS = ["windows", "macos", "linux", "android", "ios"]
_DEFAULT_PLATFORMS = ["pc", "mobile", "tablet"]


def _ensure_iterable(value: Optional[Union[str, Iterable[str]]], *, name: str, default: list[str]) -> list[str]:
    """
    Convert None, str, or Iterable[str] to a new list[str].
    
    Args:
        value: The input value to convert (None, str, or Iterable[str])
        name: Parameter name for error messages
        default: Default list to use when value is None
        
    Returns:
        A new list[str] containing the values
        
    Raises:
        TypeError: If value is not None, str, or Iterable[str], or contains non-strings
        ValueError: If the resulting list would be empty
    """
    if value is None:
        return list(default)  # Return a copy of default
    
    if isinstance(value, str):
        if not value:
            raise ValueError(f"{name} cannot be an empty string")
        return [value]
    
    if isinstance(value, Iterable):
        result = []
        for item in value:
            if not isinstance(item, str):
                raise TypeError(f"{name} must contain only strings, got {type(item).__name__}")
            result.append(item)
        if not result:
            raise ValueError(f"{name} cannot be empty")
        return result
    
    raise TypeError(f"{name} must be a string or iterable of strings, got {type(value).__name__}")


def _ensure_float(value: Union[int, float], *, name: str) -> float:
    """
    Convert int or float to float.
    
    Args:
        value: The input value to convert (int or float)
        name: Parameter name for error messages
        
    Returns:
        The value as a float
        
    Raises:
        TypeError: If value is not int or float
    """
    if isinstance(value, bool):  # bool is subclass of int, so check first
        raise TypeError(f"{name} must be a float or int, got bool")
    if isinstance(value, (int, float)):
        return float(value)
    raise TypeError(f"{name} must be a float or int, got {type(value).__name__}")


class FakeUserAgent:
    def __init__(  # noqa: PLR0913
        self,
        browsers: Optional[Union[Iterable[str], str]] = None,
        os: Optional[Union[Iterable[str], str]] = None,
        min_version: float = 0.0,
        min_percentage: float = 0.0,
        platforms: Optional[Union[Iterable[str], str]] = None,
        fallback: str = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
        ),
        safe_attrs: Optional[Union[tuple[str, ...], list[str], set[str]]] = None,
    ):
        # Validate and set browsers (creates a new list)
        self.browsers = _ensure_iterable(browsers, name="browsers", default=_DEFAULT_BROWSERS)

        # Validate and process OS (creates a new list with replacements)
        os_list = _ensure_iterable(os, name="os", default=_DEFAULT_OS)
        # OS replacement (windows -> [win10, win7])
        self.os: list[str] = []
        for os_name in os_list:
            if os_name in settings.OS_REPLACEMENTS:
                self.os.extend(settings.OS_REPLACEMENTS[os_name])
            else:
                self.os.append(os_name)

        # Validate and set min_percentage
        self.min_percentage = _ensure_float(min_percentage, name="min_percentage")

        # Validate and set min_version
        self.min_version = _ensure_float(min_version, name="min_version")

        # Validate and set platforms (creates a new list)
        self.platforms: list[str] = _ensure_iterable(platforms, name="platforms", default=_DEFAULT_PLATFORMS)

        # Validate fallback
        if not isinstance(fallback, str):
            raise TypeError(f"fallback must be a string, got {type(fallback).__name__}")
        self.fallback = fallback

        # Validate and set safe_attrs (creates a new set)
        if safe_attrs is None:
            self.safe_attrs: set[str] = set()
        elif isinstance(safe_attrs, (list, set, tuple)):
            for attr in safe_attrs:
                if not isinstance(attr, str_types):
                    raise TypeError("safe_attrs must be list/tuple/set of strings")
            self.safe_attrs: set[str] = set(safe_attrs)
        else:
            raise TypeError("safe_attrs must be list/tuple/set of strings")

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
