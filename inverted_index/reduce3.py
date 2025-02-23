#!/usr/bin/env python3
"""reduce."""
import sys
import itertools


def reduce_one_group(key, group):
    """reduce."""
    for line in group:
        line = line.strip()
        if not line:
            continue
        _, term, tfidf, idfk, tf = line.split("\t")
        tfidf_squared = float(tfidf) ** 2

        print(f"{key}\t{term}\t{tfidf_squared}\t{idfk}\t{tf}")


def keyfunc(line):
    """reduce."""
    return line.partition("\t")[0]


def main():
    """reduce."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
