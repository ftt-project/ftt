import pytest

from ftt.handlers.weights_list_load_handler import WeightsListLoadHandler
from ftt.storage import schemas


class TestWeightsListLoadHandler:
    @pytest.fixture
    def subject(self):
        return WeightsListLoadHandler()

    def test_returns_list_of_weights_by_portfolio_version(
        self, subject, portfolio_version, weight
    ):
        result = subject.handle(
            portfolio_version=schemas.PortfolioVersion(id=portfolio_version.id)
        )

        assert result.is_ok()
        assert isinstance(result.value, list)
        assert isinstance(result.value[0], schemas.WeightedSecurity)
        assert result.value[0].id == weight.id
