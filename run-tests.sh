#!/bin/sh
set -e
cd "$(dirname "$0")/code"
(cd decide && python3 -m unittest)
python3 -m unittest discover -s tests
echo "all tests passed"
