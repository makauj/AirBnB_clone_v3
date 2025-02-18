#!/usr/bin/python3
"""places reviews"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.user import User
from models import storage
from models.place import Place
from models.review import Review
from flasgger import swag_from


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/reviews/get_reviews.yml')
def get_all_reviews(place_id):
    """get reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                    strict_slashes=False)
@swag_from('documentation/reviews/get_review.yml')
def get_review(review_id):
    """get review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                    strict_slashes=False)
@swag_from('documentation/reviews/delete_review.yml')
def delete_review(review_id):
    """delete review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                    strict_slashes=False)
@swag_from('documentation/reviews/post_review.yml')
def post_review(place_id):
    """post review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in data:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                    strict_slashes=False)
@swag_from('documentation/reviews/put_review.yml')
def put_review(review_id):
    """put review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
