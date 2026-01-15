# Fake User Agent

## Mutable default parameter issue
Mutable defaults such as `[]` are evaluated once when a function is defined, so any in-place mutation leaks across future calls. In the old `FakeUserAgent.__init__` this meant adding a browser or OS to one instance polluted every new instance.

## What changed
- Replaced list defaults with `None` plus safe defaults built via helper functions.
- Added `_ensure_iterable` and `_ensure_float` to validate inputs and create fresh lists every time.
- Swapped `assert` checks for explicit `TypeError` / `ValueError` exceptions to avoid silent assertion stripping and to keep error types predictable.

## Why it fixes leakage
Each constructor call now materializes brand-new lists from immutable defaults, so mutations remain instance-local and cannot bleed into later instances.

## Running tests
- Windows: run `run_tests.bat`
- macOS/Linux: run `./run_tests.sh`

Both commands execute `pytest` and will fail if shared mutable defaults or invalid input handling regress.
