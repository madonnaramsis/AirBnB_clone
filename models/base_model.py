#!/usr/bin/python3
"""
Project's base module
"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """
    The base class that project classes will inheret from it.
    """

    def __init__(self, *args, **kwargs):
        """Class constructor"""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key == "created_at":
                    self.created_at = datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.updated_at = datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    setattr(self, key, value)
        else:
            models.storage.new(self)

    def __str__(self):
        """The string representation of the instance."""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates updated_at attribute."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of __dict__"""
        ins_dict = self.__dict__.copy()
        ins_dict["__class__"] = self.__class__.__name__
        ins_dict["created_at"] = self.created_at.isoformat()
        ins_dict["updated_at"] = self.updated_at.isoformat()
        return ins_dict
