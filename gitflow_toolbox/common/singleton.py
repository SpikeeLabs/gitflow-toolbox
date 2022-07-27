class Singleton(type):
    """Metaclass to use if you need a singleton on your class
    Example:
        >>> from unyc.python_utils.utils import Singleton
        ...
        >>> class MySingleton(metaclass=Singleton)
        ...    pass
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
