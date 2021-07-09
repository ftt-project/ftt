from datetime import datetime

from nubia import command, context
from rich.table import Table

from trade.handlers.portfolio_associate_securities_hanlder import (
    PortfolioAssociateSecuritiesHandler,
)
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

    Storage.initialize_database(application_name="ftt", environment="dev")

    result = PortfolioCreationHandler().handle(name="S&P companies", amount=10000)
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

    ctx.console.print("Loading securities information", style="bold green")

    for symbol in ["AAPL", "SHOP", "MSFT"]:
        ctx.console.print(f"- {symbol}")
    today = datetime.today()
    result = SecuritiesLoadingHandler().handle(
        securities=["AAPL", "SHOP", "MSFT"],
        start_period=datetime(today.year, 1, 1),
        end_period=datetime(today.year, today.month, today.day),
        interval="1d",
    )
    _ = result.value

    ctx.console.print(
        "Portfolio successfully associated with securities", style="bold green"
    )
    _ = PortfolioAssociateSecuritiesHandler().handle(
        securities=["AAPL", "SHOP", "MSFT"], portfolio_version=portfolio.versions[0]
    )

    ctx.console.print("Calculating weights", style="bold green")
    result = WeightsCalculationHandler().handle(
        portfolio=portfolio,
        portfolio_version=portfolio.versions[0],
        start_period=datetime(today.year, 1, 1),
        end_period=datetime(today.year, today.month, today.day),
        interval="1d",
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
