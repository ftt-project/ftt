import peewee

from trade.models import Base, Portfolio


class PortfolioVersion(Base):
    portfolio = peewee.ForeignKeyField(Portfolio, backref="versions")
    version = peewee.IntegerField()

    class Meta:
        indexes = ((("portfolio_id", "version"), True),)
        table_name = "portfolio_versions"
