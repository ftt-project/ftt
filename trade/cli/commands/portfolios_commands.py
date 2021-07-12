from nubia import argument, command, context

from trade.cli import renderers
from trade.storage.repositories.portfolios_repository import PortfoliosRepository


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
        portfolios = PortfoliosRepository.list()
        renderers.PortfoliosList(ctx, portfolios).render()

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
