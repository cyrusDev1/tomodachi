#!/usr/bin/python3
"""Defines all users routes"""
from flask import jsonify, request, abort
from models import storage
from models.user import User
from models.connection import Connection
from models.message import Message
from api.views import app_views


@app_views.route('/messages', methods=['POST'])
def post_message():
    """post new message"""
    data = request.get_json()
    if data is None:
        abort(401, "not a json")
    print(data)
    try:
        sender_id = data['sender_id']
        receiver_id = data['receiver_id']
        types = data['types']
    except KeyError:
        abort(402, "missing key")
    if storage.user_has_match(sender_id, receiver_id):
        if types == "post":
            if data['message']:
                new_message = Message(**data)
                storage.new(new_message)
                storage.save()
                return jsonify(new_message.to_dict()), 201
        elif types == "get":
            messages = storage.get_messages(sender_id, receiver_id)
            messages = [message.to_dict() for message in messages]
            return jsonify(messages), 200
    abort(400, "Users has no matches")



@app_views.route('/user/<user_id>/messages', methods=['GET'])
def get_message(user_id):
    """post new message"""
    messages = storage.get_list_messages(user_id)
    messages = [message.to_dict() for message in messages]
    return jsonify(messages), 200
