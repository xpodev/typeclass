# Typeclass

Welcome to the `typeclass` Python package! This library allows you to externally implement interface
in Python, and use classes as if they implemented the typeclass themselves.

Let's see an example usage:

> Suppose we want to create an extensible object model which we need to add support for serializing to
JSON format. One option that we have is to create a complex serialization function which will iterate
over a set of attributes and recursively serialize them. Another approach is to let each class implement
it itself.
> 
> However, we don't always want to include the serialization code inside the class, or we don't always 
> have access to the type's body. This is where typeclasses come in. Not only do they allow us to extend
> existing types, but they also allow us to extend types that we don't own. Moreover, they allow us to
> add types to an hierarchy without modifying the type itself.


This is how we would defint the `JSONSerializable` typeclass:

```python
from typeclass import Typeclass, typeclass_api

class JSONSerializable(Typeclass):
    @typeclass_api
    def serialize(self) -> dict:
        raise NotImplementedError
```

> Note that we marked the `serialize` method as abstract. This is because only
abstract methods are added as methods to the typeclass. If we don't mark it as abstract, it will not be added to implemented types afterwards.

Now, let's define a class that implements the typeclass.
We can use the `Typeclass[:]` or `Typeclass[...]` syntax to indicate that the class implements the typeclass.

```python
class Person(JSONSerializable[:]):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "age": self.age
        }
```

This is how we'll implement the typeclass on an existing type, such as `dict`:

```python
class _(JSONSerializable[dict]):
    def serialize(self) -> dict:
        return {
            key.serialize(): value.serialize()
            for key, value in self.items()
        }
```


Then, we can directly use these methods:
```python
>>> Person("John", 20).serialize()
{"name": "John", "age": 20}

>>> isinstance(Person("John", 20), JSONSerializable)
True
```
