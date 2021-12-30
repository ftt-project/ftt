import os
import pathlib

from nubia import command, context  # type: ignore
from rich.table import Table

from ftt.handlers.portfolio_associate_securities_hanlder import (
    PortfolioAssociateSecuritiesHandler,
)
from ftt.handlers.portfolio_config_handler import PortfolioConfigHandler
from ftt.handlers.portfolio_creation_handler import PortfolioCreationHandler
from ftt.handlers.portfolio_stats_handler import PortfoliosStatsHandler
from ftt.handlers.securities_information_prices_loading_handler import (
    SecuritiesInformationPricesLoadingHandler,
)
from ftt.handlers.weights_calculation_handler import WeightsCalculationHandler
from ftt.storage import Storage
from ftt.storage.data_objects.security_dto import SecurityDTO


@command
def example():
    """
    Create example portfolio_management with weights from example config
    """
    ctx = context.get_context()

    # TODO: take env from context
    Storage.initialize_database(application_name="ftt", environment="dev")

    config = read_config()

    result = PortfolioCreationHandler().handle(
        name=config.name,
        value=config.budget,
        period_start=config.period_start,
        period_end=config.period_end,
        interval=config.interval,
    )
    portfolio = result.value

    ctx.console.print("Portfolio successfully created", style="bold green")
    table = Table(show_header=True)
    for name in ["ID", "Name", "Account value", "Created"]:
        table.add_column(name)
    # TODO: use presenter
    table.add_row(
        str(portfolio.id),
        portfolio.name,
        str(portfolio.versions[0].value),
        str(portfolio.created_at),
    )
    ctx.console.print(table)

    security_dtos = [SecurityDTO(symbol=symbol) for symbol in config.symbols]

    with ctx.console.status("[bold green]Loading securities information") as _:
        for symbol in config.symbols:
            ctx.console.print(f"- {symbol}")

        result = SecuritiesInformationPricesLoadingHandler().handle(
            portfolio_version=portfolio.versions[0],
            securities=security_dtos,
        )
        _ = result.value

    with ctx.console.status(
        "[bold green]Portfolio successfully associated with securities"
    ) as _:
        _ = PortfolioAssociateSecuritiesHandler().handle(
            securities=security_dtos, portfolio_version=portfolio.versions[0]
        )

    with ctx.console.status("[bold green]Calculating weights") as _:
        result = WeightsCalculationHandler().handle(
            portfolio_version=portfolio.versions[0],
            start_period=config.period_start,
            end_period=config.period_end,
            interval=config.interval,
            persist=True,
        )
        _ = result.value

    result = PortfoliosStatsHandler().handle(portfolio_version=portfolio.versions[0])
    portfolio_stats = result.value
    table = Table(show_header=True)
    for name in ["Symbol", "Quantity"]:
        table.add_column(name)
    for symbol, qty in portfolio_stats["planned_weights"].items():
        table.add_row(
            str(symbol),
            str(qty),
        )
    ctx.console.print(table)
    ctx.console.print("Weights are calculated and saved", style="bold green")


def read_config():
    realpath = pathlib.Path().resolve()
    path = os.path.join(realpath, "config", "example_portfolio.yml")
    result = PortfolioConfigHandler().handle(path=path)
    # TODO: handle exception
    return result.value
