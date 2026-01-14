# Compatibility shim: expose `src.fake` as top-level `fake` module for
# consumers/tests that import `fake` directly.
from src.fake import *
__all__ = getattr(__import__("src.fake", fromlist=['*']), '__all__', [])