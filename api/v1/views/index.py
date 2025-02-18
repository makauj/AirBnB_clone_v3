#!/usr/bin/python3
"""app views"""
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """status"""
    return {"status": "OK"}
