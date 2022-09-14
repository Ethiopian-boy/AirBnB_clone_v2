#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        d = {}
        if cls is None:
            return self.__objects
        if cls != "":
            for key, val in self.__objects.items():
                if cls == key.split(".")[0]:
                    d[key] = val
            return d
        else:
            return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = str(obj.__class__.__name__) + "." + str(obj.id)
        value = obj
        FileStorage.__objects[key] = value

    def save(self):
        """Saves storage dictionary to file"""
        temp_dict = {}
        for k, val in FileStorage.__objects.items():
            temp_dict[k] = val.to_dict()

        with open(FileStorage.__file_path, 'w', encoding="UTF8") as f:
            json.dump(temp_dict, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            temp = {}
            with open(FileStorage.__file_path, encoding="UTF8") as f:
                FileStorage.__objects = json.load(f)
            for key, val in FileStorage.__objects.items():
                class_name = val["__class__"]
                class_name = models.classes[class_name]
                FileStorage.__objects[key] = class_name(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        if obj is not None:
            key = str(obj.__class__.__name__) + "." + str(obj.id)
            FileStorage.__objects.pop(key, None)
            self.save()

    def close(self):
        """ Deseralize json files to object """
        self.reload()
