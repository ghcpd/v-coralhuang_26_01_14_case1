# Fake UserAgent Library

A Python library for generating fake user agent strings with advanced filtering capabilities.

## Features

- Generate random user agent strings from a curated database
- Filter by browser type (Chrome, Edge, Firefox, Safari)
- Filter by operating system (Windows, macOS, Linux, Android, iOS)
- **NEW**: Filter by device platform (PC, mobile, tablet)
- **NEW**: Filter by minimum browser version
- Support for fallback user agents
- Backward compatible API

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from fake import UserAgent

ua = UserAgent()

# Get random user agent
print(ua.random)

# Get specific browser
print(ua.chrome)
print(ua.firefox)
print(ua.edge)
print(ua.safari)

# Get browser data as dictionary
browser_info = ua.getRandom
print(browser_info['useragent'])
print(browser_info['browser'])
print(browser_info['version'])
print(browser_info['os'])
print(browser_info['type'])  # pc, mobile, or tablet
```

### Platform Filtering

Filter user agents by device platform:

```python
# Only mobile devices
ua_mobile = UserAgent(platforms="mobile")
print(ua_mobile.random)

# Mobile and tablet devices
ua_mobile_tablet = UserAgent(platforms=["mobile", "tablet"])
print(ua_mobile_tablet.random)

# Only desktop PCs
ua_pc = UserAgent(platforms="pc")
print(ua_pc.random)
```

### Version Filtering

Filter user agents by minimum browser version:

```python
# Only browsers version 120 or higher
ua_new = UserAgent(min_version=120)
print(ua_new.random)

# Version 120.5 or higher
ua_newer = UserAgent(min_version=120.5)
print(ua_newer.random)
```

### Combined Filtering

Combine multiple filters:

```python
# Chrome browsers on mobile devices, version 120+
ua_combined = UserAgent(
    browsers=["chrome"],
    platforms="mobile",
    min_version=120
)
print(ua_combined.random)
```

### Advanced Configuration

```python
ua = UserAgent(
    browsers=["chrome", "firefox"],  # Only these browsers
    os=["windows", "android"],       # Only these OS
    platforms=["pc", "mobile"],      # Only these platforms
    min_version=115,                 # Minimum version 115
    min_percentage=50.0,             # Minimum usage percentage
    fallback="Custom fallback UA"    # Custom fallback
)
```

## Parameters

### Constructor Parameters

- `browsers` (list or str): Browser types to include. Default: `["chrome", "edge", "firefox", "safari"]`
- `os` (list or str): Operating systems to include. Default: `["windows", "macos", "linux", "android", "ios"]`
- `min_percentage` (float): Minimum usage percentage. Default: `0.0`
- `platforms` (list or str, optional): Device platforms to include. Options: `"pc"`, `"mobile"`, `"tablet"`. Default: `None` (all platforms)
- `min_version` (int or float, optional): Minimum browser version. Default: `0.0`
- `fallback` (str): Fallback user agent string. Default: Chrome 114 UA
- `safe_attrs` (tuple): Safe attributes to access. Default: `tuple()`

## Use Cases

### Mobile Web Scraping
```python
ua = UserAgent(platforms="mobile")
# Get mobile user agents to avoid desktop/mobile redirects
```

### Modern Browser Features
```python
ua = UserAgent(min_version=120)
# Ensure browsers support newer web features
```

### Platform-Specific Testing
```python
ua_pc = UserAgent(platforms="pc")
ua_mobile = UserAgent(platforms="mobile")
ua_tablet = UserAgent(platforms="tablet")
# Test different device types
```

## Notes and Caveats

- The library uses a static database of user agents that may become outdated
- Filtering is applied in combination - all conditions must be met
- If no user agents match the filters, the library falls back to the specified fallback UA
- Platform filtering uses the "type" field from the database ("pc", "mobile", "tablet")
- Version filtering uses >= comparison
- All new parameters are optional and maintain backward compatibility

## Testing

Run the test suite:

```bash
python -m pytest test_fake.py
```

Or use the provided script:

```bash
# Windows
run_tests.bat

# Linux/Mac
./run_tests.sh
```

## License

This project is open source. See LICENSE file for details.