from typing import List

from rich.table import Table

from ftt.cli.context import Context
from ftt.cli.renderers.abstract_renderer import AbstractRenderer
from ftt.storage.models import Portfolio


class PortfoliosList(AbstractRenderer):
    def __init__(self, context: Context, list: List[Portfolio]) -> None:
        self.context = context
        self.list = list

    def render(self) -> None:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID")
        table.add_column("Name")
        for portfolio in self.list:
            table.add_row(f"{portfolio.id}", portfolio.name)

        self.context.console.print(table)
