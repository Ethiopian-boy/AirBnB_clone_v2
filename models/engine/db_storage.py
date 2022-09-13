#!/usr/bin/python3
""" DBStorage for the project """
import models
from os import getenv
from models.state import State
from models.city import City
from models.base_model import Base
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
from sqlalchemy import (create_engine)
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """
    SQLAlchemy database
    """
    __engine = None
    __session = None

    def __init__(self):
        """ create an engine """
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        envv = getenv("HBNB_ENV", "none")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)
        if envv == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query current database session
        """
        classes = {'User': User, 'Place': Place, 'State': State, 'City': City,
                   'Amenity': Amenity, 'Review': Review}

        db_dict = {}

        if cls != "":
            objs = self.__session.query(self.classes[cls]).all()
            for obj in objs:
                key = "{}.{}".format(obj.__class__.name, obj.id)
                db_dict[key] = obj
            return db_dict
        else:
            for k, v in self.classes.items():
                objs = self.__session.query(v).all()
                if len(objs) > 0:
                    for obj in objs:
                        key = "{}.{}".format(obj.__class__.name, obj.id)
                        db_dict[key] = obj
            return db_dict

    def new(self, obj):
        """
        Add obj in the current database session
        """
        self.__session.add(obj)

    def save(self):
        """
        commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete from the current database session obj if not None
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        create all tables in the database
        create the current database session
        """

        Base.metadata.create_all(self.__engine)

        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """
        Remove or close the session
        """
        self.__session.close()
