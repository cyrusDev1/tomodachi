#!/usr/bin/python3
"""Initialise the models package"""
from models.engine.storage import Storage


storage = Storage()
storage.reload()
