#!/usr/bin/python3
"""Contains class Connection"""
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean


class Connection(BaseModel, Base):
    """Representation of a connection"""
    __tablename__ = "connections"
    first_user = Column(String(60), ForeignKey('users.id'), nullable=False)
    second_user = Column(String(60), ForeignKey('users.id'), nullable=False)
    first_user_link_second_user = Column(Integer, nullable=False)
    second_user_link_first_user = Column(Integer, nullable=False)
    match = Column(Boolean(1), nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

