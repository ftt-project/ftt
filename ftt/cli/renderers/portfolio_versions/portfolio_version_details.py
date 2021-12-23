from rich.table import Table

from ftt.cli.context import Context
from ftt.cli.renderers.abstract_renderer import AbstractRenderer
from ftt.storage.models import PortfolioVersion


class PortfolioVersionBriefDetails(AbstractRenderer):
    def __init__(self, context: Context, portfolio_version: PortfolioVersion):
        self.context = context
        self.portfolio_version = portfolio_version

    def render(self) -> None:
        table = Table(
            show_header=False,
            title="Portfolio Version Details",
            min_width=120,
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


class PortfolioVersionDetails(AbstractRenderer):
    def __init__(self, context: Context, portfolio_version: PortfolioVersion):
        self.context = context
        self.portfolio_version = portfolio_version

    def render(self) -> None:
        table = Table(
            show_header=False,
            title="Portfolio Version Details",
            min_width=120,
        )
        table.add_column("Field", max_width=4)
        table.add_column("Value")

        rows = [
            ("[bold magenta]ID", str(self.portfolio_version.id)),
            ("[bold magenta]Portfolio ID", str(self.portfolio_version.portfolio_id)),
            ("[bold magenta]Account value", str(self.portfolio_version.value)),
            ("[bold magenta]Period start", str(self.portfolio_version.period_start)),
            ("[bold magenta]Period end", str(self.portfolio_version.period_end)),
            ("[bold magenta]Interval", self.portfolio_version.interval),
            (
                "[bold magenta]Active",
                "[bold cyan]Yes" if self.portfolio_version.active else "No",
            ),
            (
                "[bold magenta]Expected Annual Return",
                str(self.portfolio_version.expected_annual_return),
            ),
            (
                "[bold magenta]Annual Volatility",
                str(self.portfolio_version.annual_volatility),
            ),
            ("[bold magenta]Sharpe Ratio", str(self.portfolio_version.sharpe_ratio)),
        ]

        for name, value in rows:
            table.add_row(name, value)

        self.context.console.print(table)
