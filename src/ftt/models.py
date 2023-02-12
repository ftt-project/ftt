from PySide6.QtSql import QSqlDatabase, QSqlQuery


TICKERS_SQL = """
CREATE TABLE tickers (
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    exchange TEXT NOT NULL,
    currency TEXT NOT NULL,
    is_enabled BOOLEAN NOT NULL
);
"""

INSERT_TICKER_SQL = """
INSERT INTO tickers (symbol, exchange, currency, is_enabled) VALUES (?, ?, ?, ?)
"""


def check(func, *args):
    if not func(*args):
        raise ValueError(func.__self__.lastError())


def add_ticker(symbol, exchange, currency, is_enabled):
    q = QSqlQuery()
    check(q.prepare, INSERT_TICKER_SQL)
    q.addBindValue(symbol)
    q.addBindValue(exchange)
    q.addBindValue(currency)
    q.addBindValue(is_enabled)
    q.exec()


def init_db():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(":memory:")

    check(db.open)

    q = QSqlQuery()
    check(q.exec, TICKERS_SQL)

    add_ticker("AAPL", "NASDAQ", "USD", True)
    add_ticker("MSFT", "NASDAQ", "USD", True)
    add_ticker("GOOG", "NASDAQ", "USD", True)
    add_ticker("AMZN", "NASDAQ", "USD", True)
    add_ticker("FB", "NASDAQ", "USD", True)
    add_ticker("TSLA", "NASDAQ", "USD", True)
