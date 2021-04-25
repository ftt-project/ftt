import peewee

from trade.db import Ticker, Portfolio
from trade.db.base import Base


class Weight(Base):
    """
    TODO: add version column to remember the history of changes of the ticker weight in portfolio
    """
    ticker = peewee.ForeignKeyField(Ticker)
    portfolio = peewee.ForeignKeyField(Portfolio, backref="weights")
    position = peewee.IntegerField()
    planned_position = peewee.IntegerField()

    class Meta:
        indexes = ((("ticker", "portfolio"), True),)
        table_name = "weights"
