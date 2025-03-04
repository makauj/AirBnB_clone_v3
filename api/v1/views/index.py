#!/usr/bin/python3
"""app views"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, Flask


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def count():
    """returns stats"""
    return jsonify({"amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")})
