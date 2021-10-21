import peewee

from ftt.storage.models.base import Base
from ftt.storage.models.portfolio_version import PortfolioVersion
from ftt.storage.models.security import Security


class Weight(Base):
    security = peewee.ForeignKeyField(Security, backref="weights")
    portfolio_version = peewee.ForeignKeyField(PortfolioVersion, backref="weights")
    position = peewee.IntegerField()
    planned_position = peewee.IntegerField()
    amount = peewee.DecimalField(constraints=[peewee.Check("amount >= 0")], default=0)
    locked_at = peewee.DateTimeField(null=True)
    locked_at_amount = peewee.DecimalField(null=True, decimal_places=2)
    peaked_value = peewee.DecimalField(null=True, decimal_places=2, default=0)

    class Meta:
        indexes = ((("security", "portfolio_version"), True),)
        table_name = "weights"
