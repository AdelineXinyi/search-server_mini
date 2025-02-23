"""Main code for fetching."""
import sqlite3
from urllib.parse import unquote
from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, render_template, request, current_app
import requests

search_views = Blueprint('search_views', __name__)


def get_document_details_from_db(docid):
    """Fetch document details from the database based on docid."""
    result_dict = {}
    try:
        # Connect to the database
        conn = sqlite3.connect("var/search.sqlite3")
        cursor = conn.cursor()
        # Query to get document details
        query = "SELECT title, summary, url FROM documents WHERE docid = ?"
        cursor.execute(query, (docid,))
        result = cursor.fetchone()
        # If a result is found, return it as a dictionary
        if result:
            result_dict = {
                "docid": docid,
                "title": result[0],
                "summary": result[1],
                "url": unquote(result[2])
            }
    except ConnectionError as e:
        print(f"Connection error while fetching {e}")
    finally:
        conn.close()
    return result_dict


def get_results_from_index(url, query, wt):
    """Fetch search results from an index server."""
    results = []
    try:
        # Make a request to the index server
        response = requests.get(url, params={'q': query, 'w': wt}, timeout=5)
        if response.status_code == 200:
            json_response = response.json()
            # Check if 'hits' exist in the response
            if "hits" in json_response:
                # For each hit, query the database for additional details
                for hit in json_response["hits"]:
                    docid = hit.get("docid")
                    doc_details = get_document_details_from_db(docid)
                    if doc_details:
                        # Add the details to the result
                        result = {
                            "docid": docid,
                            "title": doc_details["title"],
                            "summary": doc_details["summary"],
                            "url": doc_details["url"],
                            "score": hit.get("score", 0)
                        }
                        results.append(result)
                return results
    except ConnectionError as e:
        print(f"Connection error while fetching from {url}: {e}")
    return results


@search_views.route("/", methods=["GET", "POST"])
def search_page():
    """Render the search page and display the results."""
    query = request.args.get("q", "")
    weight = float(request.args.get("w", 0.5))
    index_urls = current_app.config['SEARCH_INDEX_SEGMENT_API_URLS']
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(get_results_from_index, url, query, weight)
            for url in index_urls
        ]
        results = []
        for future in futures:
            results.extend(future.result())
    final_results = sorted(results, key=lambda x: x['score'], reverse=True)
    final_results = final_results[:10]
    return render_template(
        "search.html",
        query=query,
        weight=weight,
        results=final_results
    )
