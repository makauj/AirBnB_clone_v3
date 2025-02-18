#!/usr/bin/python3
"""app"""
from flask import Blueprint
import api.v1.views


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
