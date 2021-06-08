"""
Main entry point

Author: Artem Melnykov
Contributor: Ihor Mokriienko

Usage:

    trade
    trade runner account


"""
__version__ = '0.1'
__copyright__ = '2021'

from typing import List

from nubia import argument, command, context
from rich.console import Console
from rich.table import Table

from trade.models import Portfolio
from trade.repositories import PortfoliosRepository


@command
def portfolios() -> List[Portfolio]:
    """
    List existing portfolios
    """
    portfolios = PortfoliosRepository.list()
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Amount")
    for portfolio in portfolios:
        table.add_row(portfolio.id, portfolio.name, portfolio.amount)

    console.print(table)