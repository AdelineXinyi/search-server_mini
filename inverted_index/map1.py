#!/usr/bin/env python3
"""map1."""
import sys
import re
import bs4


# Cleaning function
def clean_text(text, words):
    """clean."""
    # Remove non-alphanumeric characters (except spaces)
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)

    # Convert to lowercase
    text = text.casefold()

    # Split into terms
    terms = text.split()

    # Remove stop words
    new_terms = [term for term in terms if term not in words]

    return new_terms


# Load stop words from file
with open("stopwords.txt", "r", encoding="utf-8") as stopwords_file:
    stop_words = set(line.strip() for line in stopwords_file)

HTML = ""
for line in sys.stdin:
    # Assume well-formed HTML docs:
    # - Starts with <!DOCTYPE html>
    # - Ends with </html>
    # - Contains a trailing newline
    if "<!DOCTYPE html>" in line:
        HTML = line
    else:
        HTML += line

    # If we're at the end of a document, parse
    if "</html>" not in line:
        continue

    # Configure Beautiful Soup parser
    soup = bs4.BeautifulSoup(HTML, "html.parser")

    # Get docid from the document
    meta_tag = soup.find("meta", attrs={"eecs485_docid": True})
    DOCID = meta_tag.get("eecs485_docid") if meta_tag else None

    # Parse content from document
    # get_text() will strip extra whitespace and
    # concatenate content, separated by spaces
    element = soup.find("html")
    content = element.get_text(separator=" ", strip=True)
    # Remove extra newlines
    content = content.replace("\n", "")

    # Clean the content
    cleaned_terms = clean_text(content, stop_words)

    # Print the output: doc_id and cleaned content (space-separated terms)
    print(f"{DOCID}\t{' '.join(cleaned_terms)}")

    # Reset HTML buffer for the next document
    HTML = ""
