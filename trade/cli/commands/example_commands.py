import os
import pathlib

from nubia import command, context
from rich.table import Table

from trade.handlers.portfolio_associate_securities_hanlder import (
    PortfolioAssociateSecuritiesHandler,
)
from trade.handlers.portfolio_config_handler import PortfolioConfigHandler
from trade.handlers.portfolio_creation_handler import PortfolioCreationHandler
from trade.handlers.portfolio_stats_handler import PortfoliosStatsHandler
from trade.handlers.securities_loading_handler import SecuritiesLoadingHandler
from trade.handlers.weights_calculation_handler import WeightsCalculationHandler
from trade.storage import Storage


@command
def example():
    """
    Create example portfolio with weights
    1. [x] create portfolio
    2. [x] portfolio version
    3. [x] load securities
    4. [x] create weights
    5. [x] calculate weights
    6. [x] show portfolio stats

    TODO: load from yaml file
    """
    ctx = context.get_context()

    # TODO: take env from context
    Storage.initialize_database(application_name="ftt", environment="dev")

    config = read_config()

    result = PortfolioCreationHandler().handle(name=config.name, amount=config.budget)
    portfolio = result.value

    ctx.console.print("Portfolio successfully created", style="bold green")
    table = Table(show_header=True)
    for name in ["ID", "Name", "Amount", "Created"]:
        table.add_column(name)
    # TODO: use presenter
    table.add_row(
        str(portfolio.id),
        portfolio.name,
        str(portfolio.amount),
        str(portfolio.created_at),
    )
    ctx.console.print(table)

    with ctx.console.status("[bold green]Loading securities information") as _:
        for symbol in config.symbols:
            ctx.console.print(f"- {symbol}")

        result = SecuritiesLoadingHandler().handle(
            securities=config.symbols,
            start_period=config.period_start,
            end_period=config.period_end,
            interval=config.interval,
        )
        _ = result.value

    with ctx.console.status(
        "[bold green]Portfolio successfully associated with securities"
    ) as _:
        _ = PortfolioAssociateSecuritiesHandler().handle(
            securities=config.symbols, portfolio_version=portfolio.versions[0]
        )

    with ctx.console.status("[bold green]Calculating weights") as _:
        result = WeightsCalculationHandler().handle(
            portfolio=portfolio,
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
            str(symbol), str(qty),
        )
    ctx.console.print(table)
    ctx.console.print("Weights are calculated and saved", style="bold green")


def read_config():
    realpath = pathlib.Path().resolve()
    path = os.path.join(realpath, "config", "example_portfolio.yml")
    result = PortfolioConfigHandler().handle(path=path)
    # TODO: handle exception
    return result.value
