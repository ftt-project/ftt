from nubia import context, eventbus, exceptions  # type: ignore
from rich.console import Console

from ftt.cli.handlers.database_structure_initalization_handler import DatabaseStructureInitializationHandler


class Context(context.Context):
    def __init__(self):
        super().__init__()
        self._environment = None
        self.console = Console()

    def on_connected(self, *args, **kwargs):
        # from ftt.cli.application import APPLICATION_NAME
        # result = DatabaseStructureInitializationHandler().handle(environment=self.environment, application_name=APPLICATION_NAME)
        # if result.is_err():
        #     self.console.print(result.unwrap_err())
        #     exit(1)
        #
        # if result.value.first_run:
        #     self.console.print("First run detected, running database structure initialization")
        #     pass

        # print version
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
