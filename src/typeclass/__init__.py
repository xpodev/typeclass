from abc import abstractmethod

from .typeclass import Typeclass


typeclass_api = abstractmethod

del abstractmethod


__all__ = ["Typeclass", "typeclass_api"]
