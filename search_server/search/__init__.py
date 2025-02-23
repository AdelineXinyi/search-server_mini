"""Main code for app."""
from flask import Flask
from .views.view import search_views

# Create the Flask app instance
app = Flask(__name__)

# Register blueprints if any
app.register_blueprint(search_views)

# Other configuration like app config, logging, etc.
app.config.from_object('search.config')

if __name__ == "__main__":
    app.run(debug=True)
