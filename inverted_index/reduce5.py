#!/usr/bin/env python3
"""reduce."""
import sys
import itertools
from collections import defaultdict


def reduce_one_group(group):
    """reduce."""
    term_info = defaultdict(list)
    doc_ids = set()
    # Collect the data for each term and document in this partition
    for line in group:
        line = line.strip()
        if not line:
            continue
        _, term, idfk, doc_id, tf, norm_factor = line.split("\t")
        term_info[term].append((doc_id, idfk, tf, norm_factor))
        doc_ids.add(doc_id)
    # Sort terms alphabetically
    sorted_terms = sorted(term_info.keys())
    # For each term, calculate IDF and sort the document entries
    for term in sorted_terms:
        doc_info = term_info[term]
        # Sort document entries by doc_id (lexicographically)
        doc_info.sort(key=lambda x: x[0])  # Sort by doc_id
        # Extract idfk from the first document entry (a term has the same idfk)
        idfk = doc_info[0][1]
        idfk = float(idfk)
        # Format the output
        output = [f"{term} {idfk}"]
        # Append doc_id, term_freq, norm_factor for each document
        for doc_id, _, term_freq, norm_factor in doc_info:
            output.append(f"{doc_id} {term_freq} {norm_factor}")
        # Print the final output for this term
        print(" ".join(output))


def keyfunc(line):
    """Return the partition key (doc_id % 3)."""
    return line.partition("\t")[0]


def main():
    """Group lines by partition key and process them."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group)


if __name__ == "__main__":
    main()
