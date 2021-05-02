import peewee

from trade.db.base import Base
from trade.db.ticker import Ticker


class TickerReturn(Base):
    ticker = peewee.ForeignKeyField(Ticker, backref="returns")
    datetime = peewee.DateTimeField()
    open = peewee.DecimalField(max_digits=12)
    high = peewee.DecimalField(max_digits=12)
    low = peewee.DecimalField(max_digits=12)
    close = peewee.DecimalField(max_digits=12)
    volume = peewee.IntegerField()
    interval = peewee.CharField()
    change = peewee.DecimalField(max_digits=12)
    percent_change = peewee.FloatField()

    class Meta:
        indexes = ((("ticker", "datetime", "interval"), True),)
        table_name = "ticker_returns"
