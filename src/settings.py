"""Settings for fake-useragent."""

__version__ = "1.0.0"

# Browser name replacements
REPLACEMENTS = {
    " ": "",
    "_": "",
}

# Browser shortcuts
SHORTCUTS = {
    "internet explorer": "edge",
    "ie": "edge",
    "msie": "edge",
    "google": "chrome",
    "googlechrome": "chrome",
    "google chrome": "chrome",
}

# OS replacements
OS_REPLACEMENTS = {
    "windows": ["win10", "win7"],
    "macos": ["macos"],
    "linux": ["linux"],
}
