import peewee

from ftt.storage.models.base import Base
from ftt.storage.models.security import Security


class SecurityPrice(Base):
    security = peewee.ForeignKeyField(Security, backref="prices")
    datetime = peewee.DateTimeField()
    open = peewee.DecimalField(max_digits=12)
    high = peewee.DecimalField(max_digits=12)
    low = peewee.DecimalField(max_digits=12)
    close = peewee.DecimalField(max_digits=12)
    volume = peewee.IntegerField()
    interval = peewee.CharField()
    change = peewee.DecimalField(max_digits=12)
    percent_change = peewee.FloatField()

    class Meta:
        indexes = ((("security", "datetime", "interval"), True),)
        table_name = "security_prices"
