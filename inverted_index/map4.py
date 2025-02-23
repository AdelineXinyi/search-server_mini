#!/usr/bin/env python3
"""map4."""
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    doc_id, term, tfidfsquared, idfk, tf = line.split("\t")
    print(f"{doc_id}\t{term}\t{tfidfsquared}\t{idfk}\t{tf}")
