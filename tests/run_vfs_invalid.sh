#!/bin/bash
cd "$(dirname "$0")/.."

echo "this is not a zip" > tests/vfs_invalid.zip

python3 src/main.py --vfs-path "tests/vfs_invalid.zip"

rm -f tests/vfs_invalid.zip