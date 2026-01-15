import random
import warnings
from collections.abc import Iterable
from typing import Any, Optional, Union

from utils import BrowserUserAgentData, load, str_types

_DEFAULT_BROWSERS = ("chrome", "edge", "firefox", "safari")
_DEFAULT_OS = ("windows", "macos", "linux", "android", "ios")
_DEFAULT_PLATFORMS = ("pc", "mobile", "tablet")

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


def _ensure_iterable(value, *, name: str) -> list[str]:
    """Validate and materialize iterable input into a fresh list of strings."""

    if value is None:
        return []

    if isinstance(value, str):
        candidate = [value]
    else:
        if not isinstance(value, Iterable):
            raise TypeError(f"{name} must be an iterable of strings or a string")
        candidate = list(value)

    if not candidate:
        raise ValueError(f"{name} cannot be empty")

    if not all(isinstance(item, str) for item in candidate):
        raise ValueError(f"{name} must contain only strings")

    return candidate


def _ensure_float(value, *, name: str) -> float:
    """Convert numeric inputs to float while validating type."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a float or int")

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
        safe_attrs: Optional[Iterable[str]] = None,
    ):
        browsers_list = _ensure_iterable(
            browsers if browsers is not None else _DEFAULT_BROWSERS,
            name="browsers",
        )
        self.browsers = browsers_list

        os_list = _ensure_iterable(os if os is not None else _DEFAULT_OS, name="os")
        # OS replacement (windows -> [win10, win7])
        self.os: list[str] = []
        for os_name in os_list:
            if os_name in settings.OS_REPLACEMENTS:
                self.os.extend(settings.OS_REPLACEMENTS[os_name])
            else:
                self.os.append(os_name)

        self.min_percentage = _ensure_float(min_percentage, name="min_percentage")
        self.min_version = _ensure_float(min_version, name="min_version")

        platforms_list = _ensure_iterable(
            platforms if platforms is not None else _DEFAULT_PLATFORMS,
            name="platforms",
        )
        self.platforms: list[str] = platforms_list

        if not isinstance(fallback, str):
            raise TypeError("fallback must be string")
        self.fallback = fallback

        safe_attrs_value = () if safe_attrs is None else safe_attrs
        if not isinstance(safe_attrs_value, (list, set, tuple)):
            raise TypeError("safe_attrs must be list\\tuple\\set of strings or unicode")

        if safe_attrs_value:
            str_types_safe_attrs = [isinstance(attr, str_types) for attr in safe_attrs_value]

            if not all(str_types_safe_attrs):
                raise ValueError("safe_attrs must be list\\tuple\\set of strings or unicode")
        self.safe_attrs: set[str] = set(safe_attrs_value)

        # Next, load our local data file into memory (browsers.json)
        self.data_browsers = load()

    # This method will return a filtered list of user agents.
    # The request parameter can be used to specify a browser.
    def _filter_useragents(self, request: Optional[str] = None) -> list[BrowserUserAgentData]:
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
