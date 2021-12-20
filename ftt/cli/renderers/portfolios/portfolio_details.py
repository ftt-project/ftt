from rich.table import Table

from ftt.cli.context import Context
from ftt.cli.renderers.abstract_renderer import AbstractRenderer
from ftt.storage.models import Portfolio


class PortfolioDetails(AbstractRenderer):
    def __init__(self, context: Context, portfolio: Portfolio):
        self.context = context
        self.portfolio = portfolio

    def render(self) -> None:
        table = Table(
            show_header=False,
            title="Portfolio Details",
            min_width=120,
        )
        table.add_column("Field", max_width=2)
        table.add_column("Value")

        rows = [
            ("[bold magenta]ID", str(self.portfolio.id)),
            ("[bold magenta]Name", f"[bold cyan]{self.portfolio.name}"),
        ]
        for name, value in rows:
            table.add_row(name, value)

        self.context.console.print(table)
