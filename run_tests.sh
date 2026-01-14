#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running tests..."
cd src
python -m pytest test_fake.py -v

echo "Tests completed."