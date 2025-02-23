#!/usr/bin/env python3
"""reduce."""
import sys
import itertools
from collections import defaultdict


def reduce_one_group(group):
    """reduce."""
    tfidf_squared_sum = defaultdict(float)
    doc_term_info = defaultdict(list)
    for line in group:
        line = line.strip()
        if not line:
            continue
        doc_id, term, tfidfsq, idfk, tf = line.split("\t")
        tfidfsq = float(tfidfsq)
        doc_term_info[doc_id].append((term, tfidfsq, idfk, tf))
        tfidf_squared_sum[doc_id] += tfidfsq
    for doc_id, terms_info in doc_term_info.items():
        squared_sum = tfidf_squared_sum[doc_id]
        if squared_sum > 0:
            for term, tfidfsq, idfk, tf in terms_info:
                normalized_tfidf = squared_sum
                print(f"{doc_id}\t{term}\t{normalized_tfidf}\t{idfk}\t{tf}")


def keyfunc(line):
    """reduce."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups share a (doc_id) and process them."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group)


if __name__ == "__main__":
    main()
