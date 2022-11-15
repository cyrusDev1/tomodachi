#!/usr/bin/python3
"""Contains class BaseModel"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String
Base = declarative_base()


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs) -> None:
        """Initialisation of the base Model"""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key == "created_at":
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        if key == "id":
                            setattr(self, key, str(uuid4()))
                        setattr(self, key, value)            


    def __str__(self) -> str:
        """Return description of instance"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)


    def to_dict(self) -> dict:
        """return object in dict"""
        new_dict = self.__dict__.copy()
        time = "%Y-%m-%dT%H:%M:%S"
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "_sa_instance_state" in new_dict:
            del new_dict['_sa_instance_state']
        if "interests" in new_dict:
            interests = []
            tmp = new_dict['interests']
            for interest in tmp:
                interests.append(interest.to_dict())
            new_dict['interests'] = interests
        return new_dict
