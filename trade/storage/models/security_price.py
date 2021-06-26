import peewee

from trade.storage.models import Base
from trade.storage.models import Security


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
