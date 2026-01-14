import random

from . import settings
from .errors import FakeUserAgentError
from .log import logger
from .utils import load, str_types


class FakeUserAgent:
    def __init__(
        self,
        browsers=["chrome", "edge", "firefox", "safari"],
        os=["windows", "macos", "linux", "android", "ios"],
        min_percentage=0.0,
        min_version=0.0,
        platforms=["pc", "mobile", "tablet"],
        fallback="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        safe_attrs=tuple(),
    ):
        # Check inputs
        assert isinstance(browsers, (list, str)), "browsers must be list or string"
        if isinstance(browsers, str):
            browsers = [browsers]
        self.browsers = browsers

        assert isinstance(os, (list, str)), "OS must be list or string"
        if isinstance(os, str):
            os = [os]
        # OS replacement (windows -> [win10, win7])
        self.os = []
        for os_name in os:
            if os_name in settings.OS_REPLACEMENTS:
                self.os.extend(settings.OS_REPLACEMENTS[os_name])
            else:
                self.os.append(os_name)

        assert isinstance(
            min_percentage, float
        ), "Minimum usage percentage must be float"
        self.min_percentage = min_percentage

        # minimum browser version filter
        assert isinstance(min_version, (int, float)), "min_version must be int or float"
        self.min_version = float(min_version)

        # platforms filter (pc/mobile/tablet)
        assert isinstance(platforms, (list, str)), "platforms must be list or string"
        if isinstance(platforms, str):
            platforms = [platforms]
        platforms = [p.lower() for p in platforms]
        allowed = {"pc", "mobile", "tablet"}
        assert all(p in allowed for p in platforms), "platforms must contain only: pc, mobile, tablet"
        self.platforms = set(platforms)

        assert isinstance(fallback, str), "fallback must be string"
        self.fallback = fallback

        assert isinstance(
            safe_attrs, (list, set, tuple)
        ), "safe_attrs must be list\\tuple\\set of strings or unicode"

        if safe_attrs:
            str_types_safe_attrs = [isinstance(attr, str_types) for attr in safe_attrs]

            assert all(
                str_types_safe_attrs
            ), "safe_attrs must be list\\tuple\\set of strings or unicode"
        self.safe_attrs = set(safe_attrs)

        # Next, load our local data file into memory (browsers.json)
        self.data_browsers = load()

    def _filter_browsers(self, request):
        """Return a list of browser records filtered by request, OS, percent,
        platform and minimum version.
        """
        # Preserve original for error messages
        original = request

        # Normalize request value
        for value, replacement in settings.REPLACEMENTS.items():
            request = request.replace(value, replacement)
        request = request.lower()
        request = settings.SHORTCUTS.get(request, request)

        if request == "random":
            predicate = (
                lambda x: x["browser"] in self.browsers
                and x["os"] in self.os
                and x["percent"] >= self.min_percentage
                and x.get("type") in self.platforms
                and float(x.get("version", 0.0)) >= self.min_version
            )
        else:
            predicate = (
                lambda x: x["browser"] == request
                and x["os"] in self.os
                and x["percent"] >= self.min_percentage
                and x.get("type") in self.platforms
                and float(x.get("version", 0.0)) >= self.min_version
            )

        return list(filter(predicate, self.data_browsers)), original


    # This method will return an object
    # Usage: ua.getBrowser('firefox')
    def getBrowser(self, request):
        try:
            filtered_browsers, original = self._filter_browsers(request)

            # Pick a random browser user-agent from the filtered browsers
            # And return the full dict
            return random.choice(filtered_browsers)  # noqa: S311
        except (KeyError, IndexError):
            if self.fallback is None:
                raise FakeUserAgentError(
                    f"Error occurred during getting browser: {original}"
                )  # noqa
            else:
                logger.warning(
                    f"Error occurred during getting browser: {original}, "
                    "but was suppressed with fallback.",
                )
                # Return fallback object
                return {
                    "useragent": self.fallback,
                    "system": "Chrome 114.0 Win10",
                    "browser": "chrome",
                    "version": 114.0,
                    "os": "win10",
                }

    # This method will use the method below, returning a string
    # Usage: ua['random']
    def __getitem__(self, attr):
        return self.__getattr__(attr)

    # This method will returns a string
    # Usage: ua.random
    def __getattr__(self, attr):
        if attr in self.safe_attrs:
            return super(UserAgent, self).__getattr__(attr)

        try:
            # Handle input value
            for value, replacement in settings.REPLACEMENTS.items():
                attr = attr.replace(value, replacement)
            attr = attr.lower()
            attr = settings.SHORTCUTS.get(attr, attr)

            filtered_browsers, original = self._filter_browsers(attr)

            # Pick a random browser user-agent from the filtered browsers
            # And return the useragent string.
            return random.choice(filtered_browsers).get("useragent")  # noqa: S311
        except (KeyError, IndexError):
            if self.fallback is None:
                raise FakeUserAgentError(
                    f"Error occurred during getting browser: {original}"
                )  # noqa
            else:
                logger.warning(
                    f"Error occurred during getting browser: {original}, "
                    "but was suppressed with fallback.",
                )

                return self.fallback

    @property
    def chrome(self):
        return self.__getattr__("chrome")

    @property
    def googlechrome(self):
        return self.chrome

    @property
    def edge(self):
        return self.__getattr__("edge")

    @property
    def firefox(self):
        return self.__getattr__("firefox")

    @property
    def ff(self):
        return self.firefox

    @property
    def safari(self):
        return self.__getattr__("safari")

    @property
    def random(self):
        return self.__getattr__("random")

    # The following 'get' methods return an object rather than only the UA string
    @property
    def getFirefox(self):
        return self.getBrowser("firefox")

    @property
    def getChrome(self):
        return self.getBrowser("chrome")

    @property
    def getEdge(self):
        return self.getBrowser("edge")

    @property
    def getSafari(self):
        return self.getBrowser("safari")

    @property
    def getRandom(self):
        return self.getBrowser("random")


# common alias
UserAgent = FakeUserAgent
