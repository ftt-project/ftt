from datetime import datetime

import peewee

from ftt.storage.models.base import Base


class Portfolio(Base):
    name = peewee.CharField(index=True)
    created_at = peewee.DateTimeField(default=datetime.now)
    updated_at = peewee.DateTimeField()

    class Meta:
        indexes = ((("name",), True),)
        table_name = "portfolios"
