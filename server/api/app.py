#!/usr/bin/python3
"""Tomodachi api"""
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from api.views import app_views
from models import storage


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origin": "*"}})
host = "0.0.0.0"
port = "5001"


@app.teardown_appcontext
def teardown(exc):
    """after each request, this method calls .close() on
    the current SQLAlchemy Session
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Handle not found page"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=host, port=port)
