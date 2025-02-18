#!/usr/bin/python3
"""State Module for HBNB project"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('swagger_yaml/state_get.yml', methods=['GET'])
def get_all_states():
    """ Retrieves the list of all State objects """
    states = storage.all(state.State).values()
    states_list = []
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from('swagger_yaml/state_id_get.yml', methods=['GET'])
def get_state(state_id):
    """ Retrieves a State object """
    state = storage.get(state.State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                    strict_slashes=False)
@swag_from('swagger_yaml/state_id_delete.yml', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State object """
    state = storage.get(state.State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('swagger_yaml/state_post.yml', methods=['POST'])
def post_state():
    """ Creates a State """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = state.State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from('swagger_yaml/state_id_put.yml', methods=['PUT'])
def put_state(state_id):
    """ Updates a State object """
    state = storage.get(state.State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
