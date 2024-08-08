#!/usr/bin/python3
""" Starts a Flash Web Application """
import logging
import uuid
from os import environ

from flask import Flask
from flask import redirect
from flask import render_template
from jinja2 import TemplateNotFound

from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State

app = Flask(__name__)
# app = Flask(__name__, template_folder='web_flask/templates/')
app.logger.setLevel(logging.DEBUG)
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def close_db(error):
    """Remove the current SQLAlchemy Session

    :param error: 

    """
    storage.close()


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """HBNB is alive!"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    st_ct = []

    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    return render_template(
        "0-hbnb.html",
        states=st_ct,
        amenities=amenities,
        places=places,
        cache_id=uuid.uuid4(),
    )


@app.route("/0-hbnb", strict_slashes=False)
def hbnb_0():
    """HBNB is alive!"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    st_ct = []

    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    return render_template(
        "0-hbnb.html",
        states=st_ct,
        amenities=amenities,
        places=places,
        cache_id=uuid.uuid4(),
    )


@app.route("/1-hbnb", strict_slashes=False)
def hbnb_1():
    """HBNB is alive!"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    st_ct = []

    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    return render_template(
        "1-hbnb.html",
        states=st_ct,
        amenities=amenities,
        places=places,
        cache_id=uuid.uuid4(),
    )


if __name__ == "__main__":
    """Main Function"""
    app.run(host="0.0.0.0", port=5000, debug=True)
