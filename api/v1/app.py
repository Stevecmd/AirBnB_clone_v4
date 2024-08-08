#!/usr/bin/python3
""" Flask Application """
from os import environ

from flasgger import Swagger
from flasgger.utils import swag_from
from flask import Flask
from flask import jsonify
from flask import make_response
from flask import render_template
from flask_cors import CORS

from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(error):
    """Close Storage

    :param error: 

    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 Error
    ---
    responses:
      404:
        description: a resource was not found

    :param error: 

    """
    return make_response(jsonify({"error": "Not found"}), 404)


app.config["SWAGGER"] = {"title": "AirBnB clone Restful API", "uiversion": 3}

Swagger(app)


if __name__ == "__main__":
    """Main Function"""
    host = environ.get("HBNB_API_HOST")
    port = environ.get("HBNB_API_PORT")
    if not host:
        host = "0.0.0.0"
    if not port:
        port = "5000"
    app.run(host=host, port=port, threaded=True)
