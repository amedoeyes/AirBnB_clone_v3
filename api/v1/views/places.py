#!/usr/bin/python3
"""
Places view
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route(
    "/cities/<city_id>/places", methods=["GET"], strict_slashes=False
)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
    "/places/<place_id>", methods=["DELETE"], strict_slashes=False
)
def delete_place(place_id):
    """
    Deletes a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    "/cities/<city_id>/places", methods=["POST"], strict_slashes=False
)
def post_place(city_id):
    """
    Creates a Place object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, request.get_json()["user_id"])
    if user is None:
        abort(404)
    if "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    place = Place(**request.get_json())
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def put_place(place_id):
    """
    Updates a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())
