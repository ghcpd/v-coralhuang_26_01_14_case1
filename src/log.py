"""Logging configuration for fake-useragent."""

import logging

# Create logger
logger = logging.getLogger("fake_useragent")
logger.setLevel(logging.WARNING)

# Create console handler
handler = logging.StreamHandler()
handler.setLevel(logging.WARNING)

# Create formatter
formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)
