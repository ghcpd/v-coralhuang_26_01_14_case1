# Compatibility shim: re-export `src.settings` at the top level (explicitly
# expose dunder names required by the test-suite)
from src import settings as _src_settings
# explicit exports used by tests and consumers
__version__ = _src_settings.__version__
REPLACEMENTS = _src_settings.REPLACEMENTS
SHORTCUTS = _src_settings.SHORTCUTS
OS_REPLACEMENTS = _src_settings.OS_REPLACEMENTS

__all__ = ["__version__", "REPLACEMENTS", "SHORTCUTS", "OS_REPLACEMENTS"]