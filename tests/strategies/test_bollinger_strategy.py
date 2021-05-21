import pytest
import backtrader as bt
from tests import testcommon
from trade.strategies.bollinger_strategy import BollingerStrategy


class TestBollingerStrategy:
    @pytest.fixture
    def subject(self):
        return BollingerStrategy

    def test_implement_me(self):
        assert False
