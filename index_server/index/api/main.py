"""index server."""
import os
import re
import math
from flask import jsonify, request


# Default PageRank weight
DEFAULT_PAGERANK_WEIGHT = 0.5
inverted_index = {}
stopwords = set()
pagerank = {}


def load_index(index_path):
    """Loadindex."""
    # Load inverted index
    index_full_path = os.path.join(
        "index_server", "index", "inverted_index", index_path
    )
    try:
        with open(index_full_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip empty lines
                if not line:
                    continue
                # Split by tab character to extract fields
                fields = line.split()
                if len(fields) >= 3:
                    postings = []
                    for i in range(2, len(fields), 3):
                        doc_id = fields[i]
                        term_freq = int(fields[i+1])
                        norm_factor = float(fields[i+2])
                        postings.append((doc_id, term_freq, norm_factor))
                    # [term]=(idf,...)
                    inverted_index[fields[0]] = (float(fields[1]), postings)
                else:
                    print(f"Skipping malformed line: {line}")
    except FileNotFoundError:
        print(f"Error: Inverted index file '{index_path}' not found.")
        return

    stopwords_path = os.path.join("index_server", "index", "stopwords.txt")
    with open(stopwords_path, "r", encoding="utf-8") as f:
        stopwords.update(f.read().splitlines())

    pagerank_path = os.path.join("index_server", "index", "pagerank.out")
    try:
        with open(pagerank_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip empty lines
                if not line:
                    continue
                # Split by comma to separate doc_id and pagerank value
                fields = line.split(',')

                if len(fields) == 2:
                    doc_id = fields[0]
                    pagerank_value = float(fields[1])
                    pagerank[doc_id] = pagerank_value
                else:
                    print(f"Skipping malformed pagerank line: {line}")
    except FileNotFoundError:
        print("Error: PageRank file 'pagerank.out' not found.")
        return

    print("Index, stopwords, and PageRank loaded successfully!")


def clean_text(text, stop_words):
    """Clean with stopwords."""
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)

    text = text.casefold()

    terms = text.split()

    cleaned_terms = [term for term in terms if term not in stop_words]

    return cleaned_terms


def configure_routes(app):
    """Routes."""
    @app.route("/api/v1/", methods=["GET"])
    def list_services():
        """Render the menu."""
        return jsonify({
            "hits": "/api/v1/hits/",
            "url": "/api/v1/"
        })

    @app.route("/api/v1/hits/", methods=["GET"])
    def search_hits():
        """Render the hits and display the results."""
        try:
            pweight = float(request.args.get("w", DEFAULT_PAGERANK_WEIGHT))
        except ValueError:
            return jsonify({"error": "Parameter 'w' must be a float"}), 400

        # Clean the query
        query = request.args.get("q", "").strip()
        cleaned_terms = clean_text(query, stopwords)
        print("cleaned_terms")
        print(cleaned_terms)
        if not cleaned_terms:
            return jsonify({"hits": []})
        vector = [(term, cleaned_terms.count(term) * inverted_index[term][0])
                  for term in set(cleaned_terms) if term in inverted_index]
        print(vector)
        magnitude = math.sqrt(sum(tf_idf ** 2 for _, tf_idf in vector))
        if magnitude == 0:
            return jsonify({"hits": []})
        norm_query_vector = {
            vector[i][0]: vector[i][1] / magnitude
            for i in range(len(vector))
        }
        print(norm_query_vector)
        rele_doc = None
        for term in set(cleaned_terms):
            if term in inverted_index:
                doc_ids = {doc_id for doc_id, _, _ in inverted_index[term][1]}
                rele_doc = doc_ids if rele_doc is None else rele_doc & doc_ids
            else:
                return jsonify({"hits": []})
        doc_scores = {}
        for doc_id in rele_doc:
            # what if 0
            norm_doc_vector = {
                term: tf * inverted_index[term][0] / math.sqrt(norm_factor)
                for term in cleaned_terms if term in inverted_index
                for doc_tuple_id, tf, norm_factor in inverted_index[term][1]
                if doc_tuple_id == doc_id and norm_factor > 0
            }
            # Compute cosine similarity
            cos_sm = sum(
                norm_query_vector.get(term, 0) * norm_doc_vector.get(term, 0)
                for term in norm_query_vector
            )
            # ISBN calculated by this
            doc_scores[doc_id] = (
                pweight * pagerank.get(doc_id, 0)
                + (1 - pweight) * cos_sm
            )

        # Sort results by score in descending order
        sorted_scores = sorted(doc_scores.items(), key=lambda x: -x[1])
        hits = [
            {"docid": int(doc_id), "score": score}
            for doc_id, score in sorted_scores
        ]

        return jsonify({"hits": hits})
