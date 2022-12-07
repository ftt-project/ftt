import peewee

from ftt.storage.models.base import Base
from ftt.storage.models.portfolio import Portfolio


class PortfolioVersion(Base):
    portfolio = peewee.ForeignKeyField(Portfolio, backref="versions")
    value = peewee.DecimalField(constraints=[peewee.Check("value >= 0")], default=0)
    period_start = peewee.DateTimeField(
        null=True, constraints=[peewee.Check("length(period_start) > 0")]
    )
    period_end = peewee.DateTimeField(
        null=True, constraints=[peewee.Check("length(period_end) > 0")]
    )
    interval = peewee.CharField(
        null=True, constraints=[peewee.Check("length(interval) > 0")]
    )
    version = peewee.IntegerField()
    optimization_strategy_name = peewee.CharField(null=True)
    active = peewee.BooleanField(default=False)
    expected_annual_return = peewee.FloatField(null=True)
    annual_volatility = peewee.FloatField(null=True)
    sharpe_ratio = peewee.FloatField(null=True)

    class Meta:
        indexes = ((("portfolio_id", "version"), True),)
        table_name = "portfolio_versions"
