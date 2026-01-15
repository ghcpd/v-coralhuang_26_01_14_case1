# fake-useragent (mini prime)

## Feature overview ✅
This fork adds two optional filters to the `FakeUserAgent` API so you can request user agents by device platform and/or minimum browser version:

- `platforms`: limit results to `pc`, `mobile`, or `tablet` (supports string or list input). Default: all platforms.
- `min_version`: limit results to entries with `version >= min_version` (supports int or float). Default: `0.0` (no filtering).

Both filters are optional and backwards compatible — if you don't pass them the library behaves as before.

---

## Parameters 🔧
- `platforms`: str or list[str]
  - Accepts: `"pc"`, `"mobile"`, `"tablet"` (case-insensitive).
  - Examples: `platforms='mobile'`, `platforms=['mobile','tablet']`.

- `min_version`: int or float
  - Examples: `min_version=122`, `min_version=121.5`.

Notes:
- Inputs are validated and will raise an `AssertionError` for invalid types/values.
- `os` default list is extended to include common mobile OS values (e.g., `android`, `ios`).

---

## Usage examples 💡
```python
from fake import UserAgent

# 1) Get only mobile device UAs
ua = UserAgent(platforms='mobile')
print(ua.getRandom['useragent'])

# 2) Get Chrome entries with version >= 122
ua = UserAgent(min_version=122)
print(ua.getBrowser('chrome')['version'])

# 3) Combined: edge on mobile devices with version >= 121
ua = UserAgent(platforms=['mobile'], min_version=121)
ent = ua.getBrowser('edge')
print(e['type'], e['version'])
```

---

## Tests & one-click runner 🧪
Requirements are in `requirements.txt` (only `pytest` required).

Run tests on Windows:
```
run_tests.bat
```

Run tests on Linux/macOS:
```
bash run_tests.sh
```

---

## Caveats ⚠️
- Filtering uses fields present in `src/data/browsers.json` (`type` for platform and numeric `version`). Do not modify that JSON format if you want the filters to work.
- When filters produce an empty result set, behavior is unchanged: if `fallback` is configured it will be returned; otherwise the same error is raised.

---

If you want more advanced filtering (e.g., OS per platform, regex versions), we can extend the API with additional options later.