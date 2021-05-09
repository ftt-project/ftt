import peewee

from trade.models import Base, Ticker, PortfolioVersion


class Order(Base):
    ticker = peewee.ForeignKeyField(Ticker, backref="orders")
    portfolio_version = peewee.ForeignKeyField(PortfolioVersion, backref="orders")
    status = peewee.CharField()
    executed_at = peewee.DateTimeField(null=True)
    desired_price = peewee.DecimalField()
    execution_price = peewee.DecimalField(null=True)

    class Meta:
        table_name = "orders"
