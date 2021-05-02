from datetime import datetime

import peewee

from trade.models import Ticker, Portfolio
from trade.models import Base


class Weight(Base):
    """
    TODO: add version column to remember the history of changes of the ticker weight in portfolio
    """
    ticker = peewee.ForeignKeyField(Ticker)
    portfolio = peewee.ForeignKeyField(Portfolio, backref="weights")
    position = peewee.IntegerField()
    planned_position = peewee.IntegerField()
    created_at = peewee.DateTimeField(default=datetime.now)
    updated_at = peewee.DateTimeField()

    class Meta:
        indexes = ((("ticker", "portfolio"), True),)
        table_name = "weights"
