#!/usr/bin/env python3
"""map3."""
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    # Extract the doc_id, term, and aggregated_TF-IDF from the line
    term, doc_id, idfk, tf = line.split("\t")
    idfk = float(idfk)
    tf = int(tf)
    tf_idf = idfk * tf
    # Print the output in the format: key\t{line}
    print(f"{doc_id}\t{term}\t{tf_idf}\t{idfk}\t{tf}")
