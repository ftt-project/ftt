import pytest

from trade.handlers.portfolio_steps.portfolio_weights_allocation_step import PortfolioWeightsAllocationStep


class TestPortfolioWeightsAllocationStep:
    @pytest.fixture
    def subject(self):
        return PortfolioWeightsAllocationStep

    def test_returns_latest_version_weights_and_allocations(self, subject, portfolio_version, security, weight):
        result = subject.process(portfolio_version)

        assert result.is_ok()
        assert type(result.value) == dict
        assert result.value["planned_weights"][security.symbol] == weight.planned_position
