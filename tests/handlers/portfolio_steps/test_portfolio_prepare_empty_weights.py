import pytest

from trade.handlers.portfolio_steps.portfolio_prepare_empty_weights_step import PortfolioPrepareEmptyWeightsStep


class TestPortfolioPrepareEmptyWeightsStep:
    @pytest.fixture
    def subject(self):
        return PortfolioPrepareEmptyWeightsStep

    def test_returns_empty_weights(self, subject):
        result = subject.process(
            securities=["AAPL", "MSFT"]
        )

        assert result.is_ok()
        assert type(result.value) == tuple
        assert result.value[0]["AAPL"] == 0
        assert result.value[0]["MSFT"] == 0
        assert result.value[1] == 0
