import sys

from nubia import Nubia, Options

from trade.cli import commands
from trade.cli.plugin import Plugin


class Shell:
    @staticmethod
    def initialize_and_run():
        shell = Nubia(
            name="fam",
            command_pkgs=[commands],
            plugin=Plugin(),
            options=Options(
                persistent_history=False, auto_execute_single_suggestions=False
            ),
        )
        sys.exit(shell.run())
