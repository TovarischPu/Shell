#!/bin/bash
cd "$(dirname "$0")/.."

python3 src/main.py --vfs-path "tests/nonexistent.zip"