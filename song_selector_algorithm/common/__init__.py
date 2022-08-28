"""common classes and functions"""

from typing import Dict


class StuBruSingleton(type):
    """Superclass to have only one instance"""

    _instances = {}  # type: Dict[StuBruSingleton, StuBruSingleton]

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(StuBruSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
