#!/usr/bin/python3
"""Defines all users routes"""
from flask import jsonify, request, abort
from models import storage
from models.user import User
from models.interest import Interest
from api.views import app_views


@app_views.route('/interests', methods=['GET'])
def get_interests():
    all_interests = []
    for obj in list(storage.all(Interest).values()):
        all_interests.append(obj.to_dict())
    return jsonify(all_interests)
    

@app_views.route('/interests', methods=['POST'])
def post_interests():
    data = request.get_json()
    if data is None:
        abort(400, 'Not json')
    if storage.check_interest(data['name']):
        return jsonify({"error": "interest already exists"}), 400
    new = Interest(**data)
    storage.new(new)
    storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/interest/<interest_id>/users', methods=['GET'])
def get_users_with_interest(interest_id):
    """Get users with this interest"""
    interest = storage.get(Interest, interest_id)
    if interest:
        users = []
        for user_id in list(storage.all(User).keys()):
            user = storage.get(User, user_id.split('.')[1])
            if interest in user.interests:
                users.append(user.to_dict())
        return jsonify(users), 200
    return jsonify({'error': 'interest not found'})


@app_views.route("/interest/<interest_id>", methods=['DELETE'])
def delete_interest(interest_id):
    user = storage.get(Interest, interest_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    return jsonify({"error": "This user don't exist"})
