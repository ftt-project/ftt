from datetime import datetime

import pytest

import pandas as pd

from trade.models import Weight, Ticker, Portfolio, PortfolioVersion
from trade.repositories import TickersRepository
from trade.repositories.portfolio_versions_repository import PortfolioVersionsRepository
from trade.repositories.portfolios_repository import PortfoliosRepository


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
def weight(data, portfolio_version, ticker):
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
