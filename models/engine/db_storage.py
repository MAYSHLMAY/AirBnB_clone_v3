#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

clses = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """interacts with the db"""
    __engl = None
    __sess = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engl = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engl)

    def all(self, cls=None):
        """query on the current db session"""
        nw_dct = {}
        for clus in clses:
            if cls is None or cls is clses[clus] or cls is clus:
                obujs = self.__sess.query(clses[clus]).all()
                for obj in obujs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    nw_dct[key] = obj
        return (nw_dct)

    def new(self, obj):
        """add the object to the current db session"""
        self.__sess.add(obj)

    def save(self):
        """commit all changes of the current db session"""
        self.__sess.commit()

    def delete(self, obj=None):
        """delete from the current db session obj if not None"""
        if obj is not None:
            self.__sess.delete(obj)

    def reload(self):
        """reloads data from the db"""
        Base.metadata.create_all(self.__engl)
        sess_fact = sessionmaker(bind=self.__engl, expire_on_commit=False)
        Session = scoped_session(sess_fact)
        self.__sess = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__sess.remove()
