#!/usr/bin/python3
"""Contains class Message"""
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey


class Message(BaseModel, Base):
    """Representation of a message"""
    __tablename__ = "messages"
    sender = Column(String(60), ForeignKey('users.id'), nullable=False)
    receiver = Column(String(60), ForeignKey('users.id'), nullable=False)
    message = Column(String(60), nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
