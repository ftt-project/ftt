from rich.table import Table

from trade.cli.context import Context
from trade.cli.renderers.abstract_renderer import AbstractRenderer
from trade.storage.models import Portfolio


class PortfolioDetails(AbstractRenderer):
    def __init__(self, context: Context, portfolio: Portfolio):
        self.context = context
        self.portfolio = portfolio

    def render(self) -> None:
        table = Table(
            show_header=True,
            header_style="bold magenta",
            title="Portfolio Details",
            min_width=120,
        )
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Amount")

        table.add_row(
            str(self.portfolio.id), self.portfolio.name, str(self.portfolio.amount)
        )

        self.context.console.print(table)
