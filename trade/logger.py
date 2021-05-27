import logging
from rich.logging import RichHandler


def _setup_sql_logger():
    file_handler = logging.FileHandler("logs/debug.log")
    fmt_file = (
        "%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
    )
    file_formatter = logging.Formatter(fmt_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    return file_handler


def _setup_app_logger():
    shell_handler = RichHandler()
    shell_handler.setLevel(logging.INFO)
    fmt_shell = "%(message)s"
    shell_formatter = logging.Formatter(fmt_shell)
    shell_handler.setFormatter(shell_formatter)
    return shell_handler


logging.basicConfig(
    level="DEBUG",
    format="%(message)s",
    # datefmt="[%X]",
    handlers=[
        _setup_app_logger(),
        _setup_sql_logger()
    ]
)
logger = logging.getLogger("app")
