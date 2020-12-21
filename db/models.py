import peewee
from playhouse.postgres_ext import HStoreField
from . import configuration
import datetime


class Ticker(configuration.BaseModel):
    ticker = peewee.CharField()
    company_name = peewee.CharField()
    exchange = peewee.CharField(index=True)
    exchange_name = peewee.CharField(index=True)
    type = peewee.CharField(index=True)
    type_display = peewee.CharField()
    industry = peewee.CharField(index=True, null=True)
    currency = peewee.CharField(null=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    updated_at = peewee.DateTimeField()

    class Meta:
        indexes = (
            (('ticker', 'exchange'), True),
        )
        table_name = 'tickers'


class TickerReturn(configuration.BaseModel):
    ticker = peewee.ForeignKeyField(Ticker, backref='returns')
    date = peewee.DateTimeField()
    open = peewee.DecimalField()
    high = peewee.DecimalField()
    low = peewee.DecimalField()
    close = peewee.DecimalField()
    volume = peewee.IntegerField()
    interval = peewee.CharField()
    percent_change = peewee.FloatField()

    class Meta:
        indexes = (
            (('ticker', 'interval'), True),
        )
        table_name = 'ticker_returns'
