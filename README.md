fake-useragent — platform & min-version filters

Overview

This fork extends the existing fake-useragent implementation with two optional filters so callers can request UAs by device platform and/or minimum browser version.

New features

- platforms: limit results to device types — `"pc"`, `"mobile"`, `"tablet"` (accepts string or list/tuple). Default: all three.
- min_version: require browser `version >= min_version` (accepts int or float). Default: `0.0` (no filtering).

Design notes

- Backwards compatible: all new parameters are optional and validated; existing calls behave the same.
- Uses existing data fields in `data/browsers.json` (`type` and numeric `version`).
- Empty-result behavior unchanged (falls back to `fallback` UA or raises if `fallback` is None).

Usage examples

1) Get only mobile user-agents

```python
from fake import UserAgent
ua = UserAgent(platforms="mobile")
print(ua.getRandom["type"])  # -> "mobile"
print(ua.chrome)              # returns a chrome UA but only from mobile entries
```

2) Require a minimum browser version (Chrome 122+)

```python
ua = UserAgent(browsers="chrome", min_version=122)
print(ua.getBrowser("chrome")["version"])  # >= 122.0
```

3) Combined: tablet Chrome >= 122 (useful to avoid mobile/desktop redirects)

```python
ua = UserAgent(browsers=["chrome"], platforms=["tablet"], min_version=122.0)
print(ua.getRandom)
```

Caveats

- `platforms` only accepts the tokens `pc`, `mobile`, `tablet`.
- `min_version` is numeric and compared with `>=` against the data file's `version` field.

Running tests (one-click)

- Windows: run `run_tests.bat`
- Linux/macOS: run `./run_tests.sh`

Credits

This change set implements platform and minimum-version filtering while keeping the original API and fallback semantics.