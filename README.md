# fake-useragent — platform & version filtering

This fork adds two optional filtering features to `FakeUserAgent` while preserving the original API:

- `platforms` — restrict returned UAs to `pc`, `mobile` and/or `tablet` types
- `min_version` — require a minimum browser version (numeric, `>=` comparison)

Quick examples

- Only mobile user-agents (string or list accepted):

```py
from fake import UserAgent
ua = UserAgent(platforms="mobile")
print(ua.getRandom)            # dict for a mobile UA
print(ua.chrome)               # string UA from 'chrome' matching platform
```

- Minimum browser version (int or float accepted):

```py
ua = UserAgent(min_version=122)
print(ua.getRandom.get("version"))  # >= 122.0
```

- Combine platform + version + browser filters:

```py
ua = UserAgent(platforms=["mobile"], min_version=121)
print(ua.getBrowser("chrome"))
```

Notes and caveats

- `platforms` accepts a `str` or `list` and defaults to all platforms (`pc`, `mobile`, `tablet`).
- `min_version` accepts `int` or `float` and defaults to `0.0` (no filtering).
- Backward compatible: if you don't pass the new parameters, behavior is unchanged.
- Data source is `src/data/browsers.json` (entries include `type` and numeric `version`).

Run tests

- Windows: `run_tests.bat`
- Linux/macOS: `./run_tests.sh`

Requirements

- Python 3.8+
- `pytest` (installed automatically by the run scripts)
