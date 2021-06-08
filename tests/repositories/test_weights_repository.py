from datetime import datetime

import pandas as pd
from pytest import fixture

from trade.models import Weight
from trade.repositories import TickersRepository
from trade.repositories import PortfolioVersionsRepository
from trade.repositories import PortfoliosRepository
from trade.repositories import WeightsRepository


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

    def test_find_by_ticker_and_portfolio(self, subject, ticker, portfolio_version, weight):
        result = subject.find_by_ticker_and_portfolio(ticker=ticker, portfolio_version_id=portfolio_version.id)
        assert result == weight

    def test_update_amount(self, weight, subject):
        subject.update_amount(weight, 101)
        assert Weight.get(weight.id).amount == 101

    def test_lock_weight(self, subject, weight):
        result = subject.lock_weight(weight, 101)
        assert result.locked_at_amount == 101
        assert result.locked_at is not None

    def test_unlock_weight(self, subject, weight):
        result = subject.unlock_weight(weight)
        assert result.locked_at_amount is None
        assert result.locked_at is None

    def test_update_on_sell(self, subject, weight):
        weight.peaked_value = 101
        weight.amount = 1000
        weight.save()

        result = subject.update_on_sell(weight)
        assert 0 == result.amount
        assert 0 == result.peaked_value

    def test_update_on_buy(self, subject, weight):
        result = subject.update_on_buy(weight, 89)
        assert 89 == result.amount
