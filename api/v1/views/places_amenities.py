#!/usr/bin/python3
"""places_amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from datetime import datetime
import uuid
from os import getenv

@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place.

    Args:
        place_id (str): The ID of the Place.

    Returns:
        JSON: A list of Amenity objects in JSON format.

    Raises:
        404: If the place_id is not linked to any Place object.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes an Amenity object from a Place.

    Args:
        place_id (str): The ID of the Place.
        amenity_id (str): The ID of the Amenity.

    Returns:
        JSON: An empty dictionary with a status code 200.

    Raises:
        404: If the place_id is not linked to any Place object.
        404: If the amenity_id is not linked to any Amenity object.
        404: If the Amenity is not linked to the Place before the request.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if storage_t == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """
    Links an Amenity object to a Place.

    Args:
        place_id (str): The ID of the Place.
        amenity_id (str): The ID of the Amenity.

    Returns:
        JSON: The Amenity object in JSON format.

    Raises:
        404: If the place_id is not linked to any Place object.
        404: If the amenity_id is not linked to any Amenity object.

    Notes:
        - If the Amenity is already linked to the Place, the function
          returns the Amenity with a status code 200.
        - If the Amenity is successfully linked, the function returns
          the Amenity with a status code 201.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if storage_t == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
