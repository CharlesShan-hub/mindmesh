#!/bin/bash

PYTHON_SCRIPT="../scripts/convert.py"

python $PYTHON_SCRIPT \
    --src "/Users/kimshan/public/library/mindmesh/data/obsidian" \
    --dist "/Users/kimshan/public/library/mindmesh/data/obsidian_to_gitbook" \
    --src_kind "obsidian" \
    --dist_kind "gitbook"
