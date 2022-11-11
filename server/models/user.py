#!/usr/bin/python3
"""Contains class User"""
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship

users_interests = Table('users_interests', Base.metadata,
                        Column('user_id', String(60), ForeignKey('users.id'), onupdate='CASCADE',
                                primary_key=True),
                        Column('interest_id', String(60), ForeignKey('interests.id'),
                                onupdate='CASCADE', primary_key=True))


class User(BaseModel, Base):
    """Representation of a user"""
    __tablename__ = 'users'
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password =  Column(String(128), nullable=False)
    gender =  Column(String(128), nullable=False)
    country =  Column(String(128), nullable=False)
    age = Column(String(128), nullable=False)
    picture =  Column(String(200), nullable=False)
    interests = relationship("Interest", secondary="users_interests", backref="users_interests", viewonly=False)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


#data = {'first_name': "Cyrus", 'last_name': "Houngue","password": "1240"}
#user = User(**data)
#print(user)
#print(user.to_dict())