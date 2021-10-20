import peewee

from trade.storage.models.base import Base
from trade.storage.models.portfolio import Portfolio


class PortfolioVersion(Base):
    portfolio = peewee.ForeignKeyField(Portfolio, backref="versions")
    version = peewee.IntegerField()
    active = peewee.BooleanField(default=False)
    expected_annual_return = peewee.FloatField(null=True)
    annual_volatility = peewee.FloatField(null=True)
    sharpe_ratio = peewee.FloatField(null=True)

    class Meta:
        indexes = ((("portfolio_id", "version"), True),)
        table_name = "portfolio_versions"
