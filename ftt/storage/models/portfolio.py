from datetime import datetime

import peewee

from ftt.storage.models.base import Base


class Portfolio(Base):
    name = peewee.CharField(
        index=True, null=False, constraints=[peewee.Check("length(name) > 0")]
    )
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
    created_at = peewee.DateTimeField(default=datetime.now)
    updated_at = peewee.DateTimeField()

    @property
    def securities(self):
        from ftt.storage.models import PortfolioSecurity
        from ftt.storage.models import Security
        return (Security.select().
                join(PortfolioSecurity).
                join(Portfolio).
                where(PortfolioSecurity.portfolio == self))

    class Meta:
        indexes = ((("name",), True),)
        table_name = "portfolios"
