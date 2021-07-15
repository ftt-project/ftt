from nubia import argument, command, context

from trade.cli import renderers
from trade.handlers.portfolios_list_handler import PortfoliosListHandler


@command("portfolios")
class PortfoliosCommands:
    """
    Portfolio managing
    """

    @command
    def list(self) -> None:
        """
        List existing portfolios
        """
        ctx = context.get_context()
        result = PortfoliosListHandler().handle()
        renderers.PortfoliosList(ctx, result.value).render()

    @command
    def details(self) -> None:
        ctx = context.get_context()

        # portfolio
        # versions
        # last version
        # weights x securities
        # securities list: matrix of all securities per version
        pass

    @command("import")
    @argument("file", description="YAML file to import", positional=True)
    def import_from_file(self, file: str) -> None:
        """
        Import from yml file
        """
        from rich.console import Console

        console = Console()
        console.log("Successfully imported")

    @command
    def versions(self) -> None:
        """
        Print available versions of portfolio
        """
        pass
