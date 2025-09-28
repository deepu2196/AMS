import logging
import sys
from typing import Dict
import os.path


class Singleton(type):
    """A metaclass that creates a Singleton base class when called."""

    _instances: Dict = {}

    def __call__(cls, *args, **kwargs):
        """
        Singleton class creation.

        Args:
            *args: arguments
            **kwargs: keyword arguments

        Returns:
            Singleton: object
        """

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    

class SingletonLogger(metaclass=Singleton):
    """Logger Singleton Class."""

    def __init__(self):
        """Initialize Logger."""

        #Set up logger
        self.logger = logging.getLogger("ams_backend")
        self.logger.setLevel(logging.DEBUG)
        logs_format = logging.Formatter(
            "%(asctime)s  [%(name)s] [%(thread)d] [%(threadName)s]  [%(levelname)s] - %(message)s"
        )

        #Log to file
        log_path = "/tmp/logs"
        log_file = log_path + "/AMS.log"
        if not os.path.exists(log_path):
            os.mkdir(log_path)
            open(log_file, "w").close()
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logs_format)
        self.logger.addHandler(file_handler)

        #Log to conlose
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(logs_format)
        self.logger.addHandler(stream_handler)

    def log(self, message: str) -> None:
        """
        Record a message with level info

        Args:
            message (str): text to record
        """
        self.logger.info(message)

    def debug(self, message: str) -> None:
        """
        Record a message with level debug

        Args:
            message (str): text to record
        """
        self.logger.debug(message)

    def warning(self, message: str) -> None:
        """
        Record a message with level warning

        Args:
            message (str): text to record
        """
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """
        Record a message with level error

        Args:
            message (str): text to record
        """
        self.logger.error(message)