#!/usr/bin/env python3
"""
Demo script showing the new platform and version filtering features.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fake import UserAgent

def demo_basic():
    print("=== Basic Usage ===")
    ua = UserAgent()
    print(f"Random UA: {ua.random[:80]}...")
    print(f"Chrome UA: {ua.chrome[:80]}...")
    print()

def demo_platform_filtering():
    print("=== Platform Filtering ===")

    # Mobile only
    ua_mobile = UserAgent(platforms="mobile")
    mobile_data = ua_mobile.getRandom
    print(f"Mobile UA: {mobile_data['useragent'][:80]}...")
    print(f"Platform: {mobile_data['type']}, OS: {mobile_data['os']}")
    print()

    # PC only
    ua_pc = UserAgent(platforms="pc")
    pc_data = ua_pc.getRandom
    print(f"PC UA: {pc_data['useragent'][:80]}...")
    print(f"Platform: {pc_data['type']}, OS: {pc_data['os']}")
    print()

def demo_version_filtering():
    print("=== Version Filtering ===")

    # Version 120+
    ua_new = UserAgent(min_version=120)
    new_data = ua_new.getRandom
    print(f"New browser UA: {new_data['useragent'][:80]}...")
    print(f"Version: {new_data['version']}, Browser: {new_data['browser']}")
    print()

def demo_combined_filtering():
    print("=== Combined Filtering ===")

    # Chrome on mobile, version 115+
    ua_combined = UserAgent(
        browsers=["chrome"],
        platforms="mobile",
        min_version=115
    )
    combined_data = ua_combined.getRandom
    print(f"Combined UA: {combined_data['useragent'][:80]}...")
    print(f"Browser: {combined_data['browser']}, Platform: {combined_data['type']}, Version: {combined_data['version']}")
    print()

if __name__ == "__main__":
    demo_basic()
    demo_platform_filtering()
    demo_version_filtering()
    demo_combined_filtering()
    print("Demo completed!")