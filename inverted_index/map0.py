#!/usr/bin/env python3
"""map0."""
import sys

for line in sys.stdin:
    if "<!DOCTYPE html>" in line:
        print(f"doc\t{1}")
