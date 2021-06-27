from datetime import datetime

import pytest
import backtrader as bt
#
from trade.storage.models import Portfolio, Security, PortfolioVersion, Weight


# from trade.piloting.strategies.sizers import WeightedSizer
#
#
# @pytest.fixture(autouse=True, scope="function")
# def transactional():
#     connection = database_connection()
#     with connection.atomic() as transaction:
#         try:
#             yield
#         finally:
#             transaction.rollback()
#
#
# @pytest.fixture
# def cerebro(portfolio_version, ticker, weight):
#     def _cerebro(strategies, data):
#         cerebro = bt.Cerebro(live=True, cheat_on_open=True)
#         for strategy in strategies:
#             if type(strategy) == tuple:
#                 strategy, opts = strategy
#                 cerebro.addstrategy(strategy, portfolio_version_id=portfolio_version.id, **opts)
#             else:
#                 cerebro.addstrategy(strategy, portfolio_version_id=portfolio_version.id)
#         cerebro.addsizer(WeightedSizer)
#
#         cerebro.adddata(data, name=ticker.symbol)
#
#         cerebro.broker.setcash(30000.0)
#         return cerebro
#
#     return _cerebro
#
#
@pytest.fixture
def security():
    ticker = Security.create(
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
        created_at=datetime.now()
    )
    try:
        yield ticker
    finally:
        ticker.delete_instance()


@pytest.fixture
def portfolio():
    portfolio = Portfolio.create(
        name="Portfolio TEST 1",
        size=30000.0,
        updated_at=datetime.now(),
        created_at=datetime.now()
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
        created_at=datetime.now()
    )
    try:
        yield portfolio_version
    finally:
        portfolio_version.delete_instance()


@pytest.fixture
def weight(portfolio_version, security):
    weight = Weight.create(
        portfolio_version=portfolio_version,
        ticker=security,
        planned_position=10,
        position=2,
        updated_at=datetime.now(),
        created_at=datetime.now()
    )
    try:
        yield weight
    finally:
        weight.delete_instance()


# @pytest.fixture
# def order(ticker, portfolio_version):
#     order = Order.create(
#         ticker=ticker,
#         portfolio_version=portfolio_version,
#         status="Created",
#         type="buy",
#         desired_price=100,
#         updated_at=datetime.now(),
#         created_at=datetime.now()
#     )
#     try:
#         yield order
#     finally:
#         order.delete_instance()
