import pytest

from trade.handlers.weights_list_handler import WeightsListHandler


class TestWeightsLoadHandler:
    @pytest.fixture
    def subject(self):
        return WeightsListHandler()

    def test_returns_list_of_weights_by_portfolio_version(
        self, subject, portfolio_version, weight
    ):
        result = subject.handle(portfolio_version=portfolio_version)

        assert result.is_ok()
        assert result.value[0] == weight
