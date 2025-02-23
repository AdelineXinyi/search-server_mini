#!/usr/bin/env python3
"""map2."""
import sys

# Read lines from stdin
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        doc_id, term, tf = line.split("\t")
        print(f"{term}\t{doc_id}\t{tf}")
    except ValueError:
        print(f"Malformed line: {line}", file=sys.stderr)
