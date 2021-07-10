import pytest

from trade.handlers.portfolio_steps.portfolio_weights_persist_step import PortfolioWeightsPersistStep
from trade.handlers.weights_steps.weights_calculate_step import WeightsCalculateStepResult
from trade.storage.models.portfolio_version import PortfolioVersion
from trade.storage.models.weight import Weight


class TestPortfolioWeightsPersistStep:
    @pytest.fixture
    def subject(self):
        return PortfolioWeightsPersistStep

    @pytest.fixture
    def calculation_result(self, security):
        return WeightsCalculateStepResult(
            allocation={security.symbol: 80},
            leftover=25.599999999998545,
            expected_annual_return=10,
            annual_volatility=14,
            sharpe_ratio=15
        )

    def test_persist_weights(self, subject, calculation_result, portfolio_version):
        result = subject.process(portfolio_version, calculation_result, True)

        assert result.is_ok()
        assert type(result.value) == list
        assert isinstance(result.value[0], Weight)

    def test_persist_weights_is_false(self, subject, calculation_result, portfolio_version):
        result = subject.process(portfolio_version, calculation_result, False)

        assert result.is_ok()
        assert type(result.value) == list
        assert len(result.value) == 0

    def test_updates_portfolio_version_with_stats(self, subject, calculation_result, portfolio_version):
        result = subject.process(portfolio_version, calculation_result, True)

        portfolio_version = PortfolioVersion.get(portfolio_version.id)
        assert result.is_ok()
        assert portfolio_version.expected_annual_return is not None
        assert portfolio_version.annual_volatility is not None
        assert portfolio_version.sharpe_ratio is not None
