import peewee

from trade.storage.models.base import Base
from trade.storage.models.portfolio import Portfolio


class PortfolioVersion(Base):
    portfolio = peewee.ForeignKeyField(Portfolio, backref="versions")
    version = peewee.IntegerField()

    class Meta:
        indexes = ((("portfolio_id", "version"), True),)
        table_name = "portfolio_versions"
