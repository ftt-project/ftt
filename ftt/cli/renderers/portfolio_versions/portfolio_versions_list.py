from typing import List

from rich.table import Table

from ftt.cli.context import Context
from ftt.cli.renderers.abstract_renderer import AbstractRenderer
from ftt.storage.models import PortfolioVersion


class PortfolioVersionsList(AbstractRenderer):
    def __init__(self, context: Context, portfolio_version: List[PortfolioVersion]):
        self.context = context
        self.portfolio_versions = portfolio_version

    def render(self) -> None:
        table = Table(
            show_header=True,
            header_style="bold magenta",
            title="Portfolio Versions",
            min_width=120,
        )
        table.add_column("ID")
        table.add_column("Version")
        table.add_column("Active")
        table.add_column("Expected Annual Return")
        table.add_column("Annual Volatility")
        table.add_column("Sharpe Ratio")

        for version in self.portfolio_versions:
            table.add_row(
                str(version.id),
                str(version.version),
                "[bold cyan]Yes" if version.active else "No",
                str(version.expected_annual_return),
                str(version.annual_volatility),
                str(version.sharpe_ratio),
            )

        self.context.console.print(table)
