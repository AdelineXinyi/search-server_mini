#!/usr/bin/env python3
"""reduce0."""
import sys
import itertools


def reduce_one_group(group):
    """reduce0."""
    total_frequency = 0
    for line in group:
        _, value = line.strip().split("\t")
        total_frequency += int(value)
    print(f"{total_frequency}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group)


if __name__ == "__main__":
    main()
