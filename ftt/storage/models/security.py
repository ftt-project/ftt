import peewee

from ftt.storage.models.base import Base


class Security(Base):
    symbol = peewee.CharField()
    exchange = peewee.CharField(index=True)
    quote_type = peewee.CharField(index=True)
    sector = peewee.CharField(index=True, null=True)
    industry = peewee.CharField(index=True, null=True)
    country = peewee.CharField(index=True, null=True)
    currency = peewee.CharField(null=True)
    short_name = peewee.CharField()
    long_name = peewee.CharField()

    class Meta:
        indexes = ((("symbol", "exchange"), True),)
        table_name = "securities"
