# Compatibility shim: re-export `src.log` at the top level
from src.log import *
__all__ = getattr(__import__("src.log", fromlist=['*']), '__all__', [])