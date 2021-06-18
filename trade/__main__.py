import sys

import trade.cli.commands
from nubia import context, PluginInterface, Nubia, Options


ctx = context.get_context()


class NubiaExamplePlugin(PluginInterface):
    pass


shell = Nubia(
    name="nubia_example",
    command_pkgs=[trade.commands],
    plugin=NubiaExamplePlugin(),
    options=Options(persistent_history=False, auto_execute_single_suggestions=False),
)
sys.exit(shell.run())
