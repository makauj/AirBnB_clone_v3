#!/usr/bin/python3
"""users module"""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.user import User
from flasgger.utils import swag_from


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('swagger_yaml/user_get.yml', methods=['GET'])
def get_all_users():
    """get all users"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('swagger_yaml/user_id_get.yml', methods=['GET'])
def get_user(user_id):
    """get a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('swagger_yaml/user_id_delete.yml', methods=['DELETE'])
def delete_user(user_id):
    """delete a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('swagger_yaml/user_post.yml', methods=['POST'])
def post_user():
    """create a user"""
    user_json = request.get_json()
    if user_json is None:
        abort(400, 'Not a JSON')
    if 'email' not in user_json:
        abort(400, 'Missing email')
    if 'password' not in user_json:
        abort(400, 'Missing password')
    user = User(**user_json)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('swagger_yaml/user_id_put.yml', methods=['PUT'])
def put_user(user_id):
    """update a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_json = request.get_json()
    if user_json is None:
        abort(400, 'Not a JSON')
    for key, value in user_json.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>/change_role', methods=['POST'],
                    strict_slashes=False)
@swag_from('swagger_yaml/user_id_change_role.yml', methods=['POST'])
def create_user(user_id):
    """create a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_json = request.get_json()
    if user_json is None:
        abort(400, 'Not a JSON')
    if 'role' not in user_json:
        abort(400, 'Missing role')
    user.role = user_json['role']
    user.save()
    return jsonify(user.to_dict())



@app_views.route('/users/logout', methods=['POST'], strict_slashes=False)
def logout_user():
    """logout a user"""
    return jsonify({}), 200
