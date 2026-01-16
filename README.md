# fake-useragent Library - Enhanced Version

## Overview

The fake-useragent library provides a simple way to get random User-Agent strings from a built-in list. This enhanced version adds two powerful new filtering features:

1. **Platform Filtering** - Get user agents for specific device types (PC, mobile, tablet)
2. **Minimum Version Filtering** - Get user agents from specific browser versions or higher

These features are particularly useful for:
- **Web scraping** - Specify platform types to avoid redirects
- **Feature compatibility** - Filter by browser version to ensure feature support
- **Testing** - Simulate specific device types and browser versions

## New Features

### Feature 1: Platform Filtering (`platforms` parameter)

Filter user agents by device platform type.

**Parameters:**
- `platforms` (string or list): Device platform types to include
  - `"pc"` or `"desktop"` - Desktop/laptop computers (Windows, macOS, Linux)
  - `"mobile"` - Mobile devices (smartphones, Android, iOS)
  - `"tablet"` - Tablet devices
  - Default: `None` (includes all platforms: pc, mobile, tablet)

**Supported Input Formats:**
- Single string: `platforms="mobile"`
- List: `platforms=["pc", "mobile"]`
- Case-insensitive: `platforms="PC"` works the same as `platforms="pc"`

### Feature 2: Minimum Version Filtering (`min_version` parameter)

Filter user agents by minimum browser version.

**Parameters:**
- `min_version` (int or float): Minimum browser version (uses >= comparison)
  - Examples: `120`, `120.5`, `121.0`
  - Default: `0.0` (no version filtering)

**Supported Input Formats:**
- Integer: `min_version=120`
- Float: `min_version=120.5`

## Usage Examples

### Basic Usage (Backward Compatible)

```python
from fake import UserAgent

# Default behavior - unchanged
ua = UserAgent()
print(ua.random)  # Random user agent from all platforms and versions
print(ua.chrome)  # Random Chrome user agent
```

### Example 1: Mobile User Agents Only

Get user agents from mobile devices only (useful for mobile web scraping):

```python
from fake import UserAgent

# Get mobile user agents only
ua = UserAgent(platforms="mobile")
print(ua.random)  # Random mobile user agent

# Specify specific browser for mobile
ua = UserAgent(platforms="mobile", browsers="chrome")
print(ua.chrome)  # Random mobile Chrome user agent
```

### Example 2: PC/Desktop User Agents Only

Get user agents from desktop computers only:

```python
from fake import UserAgent

# Get desktop user agents only
ua = UserAgent(platforms="pc")
print(ua.random)  # Random desktop user agent
print(ua.safari)  # Random desktop Safari user agent

# Using dictionary-style access
print(ua["firefox"])  # Random desktop Firefox user agent
```

### Example 3: Browser Version Filtering

Get user agents from specific browser versions or higher:

```python
from fake import UserAgent

# Get Chrome 120 or higher
ua = UserAgent(min_version=120, browsers="chrome")
print(ua.random)  # Chrome 120+

# Get Firefox 121 or higher with specific version format
ua = UserAgent(min_version=121.0)
print(ua.firefox)  # Firefox 121.0+
```

### Example 4: Combined Filtering

Combine multiple filters for precise control:

```python
from fake import UserAgent

# Get mobile Chrome user agents version 120 or higher
ua = UserAgent(
    platforms="mobile",
    browsers="chrome",
    min_version=120,
)
print(ua.random)

# Get PC Edge user agents with high usage percentage
ua = UserAgent(
    platforms="pc",
    browsers="edge",
    min_version=120,
    min_percentage=80.0,
)
print(ua.random)
```

### Example 5: Multiple Platforms

Get user agents from multiple specific platforms:

```python
from fake import UserAgent

# Get PC or mobile user agents (exclude tablets)
ua = UserAgent(platforms=["pc", "mobile"])
print(ua.random)  # Either PC or mobile user agent

# Using string (single platform)
ua = UserAgent(platforms="pc")
print(ua.random)  # Desktop user agent only
```

### Example 6: Web Scraping Scenario

Avoid platform-specific redirects:

```python
from fake import UserAgent
import requests

# Scraper that needs desktop user agents
ua = UserAgent(platforms="pc")
headers = {
    "User-Agent": ua.random,
}

response = requests.get("https://example.com", headers=headers)
# Server sees request from desktop, no redirect to mobile version
```

## API Reference

### FakeUserAgent Constructor

```python
FakeUserAgent(
    browsers=["chrome", "edge", "firefox", "safari"],
    os=["windows", "macos", "linux"],
    min_percentage=0.0,
    fallback="Mozilla/5.0...",
    safe_attrs=tuple(),
    platforms=None,           # NEW PARAMETER
    min_version=0.0,          # NEW PARAMETER
)
```

**New Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `platforms` | str or list | `None` | Device platform types to include (`"pc"`, `"mobile"`, `"tablet"`) |
| `min_version` | int or float | `0.0` | Minimum browser version (uses `>=` comparison) |

**Existing Parameters (Unchanged):**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `browsers` | str or list | `["chrome", "edge", "firefox", "safari"]` | Browser types to include |
| `os` | str or list | `["windows", "macos", "linux"]` | Operating systems to include |
| `min_percentage` | float | `0.0` | Minimum usage percentage |
| `fallback` | str | `Mozilla/5.0...` | Fallback user agent if filtering returns no results |
| `safe_attrs` | tuple | `tuple()` | Attributes to pass through without processing |

### Methods

All existing methods continue to work:

