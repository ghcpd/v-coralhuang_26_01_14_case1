# FakeUserAgent - Mutable Default Parameter Fix

## The Problem: Mutable Default Arguments in Python

Python evaluates default argument values **only once** at function definition time, not each time the function is called. This creates a subtle but dangerous bug when mutable objects (lists, dicts, sets) are used as default values.

### Example of the Anti-pattern

```python
# ❌ DANGEROUS: Mutable default argument
def __init__(self, browsers=["chrome", "firefox"]):
    self.browsers = browsers
```

### Why It's Dangerous

When mutable defaults are used:

1. **All instances share the same list object** in memory
2. **Modifying one instance affects all others** created with the default
3. **State leaks between instances**, causing unpredictable behavior
4. **Bugs are hard to detect** because they only appear after mutation

### Demonstration of the Bug

```python
# With the OLD (buggy) code:
ua1 = FakeUserAgent()
ua1.browsers.append("opera")  # Mutate the default list

ua2 = FakeUserAgent()         # Create new instance
print(ua2.browsers)           # ['chrome', 'edge', 'firefox', 'safari', 'opera'] ❌
                              # "opera" leaked from ua1!
```

## The Solution

### 1. Use `None` as Default + Create Fresh Copies

```python
# ✅ SAFE: Use None as default, create new list inside function
def __init__(self, browsers=None):
    if browsers is None:
        self.browsers = ["chrome", "firefox"]  # Fresh list each time
    else:
        self.browsers = list(browsers)  # Copy provided list
```

### 2. Helper Functions for Consistent Validation

The fix introduces two helper functions:

- **`_ensure_iterable(value, *, name, default)`**: Safely converts `None`, `str`, or `Iterable[str]` to a new `list[str]`
- **`_ensure_float(value, *, name)`**: Validates and converts numeric values to `float`

### 3. Proper Exception Types

The fix replaces `assert` statements with proper exception handling:

- `TypeError` for wrong types
- `ValueError` for invalid values (empty lists, empty strings)

## How the Fix Prevents State Leakage

After the fix:

```python
# With the NEW (fixed) code:
ua1 = FakeUserAgent()
ua1.browsers.append("opera")  # Mutates only ua1's list

ua2 = FakeUserAgent()         # Creates fresh instance with new list
print(ua2.browsers)           # ['chrome', 'edge', 'firefox', 'safari'] ✅
                              # ua2 is independent of ua1!
```

## Running Tests

Execute the test suite to verify the fix:

```bash
# Windows
run_tests.bat

# Unix/Linux/macOS
./run_tests.sh
```

The test suite includes:

- **Mutable default regression tests**: Verify instances don't share state
- **Iterable flexibility tests**: Verify lists, tuples, sets, and generators work
- **Error type tests**: Verify `TypeError`/`ValueError` are raised (not `AssertionError`)
- **OS replacement tests**: Verify existing functionality is preserved

## Key Changes Made

### `fake.py`

1. Changed function signature to use `None` defaults
2. Updated type hints to `Optional[Iterable[str]]`
3. Added `_ensure_iterable()` and `_ensure_float()` helper functions
4. Replaced all `assert` statements with explicit validation
5. Each instance now gets its own fresh copy of list/set attributes

### `test_fake.py`

1. Updated existing tests to expect `TypeError` instead of `AssertionError`
2. Added `TestMutableDefaultRegression` class with 5 regression tests
3. Added `TestIterableFlexibility` class with 16 iterable tests
4. Added `TestErrorTypeCorrectness` class with 13 error type tests
5. Added `TestOSReplacement` class with 3 OS logic tests

## References

- [Python Documentation: Default Argument Values](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values)
- [Common Python Gotchas - Mutable Default Arguments](https://docs.python-guide.org/writing/gotchas/#mutable-default-arguments)
