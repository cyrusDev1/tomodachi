#!/usr/bin/python3
"""Defines all users routes"""
from flask import jsonify, request, abort
from models import storage
from models.user import User
from models.connection import Connection
from api.views import app_views


@app_views.route('/link', methods=['POST'])
def link_two_user():
    """link two user"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a json")
    try:
        sender_id = data['sender_id']
        receiver_id = data['receiver_id']
        link_type = data['link_type']
    except KeyError:
        abort("Missing information")
    if storage.already_link(sender_id, receiver_id) is False:
        dict_new = {'first_user_id': sender_id,
               'second_user_id': receiver_id,
               'first_user_link_second_user': link_type,
               'second_user_link_first_user': 2,
               'match': 0
        }
        new_connection = Connection(**dict_new)
        storage.new(new_connection)
        storage.save()
        return jsonify(new_connection.to_dict())
    else:
        connection = storage.already_link(sender_id, receiver_id)
        if (sender_id == connection.first_user_id):
            connection.first_user_link_second_user = link_type
        elif (sender_id == connection.second_user_id):
            connection.second_user_link_first_user = link_type
        if (connection.first_user_link_second_user == 1 and
                connection.second_user_link_first_user == 1):
            connection.match = 1
        else:
            connection.match = 0
        storage.save()
    return jsonify(connection.to_dict())
