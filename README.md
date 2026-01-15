# Mutable Default Parameter Fix

## Overview

This project demonstrates a fix for the **mutable default parameter anti-pattern** in Python, specifically in the `FakeUserAgent.__init__()` method.

## The Problem: Mutable Default Parameters

In Python, default parameter values are evaluated **once** at function definition time, not each time the function is called. When mutable objects (like lists or dictionaries) are used as default values, they can cause unexpected behavior where state "leaks" between different function calls or instance creations.

### Example of the Problem

```python
# DANGEROUS: Mutable default parameter
class FakeUserAgent:
    def __init__(self, browsers=["chrome", "firefox"]):
        self.browsers = browsers

# Create two instances
ua1 = FakeUserAgent()
ua2 = FakeUserAgent()

# Modify the first instance
ua1.browsers.append("opera")

# BUG: The second instance is also affected!
print(ua2.browsers)  # ['chrome', 'firefox', 'opera']
```

Both `ua1` and `ua2` share the **same list object** because the default list `["chrome", "firefox"]` is created only once when the class is defined, not each time an instance is created.

## Why This Is Dangerous

1. **Silent Bugs**: The bug is subtle and may not be immediately obvious during development
2. **Cross-Instance State Leakage**: Modifying one instance affects others
3. **Hard to Debug**: The cause can be far removed from where the symptoms appear
4. **Violates Principle of Least Surprise**: Users expect instances to be independent
5. **Production Issues**: Can cause intermittent failures that are difficult to reproduce

### Real-World Impact

This anti-pattern can cause:
- Configuration settings from one user affecting another user
- Test isolation failures where one test modifies state used by another
- Race conditions in multi-threaded applications
- Data corruption when instances are reused

## The Solution

Replace mutable default values with `None` and create new objects inside the function:

```python
# CORRECT: Use None as default
class FakeUserAgent:
    def __init__(self, browsers: Optional[Iterable[str]] = None):
        if browsers is None:
            self.browsers = ["chrome", "firefox"]  # New list each time
        else:
            self.browsers = list(browsers)  # Create a copy
```

### Key Changes Made

1. **Function Signature Updates**
   - Changed mutable defaults (`["chrome", ...]`) to `None`
   - Updated type hints from `Union[list[str], str]` to `Optional[Iterable[str]]`
   - Added imports: `from collections.abc import Iterable` and `from typing import Optional`

2. **Helper Functions Added**
   - `_ensure_iterable(value, *, name: str) -> list[str]`
     - Converts `None`, `str`, or `Iterable[str]` to a new `list[str]`
     - Raises `TypeError` for invalid types
     - Raises `ValueError` for invalid contents
   
   - `_ensure_float(value, *, name: str) -> float`
     - Converts `int` or `float` to `float`
     - Raises `TypeError` for invalid types

3. **Validation Refactoring**
   - Removed all `assert` statements
   - Replaced with explicit validation using helper functions
   - Raises `TypeError` or `ValueError` instead of `AssertionError`
   - Preserved all existing logic and behavior

4. **Iterable Flexibility**
   - Parameters now accept `list`, `tuple`, `set`, or any iterable
   - String parameters are converted to single-element lists
   - All iterables are converted to new list copies (preventing shared state)

## Testing

The test suite includes comprehensive tests to prevent regression:

### Mutable Default Tests
- Verifies that modifying one instance doesn't affect others
- Tests `browsers`, `os`, and `platforms` attributes
- Ensures multiple instances can be mutated independently

### Iterable Flexibility Tests
- Validates that `list`, `tuple`, `set`, and `str` inputs work correctly
- Ensures invalid types raise appropriate errors
- Tests empty iterable rejection

### Error Type Tests
- Confirms no `AssertionError` is raised from `__init__`
- Validates `TypeError` for invalid types
- Validates `ValueError` for invalid values

## Running the Tests

### Windows
```cmd
run_tests.bat
```

### Linux/macOS
```bash
./run_tests.sh
```

Or manually:
```bash
pytest test_fake.py -v
```

## Best Practices

To avoid mutable default parameter issues in your own code:

1. **Never use mutable objects as default values**
   ```python
   # BAD
   def func(items=[]):
       pass
   
   # GOOD
   def func(items=None):
       if items is None:
           items = []
   ```

2. **Use `None` as a sentinel value**
   - Check for `None` and create new objects inside the function
   - This ensures each call gets a fresh, independent object

3. **Create copies of mutable inputs**
   - Even when users pass mutable objects, create copies to prevent external modifications
   ```python
   def __init__(self, items=None):
       self.items = list(items) if items is not None else []
   ```

4. **Use proper type hints**
   - `Optional[Iterable[T]]` for parameters that accept iterables or None
   - `Union[T, Iterable[T]]` for parameters that accept both single values and iterables

5. **Add regression tests**
   - Test that instances are truly independent
   - Verify that mutations don't leak between instances

## Summary

This fix eliminates the mutable default parameter anti-pattern by:
- Replacing mutable defaults with `None`
- Creating new objects for each instance
- Adding comprehensive validation
- Improving type hints
- Adding extensive tests to prevent regression

The result is a more robust, predictable, and maintainable codebase that follows Python best practices.
