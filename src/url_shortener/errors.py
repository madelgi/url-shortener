"""
Error handlers for URL shortener application.
"""
import logging
import traceback

from flask import json, current_app, jsonify
from werkzeug.exceptions import HTTPException


logger = logging.getLogger(__name__)


def handle_http_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"

    return response


def handle_value_error(e: ValueError):
    """Handles internal error.
    """
    if current_app.config.get('DEBUG', False):
        d = {
            "name": type(e).__name__,
            "description": str(e),
            "traceback": traceback.format_exc()
        }
        return jsonify(d), 500
    else:
        return jsonify({"description": "Something happened"}), 500
