from datetime import datetime

from nubia import command, context
from rich.table import Table


from trade.handlers.portfolio_creation_handler import PortfolioCreationHandler
from trade.handlers.securities_loading_handler import SecuritiesLoadingHandler
from trade.handlers.weights_calculation_handler import WeightsCalculationHandler


@command
def example():
    """
    Create example portfolio with weights
    1. [x] create portfolio
    2. [x] portfolio version
    3. [x] load securities
    4. [ ] create weights
    5. [ ] calculate weights
    6. [ ] show portfolio stats

    TODO: load from yaml file
    """
    ctx = context.get_context()

    result = PortfolioCreationHandler().handle(
        name='S&P companies',
        amount=10000
    )
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
        str(portfolio.created_at)
    )
    ctx.console.print(table)

    ctx.console.print("Loading securities information", style="bold green")

    today = datetime.today()
    result = SecuritiesLoadingHandler().handle(
        securities=["AAPL", "SHOP", "MSFT"],
        period_from=datetime(today.year, 1, 1),
        period_to=datetime(today.year, today.month, today.day),
        interval='1d'
    )
    securities = result.value

    # print loaded securities and stats

    result = WeightsCalculationHandler().handle(
        portfolio=portfolio,
        persist=True
    )
    weights = result.value

