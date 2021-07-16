from nubia import argument, command, context

from trade.cli.renderers import PortfoliosList
from trade.cli.renderers.portfolio_versions.portfolio_versions_list import (
    PortfolioVersionsList,
)
from trade.cli.renderers.portfolios.portfolio_details import PortfolioDetails
from trade.cli.renderers.weights.weights_list import WeightsList
from trade.handlers.portfolio_load_handler import PortfolioLoadHandler
from trade.handlers.portfolio_versions_list_handler import PortfolioVersionsListHandler
from trade.handlers.portfolios_list_handler import PortfoliosListHandler
from trade.handlers.weights_list_handler import WeightsListHandler


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
        PortfoliosList(ctx, result.value).render()

    @command
    @argument("portfolio_id", description="Portfolio ID", positional=True)
    def details(self, portfolio_id: int) -> None:
        """
        Display details of portfolio by its ID
        """
        # portfolio
        # versions
        # last version
        # weights x securities
        # securities list: matrix of all securities per version
        ctx = context.get_context()

        result = PortfolioLoadHandler().handle(portfolio_id=portfolio_id)
        ctx.console.print("Portfolio details")
        PortfolioDetails(ctx, result.value).render()

        result = PortfolioVersionsListHandler().handle(portfolio=result.value)
        ctx.console.print("Portfolio Versions")
        PortfolioVersionsList(ctx, result.value).render()

        portfolio_version = result.value[0]
        result = WeightsListHandler().handle(portfolio_version=portfolio_version)
        ctx.console.print(f"Portfolio Version {portfolio_version.id} weights")
        WeightsList(ctx, result.value).render()

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
