import logging

from nubia import PluginInterface
from rich.logging import RichHandler

from ftt.cli import commands
from ftt.cli.context import Context
from ftt.cli.prompt import Prompt
from ftt.cli.status_bar import StatusBar


class Plugin(PluginInterface):
    def create_context(self):
        return Context()

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

    def get_commands(self):
        return commands.__all__

    def get_prompt_tokens(self, context):
        return Prompt()
