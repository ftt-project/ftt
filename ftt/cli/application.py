import sys

from nubia import Nubia, Options  # type: ignore
from nubia.internal import context

from ftt.cli import commands
from ftt.cli.handlers.database_structure_initalization_handler import DatabaseStructureInitializationHandler
from ftt.cli.plugin import Plugin


class ENVIRONMENT:
    production = "production"
    development = "development"
    test = "test"


APPLICATION_NAME = "ftt"


class Application:
    @staticmethod
    def initialize_and_run():
        plugin = Plugin()
        shell = Nubia(
            name=APPLICATION_NAME,
            command_pkgs=[commands],
            plugin=plugin,
            options=Options(
                persistent_history=False, auto_execute_single_suggestions=False
            ),
        )
        opts_parser = plugin.get_opts_parser()
        args, extra = opts_parser.parse_known_args(args=sys.argv)
        if args.dev:
            environment = ENVIRONMENT.development
        elif args.test:
            environment = ENVIRONMENT.test
        else:
            environment = ENVIRONMENT.production

        result = DatabaseStructureInitializationHandler().handle(
            environment=environment,
            application_name=APPLICATION_NAME
        )
        cnt = context.get_context()
        cnt.set_environment(environment)

        if result.is_err():
            cnt.console.print(result.unwrap_err())
            exit(1)

        if result.value.first_run:
            cnt.console.print("First run detected, running database structure initialization")

        sys.exit(shell.run())

