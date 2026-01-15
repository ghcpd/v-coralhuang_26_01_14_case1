#!/bin/bash
# run_tests.sh - One-click test runner for FakeUserAgent mutable default fix
# Usage: ./run_tests.sh

echo "============================================"
echo "FakeUserAgent Test Suite"
echo "============================================"
echo ""

# Run pytest with verbose output
python -m pytest test_fake.py -v

# Capture the exit code
EXIT_CODE=$?

echo ""
echo "============================================"
if [ $EXIT_CODE -eq 0 ]; then
    echo "SUCCESS: All tests passed!"
else
    echo "FAILURE: Some tests failed!"
fi
echo "============================================"

exit $EXIT_CODE