- `ua.random` - Random user agent string
- `ua.chrome` - Random Chrome user agent string
- `ua.firefox` - Random Firefox user agent string
- `ua.edge` - Random Edge user agent string
- `ua.safari` - Random Safari user agent string
- `ua.getBrowser(name)` - Get full browser object (dict)
- `ua.getChrome` - Get Chrome browser object
- `ua.getFirefox` - Get Firefox browser object
- `ua.getEdge` - Get Edge browser object
- `ua.getSafari` - Get Safari browser object
- `ua.getRandom` - Get random browser object

## Data Structure

Each user agent entry contains:

```json
{
    "useragent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "percent": 100.0,
    "type": "pc",
    "system": "Chrome 121.0 Windows",
    "browser": "chrome",
    "version": 121.0,
    "os": "win10"
}
```

- `type` - Device platform: `"pc"`, `"mobile"`, or `"tablet"`
- `version` - Browser version number (used for `min_version` filtering)
- Other fields continue to function as before

## Backward Compatibility

All new parameters are **optional** and have sensible defaults:

- `platforms=None` defaults to all platforms (`["pc", "mobile", "tablet"]`)
- `min_version=0.0` defaults to no version filtering

This means **existing code continues to work without any changes**:

```python
from fake import UserAgent

# This still works exactly as before
ua = UserAgent()
ua = UserAgent(browsers="chrome", os="windows")
ua = UserAgent(min_percentage=50.0)

# New features are opt-in
ua = UserAgent(platforms="mobile")  # New feature
ua = UserAgent(min_version=120)     # New feature
```

## Implementation Notes

### Code Quality

- **Eliminated code duplication** - Refactored filtering logic into `_apply_filters()` helper method
- **Consistent styling** - Follows existing code patterns and conventions
- **Type validation** - Parameters are validated with appropriate error messages
- **Case insensitivity** - Platform names can be any case

### Performance

- Filtering is performed on the entire dataset each time a user agent is requested
- For better performance with repeated requests, consider caching:

```python
from fake import UserAgent

ua = UserAgent(platforms="mobile")
mobile_ua = ua.random  # Cached result
# Reuse mobile_ua multiple times instead of calling ua.random repeatedly
```

### Empty Result Sets

If filtering results in no matching user agents:
- If `fallback` is set (default), returns the fallback user agent
- If `fallback=None`, raises `FakeUserAgentError`

Example:

```python
# If no tablets in dataset, returns fallback
ua = UserAgent(platforms="tablet")
print(ua.random)  # Returns fallback user agent with warning

# Raises error if fallback disabled
ua = UserAgent(platforms="tablet", fallback=None)
ua.random  # Raises FakeUserAgentError
```

## Testing

Run the test suite to verify all functionality:

### Windows
```bash
run_tests.bat
```

### Linux/macOS
```bash
bash run_tests.sh
```

Or manually:
```bash
python -m pytest src/test_fake.py -v
```

## Notes and Caveats

1. **Platform Type Availability** - Not all browsers have entries for all platform types
   - Desktop browsers have "pc" type
   - Mobile browsers have "mobile" type
   - Tablets are less common in the dataset

2. **Version Accuracy** - Browser versions are extracted from user agent strings
   - May not be 100% accurate
   - Use `min_version` as an approximate filter

3. **OS and Platform Independence** - Platform filtering is independent of OS filtering
   - You can have mobile devices on Android or iOS
   - OS is handled separately from platform type

4. **Fallback Behavior** - The fallback user agent always has:
   - `type: "pc"`
   - `version: 114.0`
   - These are hardcoded in the fallback

5. **Case Sensitivity**:
   - Browser names are case-insensitive (handled internally)
   - Platform names are case-insensitive (converted to lowercase)
   - OS names are case-insensitive (handled internally)

## Troubleshooting

**Q: No matching user agents found**
- Check if your filters are too restrictive
- Try with fewer filters or less stringent requirements
- Use default settings to verify data is accessible

**Q: Getting different results each time**
- This is expected! The library picks randomly from matching user agents
- To get consistent results, save the user agent string

**Q: Version filtering doesn't work**
- Verify your `min_version` matches actual versions in data
- Check if the browser/platform combination has data
- Use `getBrowser()` to see the full object including version

**Q: Mobile filtering returns PC user agents**
- The fallback user agent is always a PC user agent
- Disable fallback (`fallback=None`) to get errors instead of fallback
- Check that data actually contains mobile user agents for your browser/OS combo

## Examples with Comments

```python
from fake import UserAgent

# 1. Mobile web scraping
mobile_ua = UserAgent(platforms="mobile")
ua_string = mobile_ua.random
# Use ua_string in requests headers

# 2. Desktop-only scraping
desktop_ua = UserAgent(platforms="pc")
ua_string = desktop_ua.chrome
# Prefer Chrome on desktop

# 3. Modern browser features
modern_ua = UserAgent(min_version=120)
ua_string = modern_ua.random
# Requires browser version 120+

# 4. Specific combination
ua = UserAgent(
    platforms=["pc", "mobile"],     # Desktop or mobile only
    browsers="firefox",              # Firefox only
    min_version=121,                # Version 121+
)
ua_string = ua.random

# 5. With fallback control
ua = UserAgent(
    platforms="tablet",
    fallback=None,  # Raise error instead of falling back
)
try:
    ua_string = ua.random
except Exception as e:
    print(f"No tablet user agents available: {e}")

# 6. Existing code - no changes needed
ua = UserAgent()  # Works as before
ua_string = ua.random
```

## Support

For issues or questions:
1. Check the examples above
2. Review the test cases in `test_fake.py`
3. Verify your filters aren't too restrictive
4. Check the data file structure in `data/browsers.json`
