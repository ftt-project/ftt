import peewee

from trade.db.base import Base
from trade.db import setup


class Portfolio(Base):
    name = peewee.CharField(index=True)

    class Meta:
        indexes = (
            (('name', ), True),
        )
        table_name = 'portfolios'
