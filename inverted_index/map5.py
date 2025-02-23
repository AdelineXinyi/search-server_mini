#!/usr/bin/env python3
"""map5."""
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    # FIX:absolute value for di
    doc_id, term, normal_tfidf, idfk, tf = line.split("\t")
    # Calculate doc_id % 3 for partitioning
    partition_key = int(doc_id) % 3
    # Output partition key and the associated data (term, tf, norm factor)
    print(f"{partition_key}\t{term}\t{idfk}\t{doc_id}\t{tf}\t{normal_tfidf}")
