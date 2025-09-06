import threading
from abc import ABCMeta


class Singleton(ABCMeta):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    def reset_instance(cls):
        cls._instances.pop(cls, None)