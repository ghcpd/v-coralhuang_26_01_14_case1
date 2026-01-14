# Compatibility shim: re-export `src.errors` at the top level
from src.errors import *
__all__ = getattr(__import__("src.errors", fromlist=['*']), '__all__', [])