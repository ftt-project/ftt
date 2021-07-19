from datetime import datetime

import pytest
import backtrader as bt

from trade.piloting.strategies.sizers import WeightedSizer
from trade.storage import Storage
from trade.storage.models.order import Order
from trade.storage.models.portfolio import Portfolio
from trade.storage.models.portfolio_version import PortfolioVersion
from trade.storage.models.security import Security
from trade.storage.models.security_price import SecurityPrice
from trade.storage.models.weight import Weight


@pytest.fixture(autouse=True, scope="function")
def transactional():
    connection = Storage.get_database()
    with connection.atomic() as transaction:
        try:
            yield
        finally:
            transaction.rollback()


@pytest.fixture
def cerebro(portfolio_version, security, weight):
    def _cerebro(strategies, data):
        cerebro = bt.Cerebro(live=True, cheat_on_open=True)
        for strategy in strategies:
            if type(strategy) == tuple:
                strategy, opts = strategy
                cerebro.addstrategy(
                    strategy, portfolio_version_id=portfolio_version.id, **opts
                )
            else:
                cerebro.addstrategy(strategy, portfolio_version_id=portfolio_version.id)
        cerebro.addsizer(WeightedSizer)

        cerebro.adddata(data, name=security.symbol)

        cerebro.broker.setcash(30000.0)
        return cerebro

    return _cerebro


@pytest.fixture
def security():
    security = Security.create(
        symbol="AA.XX",
        exchange="SYD",
        company_name="Company AAXX",
        exchange_name="SYD",
        quote_type="Stock",
        type_display="Stock",
        industry="Technologies",
        sector="Technology",
        country="US",
        short_name="Short name",
        long_name="Long name",
        currency="USD",
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    try:
        yield security
    finally:
        security.delete_instance()


@pytest.fixture
def security_price(security):
    price = SecurityPrice.create(
        security=security,
        datetime=datetime.today(),
        open=100,
        high=110,
        low=90,
        close=101,
        volume=1000000,
        interval="5m",
        change=1,
        percent_change=1,
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    try:
        yield price
    finally:
        price.delete_instance()


@pytest.fixture
def portfolio():
    portfolio = Portfolio.create(
        name="Portfolio TEST 1",
        amount=30000.0,
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    try:
        yield portfolio
    finally:
        portfolio.delete_instance()


@pytest.fixture
def portfolio_version(portfolio):
    portfolio_version = PortfolioVersion.create(
        portfolio=portfolio,
        version=1,
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    try:
        yield portfolio_version
    finally:
        portfolio_version.delete_instance()


@pytest.fixture
def weight(portfolio_version, security):
    weight = Weight.create(
        portfolio_version=portfolio_version,
        security=security,
        planned_position=10,
        position=2,
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    try:
        yield weight
    finally:
        weight.delete_instance()


@pytest.fixture
def order(security, portfolio_version):
    order = Order.create(
        security=security,
        portfolio_version=portfolio_version,
        status="Created",
        type="buy",
        desired_price=100,
        updated_at=datetime.now(),
        created_at=datetime.now(),
    )
    try:
        yield order
    finally:
        order.delete_instance()
