import peewee
from trade.db.base import Base


class Portfolio(Base):
    name = peewee.CharField(index=True)

    class Meta:
        indexes = (
            (('name', ), True),
        )
        table_name = 'portfolios'
