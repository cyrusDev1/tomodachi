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
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import or_, and_, desc

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

    def all(self, cls=None):
        if cls:
            objects = self.__session.query(cls).all()
        dico = {}
        for obj in objects:
            key = obj.__class__.__name__ + '.' + obj.id
            dico[key] = obj
        return dico

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """CLose the current session"""
        self.__session.close()

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)
    
    def save(self):
        """commit all updates"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete the object"""
        if obj:
            self.__session.delete(obj)

    def delete_all(self, cls):
        """delete all row for this class"""
        self.__session.query(cls).delete()


    def check_email(self, email=""):
        if email:
            result = self.__session.query(User).filter(User.email == email)        
        if list(result) == []:
            return False
        return True

    def check_interest(self, interest=""):
        """Check if interest exist"""
        if interest:
            result = self.__session.query(Interest).filter(Interest.name == interest)        
        if list(result) == []:
            return False
        return True

    def already_link(self, sender_id, receiver_id):
        """Check if users are already linked"""
        if sender_id and receiver_id:
            result = self.__session.query(Connection).filter(
                or_(
                    and_(Connection.first_user_id  == sender_id, Connection.second_user_id == receiver_id),
                    and_(Connection.first_user_id  == receiver_id, Connection.second_user_id == sender_id)
                )
            )               
        if list(result) == []:
            return False
        return list(result)[0]

    def sent(self, user_id):
        """"""
        result = self.__session.query(Connection).filter(Connection.first_user_id == user_id, 
            Connection.first_user_link_second_user == 1, Connection.match == 0)
        return list(result)

    def received(self, user_id):
        """"""
        result = self.__session.query(Connection).filter(Connection.second_user_id == user_id, 
            Connection.first_user_link_second_user == 1, Connection.match == 0, Connection.second_user_link_first_user == 2)
        return list(result)

    def matches(self, user_id):
        """"""
        result = self.__session.query(Connection).filter(
            and_(
                or_(Connection.first_user_id == user_id, Connection.second_user_id == user_id),
                Connection.match == 1
            )
        )
        return list(result)

    def user_has_match(self, sender_id, receiver_id):
        """"""
        result = self.__session.query(Connection).filter(
            and_(
               or_(
                    and_(Connection.first_user_id  == sender_id, Connection.second_user_id == receiver_id),
                    and_(Connection.first_user_id  == receiver_id, Connection.second_user_id == sender_id)
                ),
                Connection.match == 1
            )
        )
        if list(result) == []:
            return False
        return True

    def get_messages(self, sender_id, receiver_id):
        """"""
        result = self.__session.query(Message).filter(
            or_(
                and_(Message.sender_id == sender_id, Message.receiver_id == receiver_id),
                and_(Message.sender_id == receiver_id, Message.receiver_id == sender_id)
            )
        ).order_by(desc(Message.created_at)).all()
        return list(result)

    
    def get_list_messages(self, user_id):
        """"""
        result = self.__session.query(Message).filter(
            or_(
                Message.sender_id == user_id, Message.receiver_id == user_id
            )
        ).all()
        return list(result)


    def check_user(self, data):
        """"""
        email = data['email']
        password = data['password']
        result = self.__session.query(User).filter(and_(User.email == email, User.password == password))
        if list(result) == []:
            return None
        return list(result)[0]

    def get(self, cls, id):
        try:
            objects = {}
            for obj in list(self.all(cls).values()):
                objects[obj.id] = obj
            return objects.get(id)
        except Exception:
            return None
