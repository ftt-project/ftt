import peewee
import datetime

from trade.storage.models import Base


class Ticker(Base):
    symbol = peewee.CharField()
    exchange = peewee.CharField(index=True)
    company_name = peewee.CharField(null=True)
    type = peewee.CharField(index=True)
    industry = peewee.CharField(index=True, null=True)
    currency = peewee.CharField(null=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    updated_at = peewee.DateTimeField()

    class Meta:
        indexes = ((("symbol", "exchange"), True),)
        table_name = "tickers"
