#!/usr/bin/env python3
"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
from collections import defaultdict


def reduce_one_group(key, group):
    """reduce."""
    term_frequencies = defaultdict(int)

    # Iterate through the group (list of content for the document)
    for content in group:
        _, content = content.split("\t", 1)
        # Split the content into terms
        terms = content.split()
        # Count the frequency of each term in the document
        for term in terms:
            term_frequencies[term] += 1

    # Output the term frequencies for the document
    for term, count in term_frequencies.items():
        print(f"{key}\t{term}\t{count}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
