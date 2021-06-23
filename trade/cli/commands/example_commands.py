from nubia import command, context
from rich.table import Table


from trade.handlers.portfolio_creation_handler import PortfolioCreationHandler


@command
def example():
    """
    Create example portfolio with weights
    1. [x] create portfolio
    2. [x] portfolio version
    3. [ ] load securities
    4. [ ] create weights
    5. [ ] calculate weights
    6. [ ] show portfolio stats
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
    table.add_row(
        str(portfolio.id),
        portfolio.name,
        str(portfolio.amount),
        str(portfolio.created_at)
    )
    ctx.console.print(table)

    ctx.console.print("Loading securities information", style="bold green")

    result = SecuritiesLoadingHandler().handle(
        securities=["AAPL", "SHOP", "MSFT"],
        period_from='',
        period_to='',
        interval='1d'
    )
    securities = result.value

