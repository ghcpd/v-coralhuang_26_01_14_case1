"""Standalone fake-useragent module."""

# Make common top-level imports (e.g. `import fake`, `import settings`)
# resolve to their `src.*` equivalents when the package is loaded. This keeps
# backward compatibility for older code and the existing test suite which
# uses bare imports. Create these aliases *before* importing submodules so
# modules that still use absolute imports (legacy code) continue to work.
import importlib
import sys
_aliases = ("fake", "settings", "errors", "log", "utils")
for _m in _aliases:
    sys.modules.setdefault(_m, importlib.import_module(f".{_m}", __package__))

# Now import the public symbols from local modules using relative imports.
from .fake import FakeUserAgent, UserAgent

VERSION = "1.0.0"

__all__ = ["FakeUserAgent", "UserAgent", "VERSION"]
