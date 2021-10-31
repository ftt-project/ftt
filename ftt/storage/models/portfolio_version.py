import peewee

from ftt.storage.models.base import Base
from ftt.storage.models.portfolio import Portfolio


class PortfolioVersion(Base):
    portfolio = peewee.ForeignKeyField(Portfolio, backref="versions")
    amount = peewee.DecimalField(constraints=[peewee.Check("amount >= 0")], default=0)
    period_start = peewee.DateTimeField(null=True)
    period_end = peewee.DateTimeField(null=True)
    interval = peewee.CharField(null=True)
    version = peewee.IntegerField()
    active = peewee.BooleanField(default=False)
    expected_annual_return = peewee.FloatField(null=True)
    annual_volatility = peewee.FloatField(null=True)
    sharpe_ratio = peewee.FloatField(null=True)

    class Meta:
        indexes = ((("portfolio_id", "version"), True),)
        table_name = "portfolio_versions"
