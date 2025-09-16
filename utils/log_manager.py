"""
Log_manager.py
This module provides a logging manager that sets up and configures loggers for the application.

"""

import logging
import os
from threading import Lock

class LogManager:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """Singleton pattern to ensure only one instance of LogManager exists."""
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(LogManager, cls).__new__(cls)
                    cls._instance._logger = None
        return cls._instance

    def get_logger(
        self,
        name: str = "LeagueProject",
        log_file: str = "league_project.log",
        level: int = logging.INFO,
        log_dir: str = "logs"
    ) -> logging.Logger:
        """Sets up and returns a logger instance."""
        if self._logger:
            return self._logger

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_path = os.path.join(log_dir, log_file)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.propagate = False

        # File handler
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        )
        file_handler.setFormatter(file_formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_formatter = logging.Formatter(
            '[%(levelname)s] %(name)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)

        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        self._logger = logger
        return self._logger