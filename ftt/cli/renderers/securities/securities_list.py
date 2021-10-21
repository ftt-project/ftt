from typing import List

from rich.table import Table

from ftt.cli.context import Context
from ftt.cli.renderers.abstract_renderer import AbstractRenderer
from ftt.storage.models import Security


class SecuritiesList(AbstractRenderer):
    def __init__(self, context: Context, list: List[Security]) -> None:
        self.context = context
        self.list = list

    def render(self) -> None:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID")
        table.add_column("Symbol")
        table.add_column("Exchange")
        table.add_column("Quote Type")
        table.add_column("Sector")
        table.add_column("Industry")
        table.add_column("Country")
        table.add_column("Currency")
        table.add_column("Short name")

        for security in self.list:
            table.add_row(
                str(security.id),
                security.symbol,
                security.exchange,
                security.quote_type,
                security.sector,
                security.industry,
                security.country,
                security.currency,
                security.short_name,
            )

        self.context.console.print(table)
