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


@app_views.route("/interests/<interest_id>", methods=['DELETE'])
def delete_user(interest_id):
    user = storage.get_user(Interest, interest_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    return jsonify({"error": "This user don't exist"})

