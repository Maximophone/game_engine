from enum import Enum
import numpy as np
import pickle
import codecs

from pyrr import Vector3

CLASS_REGISTER = {}
ENUM_REGISTER = {}


class DeserializeException(Exception):
    pass


class SerializeException(Exception):
    pass


class sproperty:
    "Emulate PyProperty_Type() in Objects/descrobject.c"
    serializable: bool = True

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc
        self._name = ''

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError(f'unreadable attribute {self._name}')
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError(f"can't set attribute {self._name}")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError(f"can't delete attribute {self._name}")
        self.fdel(obj)

    def getter(self, fget):
        prop = type(self)(fget, self.fset, self.fdel, self.__doc__)
        prop._name = self._name
        return prop

    def setter(self, fset):
        prop = type(self)(self.fget, fset, self.fdel, self.__doc__)
        prop._name = self._name
        return prop

    def deleter(self, fdel):
        prop = type(self)(self.fget, self.fset, fdel, self.__doc__)
        prop._name = self._name
        return prop


def serializable(*args):
    def inner(cls):
        if not hasattr(cls, "__serial"):
            cls.__serial = []
        else:
            # Inherited, we need to define a new one
            cls.__serial = cls.__serial[:]
        CLASS_REGISTER[repr(cls)] = cls
        for arg in args:
            cls.__serial.append(arg)
        for name, method in cls.__dict__.items():
            if hasattr(method, "serializable"):
                # do something with the method and class
                cls.__serial.append(name)
        return cls
    return inner


def senum(cls):
    """Registers an enum for serialization"""
    ENUM_REGISTER[repr(cls)] = cls
    if not hasattr(cls, "__senum"):
        cls.__senum = True
    return cls


def serialize(o: object) -> dict:
    if hasattr(o, "__serial"):
        ret = {"__type": repr(o.__class__), "val": {}}
        for name in o.__serial:
            value = getattr(o, name)
            ret["val"][name] = serialize(value)
        return ret
    elif isinstance(o, bool):
        return {"__type": "bool", "val": o}
    elif isinstance(o, int):
        return {"__type": "int", "val": o}
    elif isinstance(o, float):
        return {"__type": "float", "val": o}
    elif isinstance(o, str):
        return {"__type": "str", "val": o}
    elif o is None:
        return {"__type": "None", "val": None}
    elif isinstance(o, dict):
        ret = {"__type": "dict", "val": []}
        for key, value in o.items():
            ret["val"].append((serialize(key), serialize(value)))
        return ret
    elif isinstance(o, list):
        ret = {"__type": "list", "val": []}
        for value in o:
            ret["val"].append(serialize(value))
        return ret
    elif isinstance(o, set):
        ret = {"__type": "set", "val": []}
        for value in o:
            ret["val"].append(serialize(value))
        return ret
    elif isinstance(o, np.ndarray):
        return {"__type": "np.ndarray", "val": codecs.encode(pickle.dumps(o), 'base64').decode("utf-8")}
    elif isinstance(o, Enum) and hasattr(o, "__senum"):
        return {"__type": repr(o.__class__), "val": o.value}
    else:
        raise SerializeException(f"Object {o} is not serializable")
        
        
def deserialize(d: dict):
    if "__type" not in d:
        raise DeserializeException(f"Invalid dictionary, missing __type key: {d}")
    if "val" not in d:
        raise DeserializeException("Invalid dictionary, missing val key")
    typ = d["__type"]
    val = d["val"]
    if typ in {"bool", "int", "float", "str", "None"}:
        return val
    elif typ == "dict":
        return {deserialize(k): deserialize(v) for k, v in val}
    elif typ == "list":
        return [deserialize(v) for v in val]
    elif typ == "set":
        return {deserialize(v) for v in val}
    elif typ == "np.ndarray":
        return pickle.loads(codecs.decode(val.encode("utf-8"), 'base64'))
    elif typ in CLASS_REGISTER:
        cls = CLASS_REGISTER[typ]
        try:
            instance = cls()
        except TypeError as e:
            raise DeserializeException(f"Could not instanciate type {typ}, constructor should not require arguments") from e
        for k, v in val.items():
            try:
                setattr(instance, k, deserialize(v))
            except AttributeError:
                if hasattr(instance, "_" + k):
                    setattr(instance, "_" + k, deserialize(v))
                else:
                    raise DeserializeException(f"Error creating attribute {k} for class {typ}")
        return instance
    elif typ in ENUM_REGISTER:
        cls = ENUM_REGISTER[typ]
        return cls(val)
    else:
        raise DeserializeException(f"Unknown type: {typ}")
        

