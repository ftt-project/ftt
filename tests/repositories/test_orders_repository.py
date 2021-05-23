from datetime import datetime

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
            "type": "buy",
            "desired_price": 100
        })

        assert type(result) == Order
        assert result.id is not None
        result.delete_instance()

    def test_build_and_create(self, subject, ticker, portfolio_version):
        result = subject.build_and_create(
            symbol_name=ticker.symbol,
            portfolio_version_id=portfolio_version.id,
            desired_price=1,
            type="buy"
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

    def test_update_status(self, subject, order):
        result = subject.update_status(status="submitted", order_id=order.id)

        assert result.id == order.id
        assert "submitted" == subject.get_by_id(order.id).status

    def test_last_not_closed_order_when_order_exist(self, subject, order, portfolio, portfolio_version, ticker):
        order_closed = Order.create(
            ticker=ticker,
            type="buy",
            portfolio_version=portfolio_version,
            status=Order.Completed,
            executed_at=datetime.now(),
            desired_price=10,
            execution_price=10,
            updated_at=datetime.now(),
            created_at=datetime.now()
        )
        found = subject.last_not_closed_order(portfolio, ticker)
        assert found == order

        order_closed.delete_instance()

    def test_last_not_closed_order_when_no_orders(self, subject, portfolio, ticker):
        found = subject.last_not_closed_order(portfolio, ticker)
        assert found is None