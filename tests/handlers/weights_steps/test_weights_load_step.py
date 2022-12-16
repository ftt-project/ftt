import pytest

from ftt.handlers.weights_steps.weights_load_step import WeightsLoadStep
from ftt.storage import schemas


class TestWeightsLoadStep:
    @pytest.fixture
    def subject(self):
        return WeightsLoadStep

    def test_returns_list_of_weights_by_portfolio_version(
        self, subject, portfolio_version, weight, security
    ):
        result = subject.process(schemas.PortfolioVersion(id=portfolio_version.id))

        assert result.is_ok()
        assert isinstance(result.value, list)
        assert isinstance(result.value[0], schemas.WeightedSecurity)
        assert result.value[0].id == weight.id

    def test_returns_err_when_portfolio_version_not_found(self, subject):
        result = subject.process(schemas.PortfolioVersion(id=567))

        assert result.is_err()
        assert result.value == "Portfolio Version with ID 567 does not exist"
