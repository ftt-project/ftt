from datetime import datetime

import peewee

from trade.models import Base, Ticker, PortfolioVersion


class Order(Base):
    ticker = peewee.ForeignKeyField(Ticker, backref="orders")
    portfolio_version = peewee.ForeignKeyField(PortfolioVersion, backref="orders")
    executed_at = peewee.DateTimeField()
    desired_price = peewee.DecimalField()
    execution_price = peewee.DecimalField()

    class Meta:
        table_name = "orders"
