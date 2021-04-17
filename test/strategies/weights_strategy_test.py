from test import testcommon
from trade.sizers.weighted_portfolio_sizer import WeightedPortfolioSizer
from trade.strategies import WeightsStrategy


class TestStrategy:
    """
    Implementation:
    - [ ] It must buy according to the given weights
    """

    def test_it(self):
        datas = {"AA.XX": testcommon.getdata(0)}  # it is multilines strategy
        testcommon.runtest(datas,
                           WeightsStrategy,
                           sizer=WeightedPortfolioSizer)

    def test_uses_the_total_cash_value(self):
        pass

    def test_set_the_final_cash_value(self):
        pass

    def test_creates_orders_for_each_position_in_portfolio(self):
        pass

    def test_updates_position_value_in_weights(self):
        pass

    def test_buys_positions(self):
        pass
