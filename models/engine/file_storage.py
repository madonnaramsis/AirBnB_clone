#!/usr/bin/python3
"""
Project's base module
"""
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import json


class FileStorage:
    """Base storage handling class to serialize/deserialize objects"""

    __file_path = "file.json"
    __objects = {}
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def all(self):
        """Returns all objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Add/update an object with key <obj class name>.id"""
        FileStorage.__objects["{}.{}".format(
            obj.__class__.__name__, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file"""
        odict = FileStorage.__objects
        objdict = {obj: odict[obj].to_dict() for obj in odict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objdict, f, indent=4)

    def reload(self):
        """Deserialize the JSON file to __objects"""
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(FileStorage.__classes[cls_name](**o))
        except FileNotFoundError:
            return
