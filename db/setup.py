from db.configuration import database_connection
from db.models import Ticker, TickerReturn


def setup_database():
    database_connection().create_tables([Ticker, TickerReturn])