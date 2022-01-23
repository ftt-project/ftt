from nubia import context, eventbus, exceptions  # type: ignore
from rich.console import Console


class Context(context.Context):
    def __init__(self):
        super().__init__()
        self._environment = None
        self.console = Console()

    def on_connected(self, *args, **kwargs):
        pass

    def set_environment(self, environment):
        with self._lock:
            self._environment = environment

    @property
    def environment(self):
        with self._lock:
            return self._environment

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
