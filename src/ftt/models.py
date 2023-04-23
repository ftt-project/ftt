from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlRelationalTableModel, QSqlTableModel

TRACKING_SYMBOLS_SQL = """
CREATE TABLE IF NOT EXISTS tracking_symbols (
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    exchange TEXT NOT NULL,
    currency TEXT NOT NULL,
    is_enabled BOOLEAN NOT NULL
);
"""

INSERT_TRACKING_SYMBOL_SQL = """
INSERT INTO tracking_symbols (symbol, exchange, currency, is_enabled) VALUES (?, ?, ?, ?)
"""

EQUITIES_SQL = """
CREATE TABLE IF NOT EXISTS equities (
    id INTEGER PRIMARY KEY,
    symbol TEXT,
    short_name TEXT,
    long_name TEXT,
    summary TEXT,
    currency TEXT,
    sector TEXT,
    industry TEXT,
    exchange TEXT,
    market TEXT,
    country TEXT,
    state TEXT,
    city TEXT,
    zipcode TEXT,
    website TEXT,
    market_cap TEXT
);
"""

EQUITIES_SYMBOL_EXCHANGE_INDEX_SQL = """
CREATE UNIQUE INDEX IF NOT EXISTS equities_symbol_exchange_idx ON equities (symbol, exchange);
"""

INSERT_EQUITIES_SQL = """
INSERT INTO equities (symbol, short_name, long_name, summary, currency, sector, industry, exchange, market, country, state, city, zipcode, website, market_cap)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(symbol, exchange) DO NOTHING;
"""


def check(func, *args):
    if not func(*args):
        raise ValueError(func.__self__.lastError())


def get_db(name="default"):
    if QSqlDatabase.contains(name):
        return QSqlDatabase.database(name)
    else:
        db = QSqlDatabase.addDatabase("QSQLITE", name)
        db.setDatabaseName("ftt.sqlite")
        # db.setDatabaseName(":memory:")
        check(db.open)
        return db


def add_tracking_ticker(symbol, exchange, currency, is_enabled, db=get_db()):
    q = QSqlQuery(db)
    check(q.prepare, INSERT_TRACKING_SYMBOL_SQL)
    q.addBindValue(symbol)
    q.addBindValue(exchange)
    q.addBindValue(currency)
    q.addBindValue(is_enabled)
    check(q.exec)


def add_equity(symbol, short_name, long_name, summary, currency, sector, industry, exchange, market, country, state, city, zipcode, website, market_cap, db=get_db()):
    q = QSqlQuery(db)
    check(q.prepare, INSERT_EQUITIES_SQL)
    q.addBindValue(symbol)
    q.addBindValue(short_name)
    q.addBindValue(long_name)
    q.addBindValue(summary)
    q.addBindValue(currency)
    q.addBindValue(sector)
    q.addBindValue(industry)
    q.addBindValue(exchange)
    q.addBindValue(market)
    q.addBindValue(country)
    q.addBindValue(state)
    q.addBindValue(city)
    q.addBindValue(zipcode)
    q.addBindValue(website)
    q.addBindValue(market_cap)
    check(q.exec)


_tickers_model_instance = None


_equity_model_instance = None


def tracking_symbols_model_instance():
    global _tickers_model_instance
    if _tickers_model_instance is not None:
        return _tickers_model_instance

    _tickers_model_instance = QSqlRelationalTableModel(None, db=get_db())
    _tickers_model_instance.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
    _tickers_model_instance.setTable("tracking_symbols")

    _tickers_model_instance.setHeaderData(_tickers_model_instance.fieldIndex("symbol"), Qt.Horizontal, "Symbol")
    _tickers_model_instance.setHeaderData(_tickers_model_instance.fieldIndex("exchange"), Qt.Horizontal, "Exchange")
    _tickers_model_instance.setHeaderData(_tickers_model_instance.fieldIndex("currency"), Qt.Horizontal, "Currency")

    return _tickers_model_instance


def equity_model_instance():
    global _equity_model_instance
    if _equity_model_instance is not None:
        return _equity_model_instance

    model = QSqlRelationalTableModel(None, db=get_db())
    model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
    model.setTable("equities")

    model.setHeaderData(model.fieldIndex("symbol"), Qt.Horizontal, "Symbol")
    model.setHeaderData(model.fieldIndex("short_name"), Qt.Horizontal, "Short Name")
    model.setHeaderData(model.fieldIndex("long_name"), Qt.Horizontal, "Long Name")
    model.setHeaderData(model.fieldIndex("summary"), Qt.Horizontal, "Summary")
    model.setHeaderData(model.fieldIndex("currency"), Qt.Horizontal, "Currency")
    model.setHeaderData(model.fieldIndex("sector"), Qt.Horizontal, "Sector")
    model.setHeaderData(model.fieldIndex("industry"), Qt.Horizontal, "Industry")
    model.setHeaderData(model.fieldIndex("exchange"), Qt.Horizontal, "Exchange")
    model.setHeaderData(model.fieldIndex("market"), Qt.Horizontal, "Market")
    model.setHeaderData(model.fieldIndex("country"), Qt.Horizontal, "Country")
    model.setHeaderData(model.fieldIndex("state"), Qt.Horizontal, "State")
    model.setHeaderData(model.fieldIndex("city"), Qt.Horizontal, "City")
    model.setHeaderData(model.fieldIndex("zipcode"), Qt.Horizontal, "Zipcode")
    model.setHeaderData(model.fieldIndex("website"), Qt.Horizontal, "Website")
    model.setHeaderData(model.fieldIndex("market_cap"), Qt.Horizontal, "Market Cap")

    return model


def init_db(name="default"):
    db = get_db(name)

    q = QSqlQuery(db)
    check(q.exec, TRACKING_SYMBOLS_SQL)
    check(q.exec, EQUITIES_SQL)
    check(q.exec, EQUITIES_SYMBOL_EXCHANGE_INDEX_SQL)

    add_tracking_ticker("AAPL", "NASDAQ", "USD", True)
    add_tracking_ticker("MSFT", "NASDAQ", "USD", True)
    add_tracking_ticker("GOOG", "NASDAQ", "USD", True)
    add_tracking_ticker("AMZN", "NASDAQ", "USD", True)
    add_tracking_ticker("FB", "NASDAQ", "USD", True)
    add_tracking_ticker("TSLA", "NASDAQ", "USD", True)
