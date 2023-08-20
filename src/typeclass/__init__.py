from abc import abstractmethod

from .typeclass import Typeclass


__version__ = "0.1.2"


typeclass_api = abstractmethod

del abstractmethod


__all__ = ["Typeclass", "typeclass_api"]
