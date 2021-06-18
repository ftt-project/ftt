from nubia import command, argument
from rich.console import Console
from rich.table import Table

from trade.storage.repositories import PortfoliosRepository


@command
def portfolios() -> None:
    """
    List existing portfolios
    """
    portfolios = PortfoliosRepository.list()
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Amount")
    for portfolio in portfolios:
        table.add_row(f"{portfolio.id}", portfolio.name, f"{portfolio.amount}")

    console.print(table)


@command
class Portfolio:
    """
    Portfolio managing
    """

    @command("import")
    @argument("file", description="YAML file to import", positional=True)
    def import_from_file(self, file: str):
        """
        Import from yml file
        """
        from rich.console import Console

        console = Console()
        console.log("Successfully imported")

    @command
    def versions(self):
        """
        Print available versions of portfolio
        """
        pass
