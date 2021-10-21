import pytest

from ftt.handlers.weights_steps.weights_load_step import WeightsLoadStep


class TestWeightsLoadStep:
    @pytest.fixture
    def subject(self):
        return WeightsLoadStep

    def test_returns_list_of_weights_by_portfolio_version(
        self, subject, portfolio_version, weight, security
    ):
        result = subject.process(portfolio_version)

        assert result.is_ok()
        assert result.value[0] == weight
