from typing import List

from rich.table import Table

from trade.cli.context import Context
from trade.storage.models import Portfolio


class PortfoliosList:
    def __init__(self, context: Context, list: List[Portfolio]) -> None:
        self.context = context
        self.list = list

    def render(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Amount")
        for portfolio in self.list:
            table.add_row(f"{portfolio.id}", portfolio.name, f"{portfolio.amount}")

        self.context.console.print(table)
