import pytest
import backtrader as bt
from tests import testcommon
from trade.models import Order
from trade.repositories import OrdersRepository
from trade.strategies.md_macd_strategy import MdMACDStrategy
from trade.strategies.sizers import WeightedSizer


class TestMdMACDStrategy:
    """
    Implementation:
    - [ ] It must buy according to the given weights using Weight sizer
    """

    @pytest.fixture
    def subject(self):
        return MdMACDStrategy

    @pytest.fixture
    def cerebro(self, subject, portfolio_version, ticker, weight):
        cerebro = bt.Cerebro(live=True)
        cerebro.addstrategy(subject, portfolio_version_id=portfolio_version.id)
        cerebro.addsizer(WeightedSizer)

        data = testcommon.getdata(0)
        cerebro.adddata(data, name=ticker.symbol)

        cerebro.broker.setcash(30000.0)
        return cerebro

    def test_buys_with_given_cash_allocation_and_one_ticker(self, subject, cerebro):
        result = cerebro.run()
        assert 428.15999999999985 == cerebro.broker.cash
        assert type(result[0]) == subject
        assert type(result[0]._orders) == list
        Order.delete().execute()

    @pytest.mark.skip(reason="Not implemented")
    def test_uses_the_total_cash_value(self):
        pass

    @pytest.mark.skip(reason="Not implemented")
    def test_set_the_final_cash_value(self):
        pass

    def test_creates_orders_for_each_position_in_portfolio(self, cerebro, portfolio):
        orders_before = OrdersRepository().get_orders_by_portfolio(portfolio)
        assert len(orders_before) == 0
        _ = cerebro.run()
        orders_after = OrdersRepository().get_orders_by_portfolio(portfolio)
        assert len(orders_after) == 1
        Order.delete().execute()


    @pytest.mark.skip(reason="Not implemented")
    def test_updates_position_value_in_weights(self):
        pass

    @pytest.mark.skip(reason="Not implemented")
    def test_buys_positions(self):
        pass
