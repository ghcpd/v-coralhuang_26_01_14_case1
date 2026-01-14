# fake-useragent (mini)

This small clone adds two new filtering options to the FakeUserAgent class: platform filtering and minimum browser version filtering.

## Features ✅

- Filter returned user-agents by device platform: `pc`, `mobile`, `tablet`.
- Require a minimum browser version (integer or float) using `min_version` (comparison: `>=`).
- Backwards-compatible: both options are optional and the library behaves as before when they are not provided.

## New constructor parameters

- `min_version` (int|float, default: `0.0`)
  - Only user-agent records with `version >= min_version` are returned.

- `platforms` (str|list, default: `["pc", "mobile", "tablet"]`)
  - Select which device types to allow. Valid values: `pc`, `mobile`, `tablet`.

Notes:
- The `os` default was extended to include `android` and `ios` so mobile entries are available by default.
- Input types are validated; invalid values raise AssertionError (keeps existing error style).

## Usage examples 💡

1. Get only mobile UAs (any browser):

```python
from fake import UserAgent
ua = UserAgent(platforms="mobile")
print(ua.getRandom)
```

2. Require Chrome 122+ and only tablet UAs:

```python
ua = UserAgent(browsers="chrome", platforms="tablet", min_version=122)
print(ua.getBrowser("chrome"))
```

3. Pass a list for platforms and an integer for min_version:

```python
ua = UserAgent(platforms=["mobile"], min_version=122)
print(ua.getBrowser("chrome"))
```

## Tests and quick verification 🔧

- Requirements: `pytest` (provided in `requirements.txt`).
- Run tests on Windows with `run_tests.bat` or on macOS/Linux with `run_tests.sh`.

---

If you want additional filters or a different comparison rule for versions, I can add that in a follow-up.