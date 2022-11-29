#!/usr/bin/python3
"""Defines all users routes"""
from flask import jsonify, request, abort, make_response
from models import storage
from models.user import User
from models.interest import Interest
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
    if storage.check_email(data['email']):
        return jsonify({"error": "email already exists"}), 400
    new = User(**data)
    storage.new(new)
    storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data is None:
        abort(400, 'Not json')
    user =  storage.check_user(data)
    if user is None:
        return make_response(jsonify({"error": "Email or password not correct"}), 401)
    return jsonify(user.to_dict()), 200


@app_views.route("/user/<user_id>", methods=['GET'])
def get_user(user_id):
    """get a user with this user_id"""
    user = storage.get(User, user_id)
    if user:
        print(user)
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "This user don't exist"}), 400


@app_views.route("/user/<user_id>/interests", methods=['GET'])
def get_interests_ofuser(user_id):
    """get interests of user"""
    user = storage.get(User, user_id)
    if user:
        user_interests = [interest.to_dict() for interest in user.interests]
        return jsonify(user_interests)
    return jsonify({"error": "This user don't exist"}), 400  


@app_views.route("/user/interests", methods=['POST'])
def post_interests_ofuser():
    """post interests of user"""
    data = request.get_json()
    if data is None:
        abort(400)
    user_id = data['user_id']
    interests = data['interests']
    if user_id and interests:
        user = storage.get(User, user_id)
        if user:
            for id_interest in interests:
                interest = storage.get(Interest, id_interest)
                if interest is None:
                    return jsonify({"error": "One  or many interests not found"}), 400
                else:
                    if interest not in user.interests:
                        user.interests.append(interest)
                        storage.save()
            user_interests = [interest.to_dict() for interest in user.interests]
            return jsonify(user_interests), 201
    return jsonify({"error": "This user don't exist"}), 400


@app_views.route("/user/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    return jsonify({"error": "This user don't exist"}), 400


@app_views.route("/user/<user_id>/sent")
def get_sent(user_id):
    sent = storage.sent(user_id)
    users = [] 
    for conn in sent:
        user_received = storage.get(User, conn.second_user_id)
        users.append(user_received.to_dict())
    return jsonify(users)


@app_views.route("/user/<user_id>/received")
def get_received(user_id):
    received = storage.received(user_id)
    users = [] 
    for conn in received:
        user_send = storage.get(User, conn.first_user_id)
        users.append(user_send.to_dict())
    return jsonify(users)


@app_views.route("/user/<user_id>/matches")
def get_matches(user_id):
    users = []
    matches = storage.matches(user_id)
    for conn in matches:
        if user_id == conn.first_user_id:
            user_match = storage.get(User, conn.second_user_id)
        elif user_id == conn.second_user_id:
            user_match = storage.get(User, conn.first_user_id)
        users.append(user_match.to_dict())
    return jsonify(users)


@app_views.route("/user/<user_id>/swipping")
def get_swip(user_id):
    all_users = []
    for obj in list(storage.all(User).values()):
        if user_id != obj.id:
            all_users.append(obj)
    print(len(all_users))
    no_matches = []
    for user in all_users:
        if storage.user_has_match(user.id, user_id) is False:
            no_matches.append(user)

    print(len(no_matches))
    _sent = []
    sent = storage.sent(user_id)
    for conn in _sent:
        user_received = storage.get(User, conn.second_user_id)
        _sent.append(user_received)
    no_sent = []
    print(len(_sent))
    for no_match in no_matches:
        if no_match not in _sent:
            no_sent.append(no_match)

    swip = []
    for obj in no_sent:
        swip.append(obj.to_dict())
    print(len(swip))
    return jsonify(swip)
