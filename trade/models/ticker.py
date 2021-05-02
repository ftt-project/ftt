import peewee
import datetime

from trade.models import Base


class Ticker(Base):
    name = peewee.CharField()
    exchange = peewee.CharField(index=True)
    company_name = peewee.CharField(null=True)
    exchange_name = peewee.CharField(index=True)
    type = peewee.CharField(index=True)
    type_display = peewee.CharField()
    industry = peewee.CharField(index=True, null=True)
    currency = peewee.CharField(null=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    updated_at = peewee.DateTimeField()

    class Meta:
        indexes = ((("name", "exchange"), True),)
        table_name = "tickers"
