import logging

from pathlib import Path
from typing import Final, Optional, Any

from nubia.internal.io.logger import ContextFilter  # type: ignore


class Logger:
    FMT: Final[
        str
    ] = "[%(asctime)-15s] [%(level)6s] [%(logger_name)s] %(thread)s%(message)s"
    LOGFILE: Final[str] = "ftt.log"

    _instance: Optional[Any] = None
    _environment: Optional[str] = None
    _root_path: Optional[Path] = None
    _name: Optional[str] = None
    _logger: Optional[logging.Logger] = None

    def __new__(
        cls,
        name: str = "ftt",
        environment: str = "development",
        root_path: Path = None,
    ):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)

            cls._instance._environment = environment
            cls._instance._root_path = root_path
            cls._instance._name = name

            logger = logging.getLogger(name)
            logger.setLevel(logging.INFO)
            cls._instance._logger = logger

            logfile = cls._instance._root_path.joinpath(cls.LOGFILE).expanduser()  # type: ignore
            logfile.touch(exist_ok=True)
            logging_stream = open(logfile, "a")

            file_handler = logging.StreamHandler(logging_stream)
            file_handler.setLevel(logging.INFO)
            file_handler.addFilter(ContextFilter())
            file_handler.setFormatter(logging.Formatter(cls.FMT))

            cls._instance._logger.addHandler(file_handler)

        return cls._instance

    @property
    def logger(self) -> logging.Logger:
        if self._logger is None:
            raise RuntimeError("Logger not initialized")
        return self._logger

    @classmethod
    def debug(cls, msg: str):
        cls._instance.logger.debug(msg)  # type: ignore

    @classmethod
    def exception(cls, msg: str):
        cls._instance.logger.exception(msg)  # type: ignore
        cls._instance.logger.debug(msg)  # type: ignore

    @classmethod
    def info(cls, msg: str):
        cls._instance.logger.info(msg)  # type: ignore

    @classmethod
    def warning(cls, msg: str):
        cls._instance.logger.warning(msg)  # type: ignore

    @classmethod
    def error(cls, msg: str):
        cls._instance.logger.error(msg)  # type: ignore

    @classmethod
    def critical(cls, msg: str):
        cls._instance.logger.critical(msg)  # type: ignore
