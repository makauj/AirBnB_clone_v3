#!/usr/bin/python3
"""principal application app"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
from flasgger import Swagger


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def close_storage(exception):
    """close storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """not found"""
    return make_response(jsonify({"error": "Not found"}), 404)


app.config['SWAGGER'] = {
    'title': 'AirBnB clone RESTful API',
    'description': 'RESTful API for the AirBnB clone project',
    'uiversion': 3
}
swagger = Swagger(app)


if __name__ == "__main__":
    """main"""
    host = getenv("HBNB_API_HOST", default="0.0.0.0")
    port = getenv("HBNB_API_PORT", default=5000)
    app.run(host, int(port), threaded=True)
