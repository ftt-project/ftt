from test import testcommon
from trade.strategies.sizers import WeightedSizer
from trade.strategies import WeightsStrategy


class TestWeightsStrategy:
    """
    Implementation:
    - [ ] It must buy according to the given weights using Weight sizer
    """

    def test_it(self):
        pass
        # datas = {
        #     "AA.BB": testcommon.getdata(0),
        # }
        #
        # testcommon.runtest(datas,
        #                    WeightsStrategy,
        #                    portfolio_id=weights_seed.portfolio.id,
        #                    sizer=WeightedPortfolioSizer)

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
