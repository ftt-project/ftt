import logging

# import os
from pathlib import Path

# from rich.logging import RichHandler


# def _log_path(file_name):
#     # This could be a system wide logging folder
#     path = os.path.dirname(os.path.abspath(__file__))
#     return os.path.join(path, "..", "logs", file_name)
#
#
# def _setup_sql_logger():
#     file_handler = logging.FileHandler(_log_path("debug.log"))
#     fmt_file = (
#         "%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
#     )
#     file_formatter = logging.Formatter(fmt_file)
#     file_handler.setLevel(logging.DEBUG)
#     file_handler.setFormatter(file_formatter)
#     return file_handler
#
#
# def _setup_app_logger():
#     shell_handler = RichHandler()
#     shell_handler.setLevel(logging.INFO)
#     fmt_shell = "%(message)s"
#     shell_formatter = logging.Formatter(fmt_shell)
#     shell_handler.setFormatter(shell_formatter)
#     return shell_handler
#
#
# logging.basicConfig(
#     level="DEBUG",
#     format="%(message)s",
#     # datefmt="[%X]",
#     handlers=[_setup_app_logger(), _setup_sql_logger()],
# )
# logger = logging.getLogger("app")
from nubia.internal.io.logger import ContextFilter  # type: ignore

logger = logging.getLogger("ftt")
logger.setLevel(logging.INFO)
logfile = Path("~/.ftt/ftt.log").expanduser()
logfile.touch(exist_ok=True)
logging_stream = open(logfile, "a")
file_handler = logging.StreamHandler(logging_stream)
file_handler.setLevel(logging.INFO)
file_handler.addFilter(ContextFilter())
fmt = "[%(asctime)-15s] [%(level)6s] [%(logger_name)s] %(thread)s%(message)s"
file_handler.setFormatter(logging.Formatter(fmt))
logger.addHandler(file_handler)
