from datetime import datetime

import pytest

from trade.models import Weight, Ticker, Portfolio, PortfolioVersion, Order, Base, database_connection


@pytest.fixture(autouse=True, scope="function")
def transactional():
    connection = database_connection()
    with connection.atomic() as transaction:
        try:
            yield
        finally:
            transaction.rollback()

@pytest.fixture
def ticker():
    ticker = Ticker.create(
        symbol="AA.XX",
        exchange="SYD",
        company_name="Company AAXX",
        exchange_name="SYD",
        type="Stock",
        type_display="Stock",
        industry="Technologies",
        currency="USD",
        updated_at=datetime.now(),
        created_at=datetime.now()
    )
    yield ticker
    ticker.delete_instance()


@pytest.fixture
def portfolio():
    portfolio = Portfolio.create(
        name="Portfolio TEST 1",
        size=30000.0,
        updated_at=datetime.now(),
        created_at=datetime.now()
    )
    yield portfolio
    portfolio.delete_instance()


@pytest.fixture
def portfolio_version(portfolio):
    portfolio_version = PortfolioVersion.create(
        portfolio=portfolio,
        version=1,
        updated_at=datetime.now(),
        created_at=datetime.now()
    )
    yield portfolio_version
    portfolio_version.delete_instance()


@pytest.fixture
def weight(portfolio_version, ticker):
    weight = Weight.create(
        portfolio_version=portfolio_version,
        ticker=ticker,
        planned_position=10,
        position=2,
        updated_at=datetime.now(),
        created_at=datetime.now()
    )
    yield weight
    weight.delete_instance()


@pytest.fixture
def order(ticker, portfolio_version):
    order = Order.create(
        ticker=ticker,
        portfolio_version=portfolio_version,
        status="Created",
        type="buy",
        desired_price=100,
        updated_at=datetime.now(),
        created_at=datetime.now()
    )
    yield order
    order.delete_instance()
