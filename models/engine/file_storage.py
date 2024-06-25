#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

clses = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    __f_p = "file.json"
    __objs = {}

    def all(self, cls=None):
        """returns the dictionary __objs"""
        if cls is not None:
            nw_dct = {}
            for key, value in self.__objs.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    nw_dct[key] = value
            return nw_dct
        return self.__objs

    def new(self, ubj):
        """sets in __objs the ubj with key <ubj class name>.id"""
        if ubj is not None:
            key = ubj.__class__.__name__ + "." + ubj.id
            self.__objs[key] = ubj

    def save(self):
        """serializes __objs to the JSON file (path: __f_p)"""
        json_objects = {}
        for key in self.__objs:
            json_objects[key] = self.__objs[key].to_dict()
        with open(self.__f_p, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objs"""
        try:
            with open(self.__f_p, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objs[key] = clses[jo[key]["__class__"]](**jo[key])
        except:
            pass

    def delete(self, ubj=None):
        """delete ubj from __objs if it’s inside"""
        if ubj is not None:
            key = ubj.__class__.__name__ + '.' + ubj.id
            if key in self.__objs:
                del self.__objs[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
