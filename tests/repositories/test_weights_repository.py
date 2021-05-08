from datetime import datetime

import pandas as pd
from pytest import fixture

from trade.models import Weight, Portfolio, PortfolioVersion, Ticker
from trade.repositories import TickersRepository
from trade.repositories.portfolio_versions_repository import PortfolioVersionsRepository
from trade.repositories.portfolios_repository import PortfoliosRepository
from trade.repositories.weights_repository import WeightsRepository


class TestWeightsRepository:
    @fixture
    def subject(self):
        return WeightsRepository()

    @fixture
    def ticker(self):
        ticker, _ = TickersRepository().upsert(pd.Series({
            "symbol": "AA.XX",
            "exchange": "SYD",
            "company_name": "Company AAXX",
            "exchange_name": "SYD",
            "type": "Stock",
            "type_display": "Stock",
            "industry": "Technologie",
            "currency": "USD"
        }))
        return ticker

    @fixture
    def portfolio(self):
        return PortfoliosRepository().create({"name": "P1"})

    @fixture
    def portfolio_version(self, portfolio):
        return PortfolioVersionsRepository().get_latest_version(portfolio_id=portfolio.id)

    @fixture
    def data(self, ticker, portfolio_version):
        return {
            "portfolio_version": portfolio_version,
            "ticker": ticker,
            "planned_position": 2,
            "position": 10
        }

    @fixture
    def weight(self, data):
        data['updated_at'] = datetime.now()
        data['created_at'] = datetime.now()
        return Weight.create(**data)

    @fixture(autouse=True)
    def cleanup(self):
        yield
        Weight.delete().execute()
        Portfolio.delete().execute()
        PortfolioVersion.delete().execute()
        Ticker.delete().execute()

    def test_create(self, subject, data):
        result = subject.create(data)

        assert type(result) == Weight
        assert result.id is not None

    def test_upsert(self, subject, data, weight):
        result = subject.upsert(data)

        assert result == weight

    def test_get_by_ticker_and_portfolio_version(self, subject, portfolio_version, ticker, weight):
        result = subject.get_by_ticker_and_portfolio_version(
            portfolio_version_id=portfolio_version.id,
            ticker_id=ticker.id
        )

        assert result == weight
