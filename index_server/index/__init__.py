"""Start the app."""
import os
from flask import Flask
from index.api import load_index, configure_routes  # Import from `index.api`

# Create the Flask app instance
app = Flask(__name__)

# Configure the path for the inverted index
app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")

# Load inverted index, stopwords, and PageRank into memory
load_index(app.config["INDEX_PATH"])

# Configure routes for the app
configure_routes(app)
