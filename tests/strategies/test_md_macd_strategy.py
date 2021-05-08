import pytest
from tests import testcommon
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

    def test_it(self, subject, portfolio_version):
        datas = {
            "AA.BB": testcommon.getdata(0),
        }

        testcommon.runtest(datas,
                           subject,
                           portfolio_version_id=portfolio_version.id,
                           sizer=WeightedSizer)

    @pytest.mark.skip(reason="Not implemented")
    def test_uses_the_total_cash_value(self):
        pass

    @pytest.mark.skip(reason="Not implemented")
    def test_set_the_final_cash_value(self):
        pass

    @pytest.mark.skip(reason="Not implemented")
    def test_creates_orders_for_each_position_in_portfolio(self):
        pass

    @pytest.mark.skip(reason="Not implemented")
    def test_updates_position_value_in_weights(self):
        pass

    @pytest.mark.skip(reason="Not implemented")
    def test_buys_positions(self):
        pass
