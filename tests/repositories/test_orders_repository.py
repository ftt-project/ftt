import pytest

from trade.models import Order
from trade.repositories import OrdersRepository


class TestOrdersRepository:
    @pytest.fixture
    def subject(self):
        return OrdersRepository()

    def test_create(self, subject, ticker, portfolio_version):
        result = subject.create({
            "ticker": ticker,
            "portfolio_version": portfolio_version,
            "status": "created",
            "desired_price": 100
        })

        assert type(result) == Order
        assert result.id is not None
        result.delete_instance()

    def test_build_and_create(self, subject, ticker, portfolio_version):
        result = subject.build_and_create(
            symbol_name=ticker.symbol,
            portfolio_version_id=portfolio_version.id,
            desired_price=1
        )
        assert type(result) == Order
        assert result.id is not None

        result.delete_instance()

    @pytest.mark.skip(reason="Not implemented")
    def test_save(self):
        pass

    @pytest.mark.skip(reason="Not implemented")
    def test_get_by_id(self):
        pass

    def test_get_by_portfolio(self, subject, portfolio, order):
        result = subject.get_orders_by_portfolio(portfolio)

        assert type(result) == list
        assert len(result) == 1
        assert result[0] == order
