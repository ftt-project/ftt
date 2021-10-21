from typing import List

from rich.table import Table

from ftt.cli.context import Context
from ftt.cli.renderers.abstract_renderer import AbstractRenderer
from ftt.storage.models import Weight


class WeightsList(AbstractRenderer):
    def __init__(self, context: Context, list: List[Weight], title: str = "") -> None:
        self.context = context
        self.list = list
        self.title = title

    def render(self) -> None:
        table = Table(
            show_header=True,
            header_style="bold magenta",
            title=self.title,
            min_width=120,
        )
        table.add_column("ID")
        table.add_column("Symbol")
        table.add_column("Position")
        table.add_column("Planned Position")
        table.add_column("Currency")
        table.add_column("Amount")
        table.add_column("Quote Type")
        table.add_column("Short name")

        for weight in self.list:
            table.add_row(
                str(weight.id),
                weight.security.symbol,
                str(weight.position),
                str(weight.planned_position),
                weight.security.currency,
                str(weight.amount),
                weight.security.quote_type,
                weight.security.short_name,
            )

        self.context.console.print(table)
