from nubia import context
from nubia import exceptions
from nubia import eventbus

from rich.console import Console

from trade.storage import Storage


class Context(context.Context):
    def on_connected(self, *args, **kwargs):
        environment = "development"
        Storage.initialize_database(application_name="fams", environment=environment)

        self.console = Console()


    def on_cli(self, cmd, args):
        # dispatch the on connected message
        self.verbose = args.verbose
        self.registry.dispatch_message(eventbus.Message.CONNECTED)

    def on_interactive(self, args):
        self.verbose = args.verbose
        ret = self._registry.find_command("connect").run_cli(args)
        if ret:
            raise exceptions.CommandError("Failed starting interactive mode")
        # dispatch the on connected message
        self.registry.dispatch_message(eventbus.Message.CONNECTED)
