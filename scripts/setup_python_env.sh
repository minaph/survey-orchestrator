#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$project_dir"

python3 -c 'import sys; assert sys.version_info[:2] == (3, 12), "Run this script with devbox run setup (Python 3.12 required)"'
python3 -m venv .venv
.venv/bin/python -m pip install --disable-pip-version-check --only-binary=:all: -r requirements.txt
.venv/bin/python -m pip check
