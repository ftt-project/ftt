import peewee

from ftt.storage.models import Security, Portfolio
from ftt.storage.models.base import Base


class PortfolioSecurity(Base):
    portfolio = peewee.ForeignKeyField(Portfolio, backref="portfolio_securities")
    security = peewee.ForeignKeyField(Security, backref="portfolio_securities")

    class Meta:
        indexes = ((("portfolio", "security"), True),)
        table_name = "portfolio_securities"
