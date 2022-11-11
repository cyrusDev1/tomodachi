#!/usr/bin/python3
"""Handle storage"""
from models.base_model import Base
from os import getenv
from sqlalchemy import create_engine
from models.connection import Connection
from models.user import User
from models.message import Message
from models.interest import Interest
from models.connection import Connection


class Storage:
    """Storage class"""
    __engine = None
    __session = None

    def __init__(self) -> None:
        "Initialise db storage"
        MYSQL_USER = getenv('MYSQL_USER')
        MYSQL_PWD = getenv('MYSQL_PWD')
        MYSQL_HOST = getenv('MYSQL_HOST')
        MYSQL_DB = getenv('MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(MYSQL_USER, MYSQL_PWD,
                                      MYSQL_HOST, MYSQL_DB), pool_pre_ping=True)

    def reload(self):
        Base.metadata.create_all(self.__engine)


    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)
 