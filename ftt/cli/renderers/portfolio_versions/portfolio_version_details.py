from rich.table import Table

from ftt.cli.context import Context
from ftt.cli.renderers.abstract_renderer import AbstractRenderer
from ftt.storage.models import PortfolioVersion


class PortfolioVersionDetails(AbstractRenderer):
    def __init__(self, context: Context, portfolio_version: PortfolioVersion):
        self.context = context
        self.portfolio_version = portfolio_version

    def render(self) -> None:
        table = Table(
            show_header=False, title="Portfolio Version Details", min_width=120,
        )
        table.add_column("Field", max_width=2)
        table.add_column("Value")

        rows = [
            ("[bold magenta]ID", str(self.portfolio_version.id)),
            ("[bold magenta]Account value", str(self.portfolio_version.value)),
            ("[bold magenta]Period start", str(self.portfolio_version.period_start)),
            ("[bold magenta]Period end", str(self.portfolio_version.period_end)),
            ("[bold magenta]Interval", self.portfolio_version.interval),
        ]

        for name, value in rows:
            table.add_row(name, value)

        self.context.console.print(table)
