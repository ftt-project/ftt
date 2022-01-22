import logging
from typing import Optional

from nubia import PluginInterface  # type: ignore
from rich.logging import RichHandler

from ftt.cli.context import Context
from ftt.cli.prompt import Prompt
from ftt.cli.status_bar import StatusBar


class Plugin(PluginInterface):
    def __init__(self):
        self.context = None
        self.environment: Optional[str] = None

    def create_context(self):
        self.context = Context()
        return self.context

    def create_usage_logger(self, context):
        shell_handler = RichHandler()
        shell_handler.setLevel(logging.INFO)
        fmt_shell = "%(message)s"
        shell_formatter = logging.Formatter(fmt_shell)
        shell_handler.setFormatter(shell_formatter)
        return None
        # TODO use canonical logger
        return shell_handler

    def get_status_bar(self, context):
        return StatusBar(context)

    def get_prompt_tokens(self, context):
        return Prompt()

    def get_opts_parser(self, add_help=True):
        opts_parser = super().get_opts_parser(add_help=add_help)
        opts_parser.add_argument(
            "--version",
            required=False,
            type=int,
            default=None,
            help="Print version of the program and exit.",
        )
        opts_parser.add_argument(
            "--prod",
            action="store_true",
            default=True,
            help="Run application in production mode. Create and use configuration file and database in user folder."
        )
        opts_parser.add_argument(
            "--dev",
            action="store_true",
            default=False,
            help="Run application locally. Create and use configuration file and database in current directory. "
            "Used for development purposes."
        )
        opts_parser.add_argument(
            "--test",
            action="store_true",
            default=False,
            help="Run application locally. Create configuration file and database in current directory. "
            "Used for testing."
        )
        return opts_parser
