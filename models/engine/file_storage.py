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

    def new(self, obj):
        """sets in __objs the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objs[key] = obj

    def save(self):
        """serializes __objs to the JSON file (path: __f_p)"""
        json_objs = {}
        for key in self.__objs:
            json_objs[key] = self.__objs[key].to_dict()
        with open(self.__f_p, 'w') as f:
            json.dump(json_objs, f)

    def reload(self):
        """deserializes the JSON file to __objs"""
        try:
            with open(self.__f_p, 'r') as f:
                juo = json.load(f)
            for key in juo:
                self.__objs[key] = clses[juo[key]["__class__"]](**juo[key])
        except:
            pass

    def delete(self, obj=None):
        """delete obj from __objs if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objs:
                del self.__objs[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
