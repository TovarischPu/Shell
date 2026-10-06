#!/bin/bash
cd "$(dirname "$0")/.."

if [ ! -f tests/vfs_deep.zip ]; then
    python3 tests/create_vfs.py
fi

python3 src/main.py \
    --vfs-path "tests/vfs_deep.zip" \
    --script "tests/test_stage4.txt"