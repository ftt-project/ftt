import peewee

from trade.models import Ticker, PortfolioVersion
from trade.models import Base


class Weight(Base):
    ticker = peewee.ForeignKeyField(Ticker, backref="weights")
    portfolio_version = peewee.ForeignKeyField(PortfolioVersion, backref="weights")
    position = peewee.IntegerField()
    planned_position = peewee.IntegerField()
    amount = peewee.DecimalField(constraints=[peewee.Check("amount >= 0")], default=0)

    class Meta:
        indexes = ((("ticker", "portfolio_version"), True),)
        table_name = "weights"
