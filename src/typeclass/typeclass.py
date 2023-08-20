from abc import ABCMeta
from extype import extension, extend_type_with


class _TypeClassMeta(ABCMeta):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)

        cls._implementations = {}
        cls._items = {
            name: item for name, item in namespace.items() if getattr(item, "__isabstractmethod__", False)
        }

    def __getitem__(cls, typ):
        if typ is Ellipsis:
            typ = cls
        elif isinstance(typ, slice):
            if typ.start is None and typ.stop is None:
                typ = cls
            else:
                raise ValueError
        if typ in cls._implementations:
            return cls._implementations[typ]
        return _ImplMeta(cls.__name__ + f"[{typ.__name__}]", (_TypeClassImplementation,), {}, typeclass=cls, original=typ)

    def __setitem__(cls, key, value):
        cls._implementations[key] = value

    def __instancecheck__(cls, instance) -> bool:
        for typ in cls._implementations:
            if isinstance(instance, typ):
                return True
        return False

    def __subclasscheck__(cls, subclass) -> bool:
        for typ in cls._implementations:
            if issubclass(subclass, typ):
                return True
        return False


class _ImplMeta(type):
    def __init__(cls, name, bases, namespace, typeclass=None, original=None):
        if typeclass and original:
            cls._typeclass = typeclass
            cls._original = original
        else:
            for name in cls._typeclass._items:
                try:
                    namespace[name] = extension(namespace[name])
                except KeyError:
                    break
            else:
                extend_type_with(cls._original, type("", (), namespace))
        super().__init__(name, bases, namespace)


class _TypeClassImplementation:
    @classmethod
    def __init_subclass__(cls, typeclass=None, original=None) -> None:
        typeclass = typeclass or cls._typeclass
        original = original or cls._original
        typeclass[original] = cls


class Typeclass(metaclass=_TypeClassMeta):
    ...
