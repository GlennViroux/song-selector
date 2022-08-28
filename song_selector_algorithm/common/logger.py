"""logger"""
from song_selector_algorithm.common import StuBruSingleton
import logging
import sys


class StuBruLogger(metaclass=StuBruSingleton):
    def __init__(self):
        logger = logging.getLogger("stubru-logger")
        logger.setLevel(logging.INFO)
        logger.handler = []
        handler = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter("[{asctime}] [{levelname:8s}]: {message}", datefmt="%Y-%m-%d %H:%M:%S", style="{")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger

    def debug(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)
