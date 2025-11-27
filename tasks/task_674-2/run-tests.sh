#!/bin/bash
set -e

# Pin ALL required test dependencies
pip install pytest==8.2.2 jsonschema==4.23.0

pytest -q --disable-warnings --maxfail=1
