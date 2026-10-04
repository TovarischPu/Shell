#!/bin/bash
echo "=== Test: Both parameters ==="
python3 src/main.py \
    --vfs-path "/tmp/vfs_data" \
    --script "tests/valid_commands.txt"