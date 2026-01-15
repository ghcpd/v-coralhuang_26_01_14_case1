#!/usr/bin/env bash
set -e
python -m pip install -r requirements.txt
export PYTHONPATH=src
python -m pytest -q