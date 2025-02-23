#!/usr/bin/env python3
"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
import math

term_doc_count = {}  # {term: nk}
term_idf = {}        # {term: idfk}


# calculate nk and idfk
def reduce_one_group(key, group):
    """reduce."""
    with open("total_document_count.txt", "r", encoding='utf-8') as f:
        doc_num = int(f.read().strip())
    doc_ids = set()
    # Convert group to a list for repeated iterations
    group = list(group)
    # Populate the document set and count TFs
    term_tf = []
    for line in group:
        line = line.strip()
        if not line:
            continue
        try:
            _, doc_id, tf = line.split("\t")
            doc_ids.add(doc_id)
            term_tf.append((doc_id, int(tf)))
        except ValueError:
            # Skip malformed lines
            continue
    # Calculate nk and idfk
    nk = len(doc_ids)
    if nk == 0:
        return
    idfk = math.log10(doc_num / nk)
    # Store nk and idfk globally
    term_doc_count[key] = nk
    term_idf[key] = idfk
    # Emit data for each document
    for doc_id, tf in term_tf:
        print(f"{key}\t{doc_id}\t{idfk}\t{tf}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
