#!/usr/bin/python3
"""Contains class Message"""
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Message(BaseModel, Base):
    """Representation of a message"""
    __tablename__ = "messages"
    sender_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    receiver_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    message = Column(String(60), nullable=False)
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
