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
        assert type(result.value) == dict
        assert result.value["AAPL"] == 0
        assert result.value["MSFT"] == 0
