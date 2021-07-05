import pytest

from trade.handlers.portfolio_stats_handler import PortfoliosStatsHandler


class TestPortfoliosStatsHandler:
    @pytest.fixture
    def subject(self):
        return PortfoliosStatsHandler()

    def test_runs(self, subject, portfolio_version, weight, security):
        result = subject.handle(portfolio_version=portfolio_version)

        assert result.is_ok()
        assert "planned_weights" in result.value
