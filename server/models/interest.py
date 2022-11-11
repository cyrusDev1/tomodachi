#!/usr/bin/python3
"""Contains class Interest"""
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String


class Interest(BaseModel, Base):
    """Representation of an interest"""
    __tablename__ = "interests"
    name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)