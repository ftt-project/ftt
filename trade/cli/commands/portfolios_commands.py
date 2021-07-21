from nubia import argument, command, context

from trade.cli.renderers import PortfoliosList
from trade.cli.renderers.portfolio_versions.portfolio_versions_list import (
    PortfolioVersionsList,
)
from trade.cli.renderers.portfolios.portfolio_details import PortfolioDetails
from trade.cli.renderers.weights.weights_list import WeightsList
from trade.handlers.portfolio_associate_securities_hanlder import (
    PortfolioAssociateSecuritiesHandler,
)
from trade.handlers.portfolio_config_handler import PortfolioConfigHandler
from trade.handlers.portfolio_creation_handler import PortfolioCreationHandler
from trade.handlers.portfolio_load_handler import PortfolioLoadHandler
from trade.handlers.portfolio_versions_list_handler import PortfolioVersionsListHandler
from trade.handlers.portfolios_list_handler import PortfoliosListHandler
from trade.handlers.securities_loading_handler import SecuritiesLoadingHandler
from trade.handlers.weights_list_handler import WeightsListHandler


@command("portfolios")
class PortfoliosCommands:
    """
    Portfolio managing
    TODO:
    - [ ] new-version
    - [ ] delete-version
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
        PortfolioDetails(ctx, result.value).render()

        result = PortfolioVersionsListHandler().handle(portfolio=result.value)
        PortfolioVersionsList(ctx, result.value).render()

        portfolio_version = result.value[0]
        result = WeightsListHandler().handle(portfolio_version=portfolio_version)

        WeightsList(
            ctx,
            result.value,
            f"Portfolio Version [bold cyan]#{portfolio_version.id}[/bold cyan] list of weights",
        ).render()

    @command("import")
    @argument("path", description="YAML file to import", positional=True)
    def import_from_file(self, path: str) -> None:
        """
        Import from yml file
        """
        ctx = context.get_context()
        config_result = PortfolioConfigHandler().handle(path=path)
        if config_result.is_err():
            ctx.console.print("[bold red]Failed to read config file:")
            ctx.console.print(config_result.value)
            return

        portfolio_result = PortfolioCreationHandler().handle(
            name=config_result.value.name,
            amount=config_result.value.budget,
            period_start=config_result.value.period_start,
            period_end=config_result.value.period_end,
            interval=config_result.value.interval,
        )
        if portfolio_result.is_ok():
            ctx.console.print("[green]Portfolio successfully created")
        else:
            ctx.console.print("[red]Failed to create portfolio:")
            ctx.console.print(portfolio_result.value)
            return

        with ctx.console.status("[green]Loading securities information") as _:
            for symbol in config_result.value.symbols:
                ctx.console.print(f"- {symbol}")

            securities_result = SecuritiesLoadingHandler().handle(
                securities=config_result.value.symbols,
                start_period=config_result.value.period_start,
                end_period=config_result.value.period_end,
                interval=config_result.value.interval,
            )
            if securities_result.is_ok():
                ctx.console.print("[green]Securities information successfully imported")
            else:
                ctx.console.print("[red]Failed to load securities information:")
                ctx.console.print(securities_result.value)
                return

        association_result = PortfolioAssociateSecuritiesHandler().handle(
            securities=config_result.value.symbols,
            portfolio_version=portfolio_result.value.versions[0],
        )
        if association_result.is_ok():
            ctx.console.print(
                "[green]Securities successfully associated with portfolio"
            )
        else:
            ctx.console.print("[red]Failed to associate securities with portfolio:")
            ctx.console.print(association_result.value)

    @command("use")
    @argument("portfolio_id", description="Portfolio ID", positional=True)
    def use(self, portfolio_id: int) -> None:
        """
        Assign active portfolio
        """
        ctx = context.get_context()
        ctx.portfolio_in_use = portfolio_id
        ctx.console.print(f"[green]Active portfolio #{portfolio_id}")
