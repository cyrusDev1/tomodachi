#!/usr/bin/python3
"""Defines all users routes"""
from flask import jsonify, make_response, request, abort
from models import storage
from models.user import User

from api.views import app_views


@app_views.route('/users', methods=['GET'])
def get_users():
    all_users = []
    for obj in list(storage.all(User).values()):
        all_users.append(obj.to_dict())
    return jsonify(all_users)
    

@app_views.route('/users', methods=['POST'])
def post_user():
    data = request.get_json()
    if data is None:
        abort(400, 'Not json')
    if storage.get_email(data['email']):
        return jsonify({"error": "email already exists"}), 400
    new = User(**data)
    storage.new(new)
    storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/user/<user_id>", methods=['GET'])
def get_user(user_id):
    """get a user with this user_id"""
    user = storage.get_user(User, user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "This user don't exist"}), 400


@app_views.route("/user/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    user = storage.get_user(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    return jsonify({"error": "This user don't exist"})

