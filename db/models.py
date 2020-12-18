import peewee
from . import configuration
import datetime


class Ticker(configuration.BaseModel):
    ticker = peewee.CharField()
    company_name = peewee.TextField(null=True)
    exchange = peewee.CharField()
    created_at = peewee.DateTimeField(default=datetime.datetime.now)