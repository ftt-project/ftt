from rich.table import Table

from trade.cli.context import Context
from trade.cli.renderers.abstract_renderer import AbstractRenderer
from trade.storage.models import Portfolio


class PortfolioDetails(AbstractRenderer):
    def __init__(self, context: Context, portfolio: Portfolio):
        self.context = context
        self.portfolio = portfolio

    def render(self) -> None:
        table = Table(show_header=False, title="Portfolio Details", min_width=120,)
        table.add_column("Field", max_width=2)
        table.add_column("Value")

        rows = [
            ("[bold magenta]ID", str(self.portfolio.id)),
            ("[bold magenta]Name", f"[bold cyan]{self.portfolio.name}"),
            ("[bold magenta]Amount", str(self.portfolio.amount)),
            ("[bold magenta]Period start", str(self.portfolio.period_start)),
            ("[bold magenta]Period end", str(self.portfolio.period_end)),
            ("[bold magenta]Interval", self.portfolio.interval),
        ]
        for name, value in rows:
            table.add_row(name, value)

        self.context.console.print(table)
