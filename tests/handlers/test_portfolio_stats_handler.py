import pytest

from trade.handlers.portfolio_stats_handler import PortfoliosStatsHandler


class TestPortfoliosStatsHandler:
    @pytest.fixture
    def subject(self):
        return PortfoliosStatsHandler
