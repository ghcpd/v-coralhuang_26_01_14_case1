# FakeUserAgent

## 🚫 Mutable default parameters: why they bite
- In Python, default argument values are evaluated **once** at function definition time.
- If you use a mutable default (e.g., `list` or `dict`) and mutate it, the change is **shared across all future calls/instances**.
- This can lead to subtle cross-instance leaks (e.g., adding a browser in one `FakeUserAgent` instance shows up in another).

## ✅ What changed in `FakeUserAgent`
- Replaced mutable defaults (`browsers`, `os`, `platforms`, `safe_attrs`) with `None` sentinels.
- Added helper validators:
  - `_ensure_iterable(value, *, name, allow_empty=False) -> list[str]` ensures fresh lists, validates types/content, and raises `TypeError`/`ValueError`.
  - `_ensure_float(value, *, name) -> float` accepts `int`/`float` and raises `TypeError` otherwise.
- Preserved existing behavior:
  - `OS_REPLACEMENTS` expansion (e.g., `"windows"` → `"win10"`, `"win7"`).
  - Browser normalization and fallback handling.
  - Public API compatibility (`UserAgent` alias, attribute access, `getBrowser`, etc.).
- Removed `assert`-based validation to avoid `AssertionError` and rely on explicit exceptions.

## 🧪 Tests added/updated
- Regression test ensuring **no shared mutable defaults** across instances.
- Iterable flexibility: accepts `list`, `tuple`, `set` for relevant parameters.
- Error-type correctness: invalid inputs raise `TypeError`/`ValueError`, **not** `AssertionError`.
- Keeps existing fallback and alias tests intact.

## ▶️ Run tests
Use the convenience scripts (pick one for your platform):

```bash
# POSIX
./run_tests.sh
```

```bat
REM Windows
run_tests.bat
```

Both scripts invoke `python -m pytest -q` and exit with the test status code.
