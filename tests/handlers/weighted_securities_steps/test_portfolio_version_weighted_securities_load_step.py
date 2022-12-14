import pytest

from ftt.handlers.weighted_securities_steps.portfolio_version_weighted_securities_load_step import (
    PortfolioVersionWeightedSecuritiesLoadStep,
)
from ftt.storage import schemas


class TestPortfolioVersionWeightedSecuritiesLoadStep:
    @pytest.fixture
    def subject(self):
        return PortfolioVersionWeightedSecuritiesLoadStep

    def test_returns_weighted_securities_of_portfolio_version(
        self, subject, portfolio_version, weight
    ):
        result = subject.process(
            portfolio_version=schemas.PortfolioVersion(id=portfolio_version.id)
        )

        assert result.is_ok()
        assert isinstance(result.value[0], schemas.WeightedSecurity)
        assert result.value[0].symbol == weight.security.symbol

    def test_returns_err_when_portfolio_version_missing(self, subject):
        result = subject.process(portfolio_version=schemas.PortfolioVersion(id=567))

        assert result.is_err()
        assert result.unwrap_err() == "Portfolio Version with ID 567 does not exist."

    def test_returns_err_when_portfolio_missing(
        self, subject, portfolio, portfolio_version
    ):
        portfolio.delete_instance()
        result = subject.process(
            portfolio_version=schemas.PortfolioVersion(id=portfolio_version.id)
        )

        assert result.is_err()
        assert (
            result.unwrap_err()
            == "Portfolio of Portfolio Version with ID 1 does not exist."
        )

    def test_returns_empty_result_when_portfolio_version_is_not_created(self, subject):
        result = subject.process(portfolio_version=schemas.PortfolioVersion())

        assert result.is_ok()
        assert result.value == []
