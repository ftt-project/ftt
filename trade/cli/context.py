from nubia import context, eventbus, exceptions
from rich.console import Console

from trade.storage import Storage


class Context(context.Context):
    def on_connected(self, *args, **kwargs):
        # TODO take environment from outside
        environment = "dev"
        Storage.initialize_database(application_name="ftt", environment=environment)

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
