#!/usr/bin/python3
"""Defines all users routes"""
from flask import jsonify, request, abort
from models import storage
from models.user import User
from models.connection import Connection
from models.message import Message
from api.views import app_views


@app_views.route('/messages', methods=['POST', 'GET'])
def post_message():
    """post new message"""
    data = request.get_json()
    if data is None:
        abort(400, "not a json")
    try:
        sender_id = data['sender_id']
        receiver_id = data['receiver_id']
    except KeyError:
        abort(400, "missing key")
    if storage.user_has_match(sender_id, receiver_id):
        if request.method == "POST":
            if data['message']:
                new_message = Message(**data)
                storage.new(new_message)
                storage.save()
                return jsonify(new_message.to_dict()), 201
        elif request.method == "GET":
            messages = storage.get_messages(sender_id, receiver_id)
            messages = [message.to_dict() for message in messages]
            return jsonify(messages), 200
    abort(400, "Users has no matches")
