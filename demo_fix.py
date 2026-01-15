"""
Demonstration of the mutable default parameter fix.
This script shows that instances are now independent.
"""

from fake import FakeUserAgent

print("=" * 60)
print("Demonstrating Mutable Default Parameter Fix")
print("=" * 60)

# Create first instance
print("\n1. Creating first instance (ua1)...")
ua1 = FakeUserAgent()
print(f"   ua1.browsers: {ua1.browsers}")

# Mutate first instance
print("\n2. Modifying ua1 by appending 'opera' to browsers...")
ua1.browsers.append("opera")
print(f"   ua1.browsers: {ua1.browsers}")

# Create second instance
print("\n3. Creating second instance (ua2)...")
ua2 = FakeUserAgent()
print(f"   ua2.browsers: {ua2.browsers}")

# Verify independence
print("\n4. Verification:")
if "opera" in ua2.browsers:
    print("   ❌ FAIL: ua2 was affected by ua1's mutation!")
    print("   This indicates the mutable default bug is present.")
else:
    print("   ✓ SUCCESS: ua2 is independent of ua1!")
    print("   The mutable default parameter bug has been fixed.")

print("\n" + "=" * 60)
print("Testing different iterable types...")
print("=" * 60)

# Test list input
print("\n5. Testing list input...")
ua_list = FakeUserAgent(browsers=["chrome", "firefox"])
print(f"   browsers (list): {ua_list.browsers}")

# Test tuple input
print("\n6. Testing tuple input...")
ua_tuple = FakeUserAgent(browsers=("chrome", "firefox"))
print(f"   browsers (tuple): {ua_tuple.browsers}")

# Test set input
print("\n7. Testing set input...")
ua_set = FakeUserAgent(browsers={"chrome", "firefox"})
print(f"   browsers (set): {sorted(ua_set.browsers)}")

# Test string input
print("\n8. Testing string input...")
ua_string = FakeUserAgent(browsers="chrome")
print(f"   browsers (string): {ua_string.browsers}")

print("\n" + "=" * 60)
print("Testing error handling...")
print("=" * 60)

# Test invalid input
print("\n9. Testing invalid input (should raise TypeError)...")
try:
    ua_invalid = FakeUserAgent(browsers=123)
    print("   ❌ FAIL: No exception raised!")
except TypeError as e:
    print(f"   ✓ SUCCESS: TypeError raised as expected")
    print(f"   Message: {e}")
except AssertionError as e:
    print(f"   ❌ FAIL: AssertionError raised (should be TypeError)")

print("\n" + "=" * 60)
print("All demonstrations completed successfully!")
print("=" * 60)
