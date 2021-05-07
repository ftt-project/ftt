from datetime import datetime

import peewee

from trade.models import Ticker, PortfolioVersion
from trade.models import Base


class Weight(Base):
    """
    TODO: add version column to remember the history of changes of the ticker weight in portfolio
    """
    ticker = peewee.ForeignKeyField(Ticker)
    portfolio_version = peewee.ForeignKeyField(PortfolioVersion, backref="weights")
    position = peewee.IntegerField()
    planned_position = peewee.IntegerField()

    class Meta:
        indexes = ((("ticker", "portfolio_version"), True),)
        table_name = "weights"
