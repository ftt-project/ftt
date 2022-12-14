import pytest

from ftt.handlers.weighted_securities_steps.portfolio_weighted_securities_load_step import (
    PortfolioWeightedSecuritiesLoadStep,
)
from ftt.storage import schemas


class TestPortfolioWeightedSecuritiesLoadStep:
    @pytest.fixture
    def subject(self):
        return PortfolioWeightedSecuritiesLoadStep

    def test_returns_weighted_securities_for_given_portfolio(
        self, subject, portfolio_security, portfolio
    ):
        result = subject.process(portfolio=schemas.Portfolio.from_orm(portfolio))

        assert result.is_ok()
        assert isinstance(result.value[0], schemas.WeightedSecurity)
        assert result.value[0].symbol == portfolio_security.security.symbol

    def test_returns_err_when_portfolio_missing(self, subject):
        result = subject.process(portfolio=schemas.Portfolio(id=761))

        assert result.is_err()
        assert result.unwrap_err() == "Portfolio with ID 761 does not exist."
